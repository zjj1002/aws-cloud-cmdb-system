#!/usr/bin/env python
import argparse
import logging
import os.path

import botocore
import boto3
from opinel.utils.console import configPrintException

import inventory.aws_inventory.config
import inventory.aws_inventory.blacklist
import inventory.aws_inventory.invoker


# create a module logger and ignore messages outside of the module. botocore was spewing messages
from libs.catch_execption import catch_exceptions_util
from libs.db_context import DBContext
from models.all_assets import AllAssets

logging.basicConfig()
LOGGER = logging.getLogger(inventory.aws_inventory.__name__)
LOGGER.addFilter(logging.Filter(inventory.aws_inventory.__name__))


def setup_logging(verbose):
    LOGGER.setLevel(logging.DEBUG if verbose else logging.INFO)


def parse_args(args=None):
    parser = argparse.ArgumentParser(
        description='Discover resources in an AWS account.'
    )

    parser.add_argument('--profile',
                        default='default',
                        help='Name of the profile (default: %(default)s)')

    parser.add_argument('--mfa-serial',
                        help='serial number of MFA device')

    parser.add_argument('--mfa-code',
                        help='MFA code')

    parser.add_argument('--csv-credentials',
                        help='CSV file containing account credentials')

    parser.add_argument('--services',
                        default=[],
                        nargs='+',
                        help='Name of AWS services to include')

    parser.add_argument('--exclude',
                        dest='excluded_services',
                        default=[],
                        nargs='+',
                        help='Name of AWS services to exclude')

    parser.add_argument('--regions',
                        default=[],
                        nargs='+',
                        help='Name of regions to include, defaults to all')

    parser.add_argument('--list-svcs',
                        action='store_true',
                        help=('Print a list of available services (ignore service and region '
                              'filters) and exit'))

    parser.add_argument('--list-operations',
                        action='store_true',
                        help='Print a list of operations to invoke for a given service and exit')

    parser.add_argument('--dry-run',
                        action='store_true',
                        help=('Go through local API discovery, but do not actually invoke any API. '
                              'Useful for checking filtering of regions, services, and operations.'
                        ))

    parser.add_argument('--op-blacklist',
                        type=argparse.FileType('r'),
                        default='operation_blacklist.conf',
                        help=(
                            'Configuration file listing service operations to avoid invoking ' +
                            '(default: %(default)s)'
                        ))

    parser.add_argument('--exceptions-dump', help='File to dump the exceptions store')

    parser.add_argument('--responses-dump', help='File to dump the responses store')

    parser.add_argument('--gui-data-file',
                        help='File to the GUI data (default: {})'.format(
                            inventory.aws_inventory.config.GUI_DATA_FILENAME_TEMPLATE.template
                        ))

    parser.add_argument('--debug',
                        action='store_true',
                        help='Print debugging information')

    parser.add_argument('-v', '--verbose',
                        action='store_true',
                        help='Print the account resources to stdout')

    parser.add_argument('-V', '--version',
                        action='store_true',
                        help='Print version and exit')

    parsed = parser.parse_args(args)

    if not parsed.gui_data_file:
        tool_dir = os.path.dirname(__file__)
        relative_path = inventory.aws_inventory.config.GUI_DATA_FILENAME_TEMPLATE.substitute(
            profile=parsed.profile
        )
        parsed.gui_data_file = os.path.join(tool_dir, relative_path)

    return parsed


class Arg(object):
    def __init__(self):
        pass

    @property
    def services(self):
        return []

    @property
    def profile(self):
        return 'default'

    @property
    def mfa_serial(self):
        return None

    @property
    def mfa_code(self):
        return None

    @property
    def csv_credentials(self):
        return None

    @property
    def excluded_services(self):
        return []

    @property
    def regions(self):
        return []

    @property
    def list_svcs(self):
        return None

    @property
    def list_operations(self):
        return None

    @property
    def dry_run(self):
        return None

    @property
    def op_blacklist(self):
        return parse_args().op_blacklist

    @property
    def exceptions_dump(self):
        return None

    @property
    def responses_dump(self):
        return None

    @property
    def gui_data_file(self):
        return None

    @property
    def debug(self):
        return None

    @property
    def verbose(self):
        return None

    @property
    def version(self):
        return None

    @property
    def gui_data_file(self):
        return parse_args().gui_data_file


args = Arg()
# Fill in filename-based defaults. We can't use "default" kwarg because we need another
#   commandline arg, namely the profile name.


def filter_services(api_model, services=frozenset(), excluded_services=frozenset()):
    """Build a list of services by merging together a white- and black-list.

    :param dict api_model: the reference API model
    :param frozenset services: services to include
    :param frozenset excluded_services: services to exclude
    :rtype: frozenset
    :return: the list of merged services
    """
    available = frozenset(api_model.keys())
    if services:
        invalid = services - available
        if invalid:
            raise ValueError('Invalid requested service(s): {}'.format(invalid))
        enabled = services
    else:
        enabled = available

    if excluded_services:
        invalid = excluded_services - available
        if invalid:
            raise ValueError('Invalid excluded service(s): {}'.format(invalid))
        enabled = enabled - excluded_services

    return enabled


