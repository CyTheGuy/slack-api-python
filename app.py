import os
from slackclient import SlackClient

# Get The Envrionmental Variable Set For Token And Instantiate The SlackClient Helper Library
SLACK_TOKEN = os.environ.get('SLACK_TOKEN')
slack_client = SlackClient(SLACK_TOKEN)

#
# Functions
#

# Function To List All Channels
def list_channels():
    channels_call = slack_client.api_call("channels.list")
    if channels_call.get('ok'):
        return channels_call['channels']
    return None

# Function To Get Channel Info
def info_channel(channelid):
    channel_info = slack_client.api_call(
        "channels.info",
        channel=channelid
    )
    if channel_info.get('ok'):
        return channel_info['channel']
    return None

# Function To Join Channel
def join_channel(channelname):
    channel_join = slack_client.api_call(
        "channels.join",
        name=channelname
    )
    if channel_join.get('ok'):
        print("Successfully joined " + channelname)
        return channel_join['channel']
    return None

# Function To List Files In A Channel
def list_files(channelid):
    files_call = slack_client.api_call(
        "files.list",
        channel=channelid
    )
    if files_call.get('ok'):
        return files_call['files']
    return None

# Function To Delete Files
def delete_file(fileid, filename, channelname):
    file_delete = slack_client.api_call(
        "files.delete",
        file=fileid
    )
    if file_delete.get('ok'):
        print("         Successfully deleted " + filename + " from " + channelname)
    return None

# Function To Get User Info
def info_user(userid):
    user_info = slack_client.api_call(
        "users.info",
        user=userid
    )
    if user_info.get('ok'):
        return user_info['user']
    return None

#
# Variables
#

channels_list = ['cytest','cytest2','cytest3','cytest4']
files_list = ['Test.txt','Test1.txt','Test2.txt','Test3.txt','Test4.txt']

#
# The Fun Stuff
#

# Gets List Of Channels > Checks If It Is In Channels_List > Joins Channel > Checks If It Has Files In Files_List > Deletes File If It Is In List > Leave Channel
if __name__ == '__main__':
    print("WARNING: This Only Works With Public Channels, If One Of The Channels Is Private You Need To Be Invited To It First")
    channels = list_channels()
    if channels:
        for c in channels:
            if c['name'] in channels_list:
                files = list_files(c['id'])
                if files:
                    print("Channel: " + c['name'] + " Is In channel_list And Has Files")
                    print("   ## Name, File Owner, FileType ##")
                    for f in files:
                        if f['name'] in files_list:
                            fileownerinfo = info_user(f['user'])
                            fileownername = fileownerinfo['name']
                            print("   " + f['name'] + ", " + fileownername + ", " + f['filetype'] + " - Is In file_list For Cleanup")
                            print("      Going To Purge " + f['name'] + " From " + c['name'])
                            delete_file(f['id'],f['name'],c['name'])
                else:
                    print("WARNING: NO FILES WERE FOUND IN CHANNEL " + c['name'])         
    else:
        print("Unable To Authenticate With API")