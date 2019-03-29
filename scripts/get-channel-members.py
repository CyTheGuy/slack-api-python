# This will write out the members to ./outputs/channel_members.txt and also print it to the console

import os
import sys
import json
from slackclient import SlackClient

# Get Modules In pkg Folder
sys.path.append(os.getcwd()) 
from pkg import channels, common, users, bots

#
# Constants
#
slack_yml = common.import_yaml('./secrets/slack-automation.yml')
slack_client = SlackClient(slack_yml['token']) 
channel_name = "random"

#
# The Fun Stuff
#
def main():
    channel_info = channels.get_channel(slack_client, channel_name)
    if channel_info == None:
        print('ERROR: Failed To Retrieve Info For {0} make sure it exists and you spelled it right'.format(channel_name))
    else:
        # By default only returns active members - add false to parameters if you want to include deleted users
        members = channels.get_members(slack_client, channel_info)
    print('#################################################')
    print('Name, Delete, Is Bot, Is App User')
    print('#################################################')
    for member in members.keys():
        if member == 'QUIP_ID':
            print('Quip is a member')
            continue
        userinfo = users.get_user(slack_client, member)
        try:
            print('{0} | {1} | {2} | {3}'.format(userinfo['name'], userinfo['deleted'], userinfo['is_bot'], userinfo['is_app_user']))
        except:
            print('There was an issue outputting user info for {0} - seeing if they are a bot'.format(json.dumps(member, sort_keys=True,indent=4, separators=(',', ': '))))
            botinfo = bots.get_bot(slack_client, member)
            
    print('INFO: End Of Script')
        
if __name__ == '__main__':
    print('INFO: Running get-channel-members.py')
    main()