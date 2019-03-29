# This get channels from ./inputs/channel_list.txt and checks if they have any files in ./inputs/purge_files_list.txt and then it purges the files

import os
import sys
import json
from slackclient import SlackClient

# Get Modules In pkg Folder
sys.path.append(os.getcwd()) 
from pkg import channels, files, common

#
# Constants
#
slack_yml = common.import_yaml('./secrets/slack-automation.yml')
slack_client = SlackClient(slack_yml['token']) 
channels_list = common.read_file('./inputs/channels_list.txt')
files_list = common.read_file('./inputs/purge_file_list.txt')

#
# The Fun Stuff
#
def main():
    print("WARNING: This Only Works With Public Channels, If One Of The Channels Is Private You Need To Be Invited To It First")
    for channel_name in channels_list:
        channel_info = channels.get_channel(slack_client, channel_name)
        if channel_info == None:
            print("ERROR: Failed to retrieve info for {0} make sure it exists and you spelled it right".format(channel_name))
            continue
        else:
            # list and purge files for the channels specified
            print("Targeting {0}".format(channel_name))
            files.list_files(slack_client, files_list, channel_info['id'])

if __name__ == '__main__':
    print('INFO: Running purge-files-from-channel.py')
    main()
