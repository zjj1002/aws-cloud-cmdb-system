"""Data persistence for responses and any exceptions while invoking operations."""

import datetime
import json
import logging
import pickle
import string
import sys
import time
import uuid
import boto3

# import botocore
from inventory.aws_inventory import version
from libs.db_context import DBContext
from libs.web_logs import ins_log
from models.all_assets import AllAssets

LOGGER = logging.getLogger(__name__)


class ComplexEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            return obj.strftime('%Y-%m-%d %H:%M:%S')
        elif isinstance(obj, datetime.date):
            return obj.strftime('%Y-%m-%d')
        else:
            return json.JSONEncoder.default(self, obj)


class ResponseEncoder(json.JSONEncoder):
    """Encode responses from operations in order to serialize to JSON."""

    def default(self, o):
        if isinstance(o, datetime.datetime):
            return o.isoformat()
        return super(ResponseEncoder, self).default(o)


class ResultStore(object):
    """Storage and serialization for responses and exceptions."""

    def __init__(self, profile):
        self.profile = profile
        self._response_store = {}  # {svc: {region: {svc_op: response}}}
        self._exception_store = {}  # {svc: {svc_op: {region: exception}}}
        self.run_date = time.strftime('%Y-%m-%d %H:%M:%S %Z')
        self.commandline = ' '.join(sys.argv)
        self.version = version.__version__
        self.response_data = []

    def add_response(self, service, region, svc_op, resp):
        """Add a response to the store for a given service for an operation in a region. Replace
        existing values.

        :param str service: service name
        :param str region: region name
        :param str svc_op: service operation name
        :param dict resp: response from invoking an API
        """
        self.response_data.append([service, region, svc_op, resp])
        svc_store = self._response_store.setdefault(service, {})
        svc_store.setdefault(region, {})[svc_op] = resp

    def add_exception(self, service, region, svc_op, exc):
        """Add an exception to the store for a given service for an operation in a region. Replace
        existing values.

        :param str service: service name
        :param str region: region name
        :param str svc_op: service operation name
        :param dict exc: exception from invoking an API
        """
        svc_store = self._exception_store.setdefault(service, {})
        svc_store.setdefault(svc_op, {})[region] = str(exc)

    def has_exceptions(self, service, svc_op):
        """Check whether a service operation has any exceptions.

        :param str service: service name
        :param str svc_op: service operation name
        :rtype: bool
        :return: whether there are exceptions
        """
        try:
            return len(self._exception_store[service][svc_op]) > 0
        except KeyError:
            return False

    def get_response_store(self):
        """Serialize response store to JSON.

        :rtype: str
        :return: serialized response store in JSON format
        """
        LOGGER.debug('Building the response store.')
        return json.dumps(self._response_store, cls=ResponseEncoder)

    def dump_response_store(self, fp):
        """Pickle the response store.

        :param file fp: file to write to
        """
        LOGGER.debug('Writing the response store to file "%s".', fp.name)
        pickle.dump(self._response_store, fp)

    def dump_exception_store(self, fp):
        """Pickle the exception store.

        :param file fp: file to write to
        """
        LOGGER.debug('Writing the exception store to file "%s".', fp.name)
        pickle.dump(self._exception_store, fp)

    def generate_data_file(self, fp):
        """Generate the data file for consumption by the data GUI.

        :param file fp: file to write to
        """

        service_data = self.response_data
        with DBContext('w') as session:
            session.query(AllAssets).delete(synchronize_session=False)  # 清空数据库的所有记录
            for data in service_data:
                service_name = data[0]
                regions = data[1]
                operation = data[2]
                response = data[3]
                try:
                    operation_data = json.dumps(response, cls=ComplexEncoder)
                except Exception as e:
                    ins_log.read_log('error', e)
                    operation_data = json.dumps('{!r}'.format(response), cls=ComplexEncoder)
                try:
                    new_data = AllAssets(
                        service_name=service_name, regions=regions,
                        operation=operation, operation_data=operation_data)
                    session.add(new_data)
                    session.commit()
                except Exception as e:
                    ins_log.read_log('error', e)

        def build_children(obj):
            children = []
            if isinstance(obj, dict):
                for key, val in obj.items():
                    child = build_children(val)
                    if isinstance(child, (dict, list, tuple)) and child:
                        children.append({'text': key, 'children': child})
                    else:
                        # leaf node
                        try:
                            children.append({'text': u'{} = {}'.format(key, val)})
                        except UnicodeDecodeError:
                            # key or value is probably binary. For example, CloudTrail API ListPublicKeys
                            children.append({'text': u'{} = {!r}'.format(key, val)})
            elif isinstance(obj, (list, tuple)):
                for i, val in enumerate(obj):
                    child = build_children(val)
                    if isinstance(child, (dict, list, tuple)) and child:
                        children.append({'text': '[{:d}]'.format(i), 'children': child})
                    else:
                        # leaf node
                        children.append({'text': child})
            else:
                return obj
            return children
        LOGGER.debug('Building the GUI data model.')
        data = build_children({'[inventory]': self._response_store})

        # assign types to nodes so jsTree can handle them appropriately

        data[0]['type'] = 'root'
        data[0]['state'] = {'opened': True}
        for service in data[0]['children']:
            service['type'] = 'service'
            service['state'] = {'opened': True}
            for region in service['children']:
                region['type'] = 'region'
                region['state'] = {'opened': True}
                num_hidden_operations = 0
                for operation in region['children']:
                    operation['type'] = 'operation'

                    # add count of non empty response to operation name

                    try:
                        num_non_empty_responses = 0
                        for response in operation['children']:
                            try:
                                if response['text'] == 'ResponseMetadata':
                                    response['type'] = 'response_metadata'
                                    continue  # ignore metadata nodes in count
                                num_non_empty_responses += 1 if response['children'] else 0
                            except KeyError:
                                # an empty response
                                pass
                        if num_non_empty_responses:
                            operation['text'] += ' ({:d})'.format(num_non_empty_responses)
                        else:
                            num_hidden_operations += 1
                            operation['state'] = {"hidden": True}
                    except KeyError:
                        # no response
                        pass
                region['a_attr'] = {'title': '{:d} hidden operations'.format(num_hidden_operations)}

        out_obj = {'run_date': self.run_date,
                   'commandline': self.commandline,
                   'version': self.version,
                   'botocore_version': boto3.__version__,
                   'responses': data}
        LOGGER.debug('Writing the GUI data model to file "%s".', fp.name)
        json.dump(out_obj, fp, cls=ResponseEncoder)
