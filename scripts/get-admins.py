# Gets A List Of All Admins & Workspace Owners

import os
import sys
from slackclient import SlackClient

# Get Modules In pkg Folder
sys.path.append(os.getcwd()) 
from pkg import users, common

#
# Constants
#
slack_yml = common.import_yaml('./secrets/slack-automation.yml')
slack_client = SlackClient(slack_yml['token'])

#
# The Fun Stuff
#
def main():
    all_users = users.get_allusers(slack_client)
    # Get Active Admins
    admins = {k:v for (k,v) in all_users.items() if v['deleted'] == False and v['is_admin'] == True and v['is_owner'] == False}
    # Get Active Workspace Owners
    owners = {k:v for (k,v) in all_users.items() if v['deleted'] == False and v['is_admin'] == True and v['is_owner'] == True}
    print('INFO: These People Are Admins:')
    for k, v in admins.items():
        print(k)
    print('INFO: These People Are Workspace Owners:')
    for k, v in owners.items():
        print(k)
    print('INFO: End Of Script')

if __name__ == '__main__':
    print('INFO: Running get-admins.py')
    main()