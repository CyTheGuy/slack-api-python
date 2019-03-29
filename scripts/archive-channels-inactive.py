# This scripts prunes channels that have no activity in the last 3 months. It sends a warning/reminder after 60 days of inactivity/30 days before archive.

import os
import sys
from datetime import datetime, timedelta
from slackclient import SlackClient

# Get Modules In pkg Folder
sys.path.append(os.getcwd()) 
from pkg import users, common, channels, messages

#
# Constants
#
slack_yml = common.import_yaml('./secrets/slack-automation.yml')
slack_client = SlackClient(slack_yml['token'])
exceptions = common.import_yaml('./scripts/archive-channels-inactive.yml')
ninety_days_ago = common.get_timediff(90)          # Get Timestamp For 90 Days Ago
unix_ts = common.get_unixtime(ninety_days_ago)     # Convert To Unix Time Cuz That Us What Slack Uses

#
# Variables
#
archive_message = "Hello quiet channel,\n\n We tend the channel garden by pinging channels that have been quiet for 60 straight days and archiving them after 90 days. Archiving a channel removes it from the list of active channels and prevents new comments from being made here. This makes it easier for newer folks to find the right channels to get their questions, answers, and comments heard without wading through extraneous channels.\n\n All existing comments in the channel are retained for easy browsing and everything can be read like any other channel. If a need for this channel arises again, it can be unarchived by clicking Channel Settings --> Unarchive.\n\n If you'd like to keep this channel active then post in the channel and the inactivity timer will be reset. It's that simple. If there are no new comments in the next 30 days then this channel will be archived."
to_archive_dict = {}
to_message_dict = {}

#
# The Fun Stuff
#
def main():
    all_channels = channels.get_channels(slack_client)
    public_channels = {k:v for (k,v) in all_channels.items() if v['is_private'] == False and v['is_archived'] == False}
    for k, v in public_channels.items():
        # If Channel Name In Exceptions List Skip It
        if k in exceptions['channels']:
            print('WARNING: {0} is in the exceptions list - skipping it'.format(k.encode('utf-8')))
            continue
        # Get Latest Message From Channel
        latest_message = channels.get_channelhistory(slack_client, v, True)
        try: # Get Readable Time Stamp Of Latest Message & Calculate Time Difference
            time_diff = datetime.now() - common.get_readabletime(latest_message['ts'])
        except Exception as e:
            print('WARNING: Failed to get last message time diff for {0} - {1}'.format(k.encode('utf-8'), str(e)))
            continue
        try: # See If Last Message Contains Username Value - username Is Only Included For Bot Messages
            user_name = latest_message['username']
        except:
            user_name = None
        # Archive Channel If Last Message In Channel Was The archive_message Sent By ArchiveBot & It Has Been 30 Days 
        if time_diff.days > 30 and latest_message['text'].startswith("Hey very quiet channel,") and user_name == "ArchiveBot":
            print('INFO: {0} has no activity since the archive warning was sent, adding to archive_dict'.format(k.encode('utf-8')))
            to_archive_dict.update( {k : v} )
        # Message 60 Day Inactive Channel With archive_message About How In 30 Days It Will Be Archived If There Is Still No Activity
        elif time_diff.days > 60: 
            print('INFO: {0} has no activity within the last 60 days, adding to message_dict'.format(k.encode('utf-8')))
            to_message_dict.update( {k : v} )
    # Action On Various Dictionaries
    print('INFO: Total Inactive Channels To Archive = {0} - But Only Targetting 3'.format(str(len(to_archive_dict))))
    for k in sorted(to_archive_dict)[:3]:
        #print('INFO: {0} has no activity within the last 30 days since the notification - would have archived it'.format(k))
        channels.archive_channel(slack_client, to_archive_dict[k])
    print('INFO: Total Inactive Channels To Message = {0} - But Only Targetting 3'.format(str(len(to_message_dict))))
    for k in sorted(to_message_dict)[:3]:
        #print('INFO: Would have messaged {0}'.format(k))
        messages.create_message(slack_client, to_message_dict[k], archive_message)
    print('INFO: End Of Script')

if __name__ == '__main__':
    print('INFO: Running archive-channels-inactive.py')
    main()