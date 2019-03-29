# This searches for channels you specify in ./inputs/channel_list.txt and sets the purpose to what you set channel_purpose to

import os
import sys
import json
from slackclient import SlackClient

# Get Modules In pkg Folder
sys.path.append(os.getcwd()) 
from pkg import channels, common

#
# Constants
#
slack_yml = common.import_yaml('./secrets/slack-automation.yml')
slack_client = SlackClient(slack_yml['token']) 
channels_list = common.read_file('./inputs/channels_list.txt')

#
# Variables
#
channel_purpose = "This is the channel purpose from code"

#
# The Fun Stuff
#
def main():
    print('WARNING: This Only Works With Public Channels, If One Of The Channels Is Private You Need To Be Invited To It First')
    all_channels = channels.get_channels(slack_client)
    # Get Target Channels From All_Channels Array
    for channel_name in channels_list:
        print('INFO: Searching all channels for {0}'.format(channel_name))
        target_channels = channels.get_target_channels(all_channels, channel_name)
        # Set Purpose For The Existing Targeted Channels
        for k, v in target_channels.items():
            purpose = v['purpose']
            value = purpose['value']
            if value == "":
                channels.set_channelpurpose(slack_client, v, channel_purpose)
            elif value == channel_purpose or channel_purpose in value:
                print("WARNING: {0}'s purpose is already set to or already contains".format(k, channel_purpose))
                continue
            else:
                # Append Purpose To Existing Purpose
                print('WARNING: {0} has a different purpose already set - appending to existing value'.format(k))
                channel_purpose_full = value + " - " + channel_purpose
                set_channelpurpose(slack_client, v, channel_purpose_full)

if __name__ == '__main__':
    print('INFO: Running set-channel-purpose.py')
    main()