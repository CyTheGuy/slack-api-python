# This script checks for channels that only the quip app is a member of and it will archive the channels.

import os
import sys
from slackclient import SlackClient

# Get Modules In pkg Folder
sys.path.append(os.getcwd()) 
from pkg import users, common, channels, messages

def get_quipid(slack_client):
    all_users = users.get_allusers(slack_client)
    quip = {k:v for (k,v) in all_users.items() if k == 'quip'}
    print('INFO: Quip ID = {0}'.format(quip['quip']['id']))
    return quip['quip']['id']

#
# Stuff
#
slack_yml = common.import_yaml('./secrets/slack-automation.yml')
slack_client = SlackClient(slack_yml['token'])                            ############ Use the token to send message as ArchiveBot
channel_dict = {}
quip_id = get_quipid(slack_client)

#
# The Fun Stuff
#
def main():
    # Get All Channels
    all_channels = channels.get_channels(slack_client)
    # Grab channels with 0 members - if private channel skip because num_members is NOT returned for private channels
    zero_members = {k:v for (k,v) in all_channels.items() if v['is_private'] == False and v['num_members'] == 0 and v['is_archived'] == False}
    print('INFO: {0} channels with 0 members'.format(str(len(zero_members))))
    # Grab channels with 1 member - if private channel skip because num_members is NOT returned for private channels
    one_member = {k:v for (k,v) in all_channels.items() if v['is_private'] == False and v['num_members'] == 1 and v['is_archived'] == False}
    print('INFO: {0} channels with 1 member'.format(str(len(one_member))))
    # Archive 0 member channels
    for k, v in zero_members.items():
        print('INFO: {0} has zero members in it'.format(k))
        result = messages.create_message(slack_client, v, "Archiving this channel because there are zero members in it")
        if result != 1:
            channels.archive_channel(slack_client, v)
    # Check if quip is only member and archive the channel
    for k, v in one_member.items():
        members = channels.get_members(slack_client, v)
        if quip_id in members:
            print('INFO: Quip is the only member of - {0}'.format(k))
            result = messages.create_message(slack_client, v, "Archiving this channel because there are zero members in it")
            if result != 1:
                channels.archive_channel(slack_client, v)
    print('INFO: End of script')

if __name__ == '__main__':
    print('INFO: Running archive-channels-zero-members.py')
    main()