def filter_operations(api_model, op_blacklist_parser, regions, services):
    """Build a list of operations.

    :param dict api_model: the reference API model
    :param OpBlacklistParser op_blacklist_parser: the blacklist parser
    :param list regions: regions to include
    :param list services: services to include
    :rtype: dict
    :return: dict describing operations from a service and available regions
    """
    svc_descriptors = {}
    for svc_name in services:
        # validate regions against ones available for service
        available_regions = api_model[svc_name]['regions']
        if available_regions:
            if regions:
                invalid_regions = frozenset(regions) - available_regions
                if invalid_regions:
                    LOGGER.warning('[%s] Invalid region(s): %s.', svc_name, ', '.join(invalid_regions))
                target_regions = frozenset(regions) - invalid_regions
                if not target_regions:
                    LOGGER.warning('[%s] No valid regions after applying service and region '
                                   'filters.', svc_name)
            else:
                 target_regions = available_regions
        else:
             target_regions = [None]
        svc_descriptors[svc_name] = {'regions': target_regions}

        LOGGER.debug('[%s] Service region(s) to inspect: %s.',
                     svc_name,
                     ', '.join(target_regions if available_regions else ['global']))

        operations = []
        if target_regions:
            for svc_op in api_model[svc_name]['ops']:
                if op_blacklist_parser.is_blacklisted(svc_name, svc_op):
                    LOGGER.debug('[%s] Excluding blacklisted API "%s".', svc_name, svc_op)
                else:
                    operations.append(svc_op)

        if not operations:
            LOGGER.warning('[%s] No operations to invoke for specified regions.', svc_name)

        LOGGER.info(
            '[%s] service summary - %d API(s), %d region(s).',
            svc_name,
            len(operations),
            len(target_regions))
        svc_descriptors[svc_name]['ops'] = operations

    return svc_descriptors


def build_api_model():
    """Build a model of the available API.

    :rtype: dict
    :return: dict describing operations from a service and available regions
    """

    boto3_session = boto3.session.Session()
    LOGGER.debug('Building service list.')
    available_services = frozenset(boto3_session.get_available_services())
    # available_services = ['s3', 'ec2']
    svc_descriptors = {}
    for svc_name in available_services:
        # validate regions
        # available_regions = frozenset(boto3_session.get_available_regions(svc_name, partition_name='aws-cn'))
        available_regions = ['cn-northwest-1', 'cn-north-1']
        svc_descriptors[svc_name] = {'regions': available_regions}

        if available_regions:
            LOGGER.debug(
                '[%s] Available service region(s): %s.',
                svc_name,
                ', '.join(available_regions))
        else:
            LOGGER.warning(
                '[%s] Unable to obtain a valid region. Assuming service is region agnostic (i.e., '
                'global).', svc_name)

        operations = set()
        # get operation names from local service model files
        for regions in available_regions:
            client = boto3.client(svc_name, regions)
            service_model = client._service_model
        # Filter out operations we don't care about. Currently we care about operations with
        #   names indicating a list- or describe-like action and the operation doesn't require
        #   any params.
        # create list of desired service operations
            for svc_op in service_model.operation_names:
                if inventory.aws_inventory.config.SVC_OPS_RE.match(svc_op):
                    operation_model = service_model.operation_model(svc_op)
                    try:
                        if not operation_model.input_shape.required_members:
                            operations.add(svc_op)
                    except AttributeError:
                        # no input shape
                        operations.add(svc_op)

            svc_descriptors[svc_name]['ops'] = operations

    return svc_descriptors


def get_data_main(args):

    setup_logging(args.debug)

    if args.version:
        print(inventory.aws_inventory.__version__)
        return

    api_model = build_api_model()

    if args.list_svcs:
        print('\n'.join(sorted(filter_services(api_model))))
        return

    # configure the debug level for opinel
    configPrintException(args.debug)

    # validate services against API mode #

    available_services = api_model.keys()

    if args.services:
        invalid_included_services = [svc for svc in args.services if svc not in available_services]
        if invalid_included_services:
            raise EnvironmentError('Invalid service(s) specified: {}'.format(
                ', '.join(invalid_included_services))
            )

    if args.excluded_services:
        invalid_excluded_services = [svc for svc in args.excluded_services if svc not in available_services]
        if invalid_excluded_services:
            raise EnvironmentError('Invalid service(s) to exclude: {}'.format(
                ', '.join(invalid_excluded_services))
            )

    # validate regions against API model #

    if args.regions:
        available_regions = set()
        for svc in available_services:
            available_regions.update(api_model[svc]['regions'])
        invalid_regions = [region for region in args.regions if region not in available_regions]
        if invalid_regions:
            raise EnvironmentError('Invalid region(s) specified: {}'.format(
                ', '.join(invalid_regions))
            )

    # create the list of services to analyze
    services = filter_services(api_model,
                               frozenset(args.services),
                               frozenset(args.excluded_services))
    if not services:
        raise EnvironmentError('List of AWS services to be analyzed is empty.')
    LOGGER.debug('%d AWS service(s) to inspect: %s.', len(services), ', '.join(services))

    op_blacklist_parser = inventory.aws_inventory.blacklist.OpBlacklistParser(args.op_blacklist, api_model)
    service_descriptors = filter_operations(api_model, op_blacklist_parser, args.regions, services)
    if not service_descriptors:
        raise EnvironmentError('No operations to invoke for specifed AWS services and regions.')

    ops_count = 0
    for svc_name in service_descriptors:
        ops_count += (
            len(service_descriptors[svc_name]['ops']) *
            len(service_descriptors[svc_name]['regions'])
        )
        if args.list_operations:
            print('[{}]\n{}\n'.format(
                svc_name,
                '\n'.join(service_descriptors[svc_name]['ops']) or '# NONE'
            ))

    if args.list_operations:
        print('Total operations to invoke: {}'.format(ops_count))
    else:
        LOGGER.debug('Total operations to invoke: %d.', ops_count)
        # aws_inventory.invoker.ApiInvoker(args, service_descriptors, ops_count).start()
        inventory.aws_inventory.invoker.ApiInvoker(args, service_descriptors, ops_count)._probe_services()


def get_inventory_data():
    print("开始获取数据")
    get_data_main(args)

    print("结束获取数据")


if __name__ == '__main__':
    get_inventory_data()