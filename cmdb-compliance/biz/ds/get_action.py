import json
import logging
import pkg_resources
import re
from biz.ds.athena import Athena

from colors import color
import jmespath

cloudtrail_supported_actions = None

logging.basicConfig(
    level=logging.INFO,
    format='%(levelname)-8s %(message)s'
)

SERVICE_RENAMES = {
    'monitoring': 'cloudwatch',
    'email': 'ses',
}

EVENT_RENAMES = {
    's3:listallmybuckets': 's3:listbuckets',
    's3:getbucketaccesscontrolpolicy': 's3:getbucketacl',
    's3:setbucketaccesscontrolpolicy': 's3:putbucketacl',
    's3:getbucketloggingstatus': 's3:getbucketlogging',
    's3:setbucketloggingstatus': 's3:putbucketlogging'
}

NO_IAM = {
    'sts:getcalleridentity': True,
    'sts:getsessiontoken': True,
    'signin:consolelogin': True,
    'signin:checkmfa': True,
    "signin:exitrole": True,
    "signin:renewrole": True,
    "signin:switchrole": True
}


class Privileges(object):
    """Keep track of privileges an actor has been granted"""
    stmts = None
    roles = None
    aws_api_list = None

    def __init__(self, aws_api_list):
        self.stmts = []
        self.roles = []
        self.aws_api_list = aws_api_list

    def add_stmt(self, stmt):
        """Adds a statement from an IAM policy"""
        if 'Action' not in stmt:
            # TODO Implement NotAction
            return
        self.stmts.append(stmt)

    def get_actions_from_statement(self, stmt):
        """Figures out what API calls have been granted from a statement"""
        actions = {}

        for action in make_list(stmt['Action']):
            # Normalize it
            action = action.lower()
            # Convert it's globbing to a regex
            action = '^' + action.replace('*', '.*') + '$'

            for possible_action in self.aws_api_list:
                for iam_name, cloudtrail_name in EVENT_RENAMES.items():
                    if possible_action == cloudtrail_name:
                        possible_action = iam_name
                if re.match(action, possible_action):
                    actions[possible_action] = True

        return actions

    def determine_allowed(self):
        """After statements have been added from IAM policiies, find all the allowed API calls"""
        actions = {}

        # Look at alloweds first
        for stmt in self.stmts:
            if stmt['Effect'] == 'Allow':
                stmt_actions = self.get_actions_from_statement(stmt)
                for action in stmt_actions:
                    if action not in actions:
                        actions[action] = [stmt]
                    else:
                        actions[action].append(stmt)

        # Look at denied
        for stmt in self.stmts:
            if (stmt['Effect'] == 'Deny' and
                    '*' in make_list(stmt.get('Resource', None)) and
                    stmt.get('Condition', None) is None):

                stmt_actions = self.get_actions_from_statement(stmt)
                for action in stmt_actions:
                    if action in actions:
                        del actions[action]

        return list(actions)


def make_list(obj):
    """Convert an object to a list if it is not already"""
    if isinstance(obj, list):
        return obj
    return [obj]


def normalize_api_call(service, eventName):
    """Translate API calls to a common representation"""
    service = service.lower()
    eventName = eventName.lower()

    # Remove the dates from event names, such as createdistribution2015_07_27
    eventName = eventName.split("20")[0]

    # Rename the service
    if service in SERVICE_RENAMES:
        service = SERVICE_RENAMES[service]

    return "{}:{}".format(service, eventName)


def get_account_iam(account):
    """Given account data from the config file, open the IAM file for the account"""
    return json.load(open(account['iam']))


def get_allowed_users(account_iam):
    """Return all the users in an IAM file"""
    return jmespath.search('UserDetailList[].UserName', account_iam)


def get_allowed_roles(account_iam):
    """Return all the roles in an IAM file"""
    return jmespath.search('RoleDetailList[].RoleName', account_iam)


def print_actor_diff(performed_actors, allowed_actors, use_color):
    """
    Given a list of actors that have performed actions, and a list that exist in the account,
    print the actors and whether they are still active.
    """
    PERFORMED_AND_ALLOWED = 1
    PERFORMED_BUT_NOT_ALLOWED = 2
    ALLOWED_BUT_NOT_PERFORMED = 3

    actors = {}
    for actor in performed_actors:
        if actor in allowed_actors:
            actors[actor] = PERFORMED_AND_ALLOWED
        else:
            actors[actor] = PERFORMED_BUT_NOT_ALLOWED

    for actor in allowed_actors:
        if actor not in actors:
            actors[actor] = ALLOWED_BUT_NOT_PERFORMED

    for actor in sorted(actors.keys()):
        if actors[actor] == PERFORMED_AND_ALLOWED:
            colored_print("  {}".format(actor), use_color, 'white')
        elif actors[actor] == PERFORMED_BUT_NOT_ALLOWED:
            # Don't show users that existed but have since been deleted
            continue
        elif actors[actor] == ALLOWED_BUT_NOT_PERFORMED:
            colored_print("- {}".format(actor), use_color, 'red')
        else:
            raise Exception("Unknown constant")


def get_user_iam(username, account_iam):
    """Given the IAM of an account, and a username, return the IAM data for the user"""
    user_iam = jmespath.search('UserDetailList[] | [?UserName == `{}`] | [0]'.format(username), account_iam)
    if user_iam is None:
        exit("ERROR: Unknown user named {}".format(username))
    return user_iam


def get_user_allowed_actions(aws_api_list, user_iam, account_iam):
    """Return the privileges granted to a user by IAM"""
    managed_policies = user_iam['AttachedManagedPolicies']

    privileges = Privileges(aws_api_list)

    # Get privileges from managed policies attached to the user
    for managed_policy in managed_policies:
        policy_filter = 'Policies[?Arn == `{}`].PolicyVersionList[?IsDefaultVersion == true] | [0][0].Document'
        policy = jmespath.search(policy_filter.format(managed_policy['PolicyArn']), account_iam)
        if policy is None:
            continue
        for stmt in make_list(policy['Statement']):
            privileges.add_stmt(stmt)

    # Get privileges from inline policies attached to the user
    for stmt in jmespath.search('UserPolicyList[].PolicyDocument.Statement', user_iam) or []:
        privileges.add_stmt(stmt)

    return privileges.determine_allowed()


def is_recorded_by_cloudtrail(action):
    """Given an action, return True if it would be logged by CloudTrail"""
    if action in cloudtrail_supported_actions:
        return True
    return False


def colored_print(text, use_color=True, color_name='white'):
    """Print with or without color codes"""
    if use_color:
        print(color(text, fg=color_name))
    else:
        print(text)


def print_diff(performed_actions, allowed_actions):
    """
    For an actor, given the actions they performed, and the privileges they were granted,
    print what they were allowed to do but did not, and other differences.
    """
    PERFORMED_AND_ALLOWED = 1
    PERFORMED_BUT_NOT_ALLOWED = 2
    ALLOWED_BUT_NOT_PERFORMED = 3
    ALLOWED_BUT_NOT_KNOWN_IF_PERFORMED = 4

    actions = {}
    un_used_action = []
    for action in performed_actions:
        # Convert to IAM names
        for iam_name, cloudtrail_name in EVENT_RENAMES.items():
            if action == cloudtrail_name:
                action = iam_name

        # See if this was allowed or not
        if action in allowed_actions:
            actions[action] = PERFORMED_AND_ALLOWED
        else:
            if action in NO_IAM:
                # Ignore actions in cloudtrail such as sts:getcalleridentity that are allowed
                # whether or not they are in IAM
                continue
            actions[action] = PERFORMED_BUT_NOT_ALLOWED

    # Find actions that were allowed, but there is no record of them being used
    for action in allowed_actions:
        if action not in actions:
            if not is_recorded_by_cloudtrail(action):
                actions[action] = ALLOWED_BUT_NOT_KNOWN_IF_PERFORMED
            else:
                actions[action] = ALLOWED_BUT_NOT_PERFORMED

    for action in sorted(actions.keys()):
        # Convert CloudTrail name back to IAM name
        display_name = action

        if actions[action] == PERFORMED_AND_ALLOWED:
            pass
        elif actions[action] == PERFORMED_BUT_NOT_ALLOWED:
            pass
        elif actions[action] == ALLOWED_BUT_NOT_PERFORMED:
            un_used_action.append(display_name)
        elif actions[action] == ALLOWED_BUT_NOT_KNOWN_IF_PERFORMED:
            pass
        else:
            raise Exception("Unknown constant")
    return un_used_action


def get_account(accounts, account_name):
    """
    Gets the account struct from the config file, for the account name specified

    accounts: array of accounts from the config file
    account_name: name to search for (or ID)
    """
    for account in accounts:
        if account_name == account['name'] or account_name == str(account['id']):
            # Sanity check all values exist
            if 'name' not in account or 'id' not in account or 'iam' not in account:
                exit("ERROR: Account {} does not specify an id or iam in the config file".format(account_name))

            # Sanity check account ID
            if not re.search("[0-9]{12}", str(account['id'])):
                exit("ERROR: {} is not a 12-digit account id".format(account['id']))

            return account
    exit("ERROR: Account name {} not found in config".format(account_name))
    return None


def read_aws_api_list(aws_api_list_file='aws_api_list.txt'):
    """Read in the list of all known AWS API calls"""
    api_list_path = pkg_resources.resource_filename(__name__, "data/{}".format(aws_api_list_file))
    aws_api_list = {}
    with open(api_list_path) as f:
        lines = f.readlines()
    for line in lines:
        service, event = line.rstrip().split(":")
        aws_api_list[normalize_api_call(service, event)] = True
    return aws_api_list


def run(account, username, config, start, end):
    """Perform the requested command"""

    account = get_account(config['accounts'], account)

    logging.debug("Using Athena")

    datasource = Athena(config['athena'], account, start, end)

    # Read AWS actions
    aws_api_list = read_aws_api_list()

    # Read cloudtrail_supported_events
    global cloudtrail_supported_actions
    ct_actions_path = pkg_resources.resource_filename(__name__, "/var/www/cmdb-compliance/biz/ds/data/{}".format("cloudtrail_supported_actions.txt"))
    cloudtrail_supported_actions = {}
    with open(ct_actions_path) as f:
        lines = f.readlines()
    for line in lines:
        (service, event) = line.rstrip().split(":")
        cloudtrail_supported_actions[normalize_api_call(service, event)] = True

    account_iam = get_account_iam(account)
    user_iam = get_user_iam(username, account_iam)
    search_query = datasource.get_search_query()

    allowed_actions = get_user_allowed_actions(aws_api_list, user_iam, account_iam)
    performed_actions = datasource.get_performed_event_names_by_user(
        search_query, user_iam)

    return print_diff(performed_actions, allowed_actions)
