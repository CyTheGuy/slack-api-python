import json

def get_target_channels(allchannels, channelname, channeldict = {}):
    count = channelname.count("*")
    if count > 2:
        print('WARNING: Invalid wild card channel entry {0} - skipping it'.format(channelname))
        exit()
    elif count == 2:
        # If There Are Two * Then Grab Value Between Them And Find Channels Containing It
        parsedname = re.search("\*(.*?)\*", channelname).group(1)
        for k, v in allchannels.items():
            if parsedname in k:
                print('INFO: Found channel - {0} - matching {1}'.format(k, channelname))
                channeldict.update( {k : v} )
    elif channelname.startswith("*"):
        parsedname = channelname[1:]
        for k, v in allchannels.items():
            if k.endswith(parsedname):
                print('INFO: Found channel - {0} - matching {1}'.format(k, channelname))
                channeldict.update( {k : v} )
    elif channelname.endswith("*"):
        parsedname = channelname[:-1]
        for k, v in allchannels.items():
            if k.startswith(parsedname):
                print('INFO: Found channel - {0} - matching {1}'.format(k, channelname))
                channeldict.update( {k : v} )
    else:
        # If No * Then Return Specific Channel Info
        for k, v in allchannels.items():
            if k == channelname:
                print('INFO: Found channel - {0} - matching {1}'.format(k, channelname))
                channeldict.update( {k : v} )
    # Also Let Them Know If Channels Could Not Be Found
    if len(channeldict) == 0:
        print('WARNING: There are no channels matching or equal to - {0}'.format(channelname))
        exit()
    else:
        return channeldict

#
# Channel
#

# Function To List All Channels Specified In The Types
def get_channels(slackclient, channelsdict = {}, nextcursor = 1):
    if nextcursor is 1:
        channels_call = slackclient.api_call(
            "conversations.list",
            limit = 1000,
            types = "public_channel, private_channel",
            exclude_archived = "true"
        )
    else:
        channels_call = slackclient.api_call(
            "conversations.list",
            limit = 1000,
            types = "public_channel, private_channel",
            cursor = nextcursor,
            exclude_archived = "true"
        )
    if channels_call.get('ok'):
        if nextcursor != 1:
            print('INFO: Retrieved page {0} of channels'.format(str(nextcursor)))
        else:
            print('INFO: Retrieved first page of channels')
        for channel in channels_call['channels']:
            # Uncomment this to print all info on the channel if you are curious about it
            #print(json.dumps(channel, sort_keys=True,indent=4, separators=(',', ': ')))
            # Uncomment this to print just channel name and ID
            #print(channel['name'] + " - " + channel['id'])
            channelsdict.update( {channel['name'] : channel} )
        metadata = channels_call['response_metadata']
        nextcursor = metadata['next_cursor']
        if nextcursor:
            return(get_channels(slackclient, channelsdict, nextcursor))
        else:
            print('INFO: Returned {0} total channels'.format(str(len(channelsdict))))
            return channelsdict
    else:
        print('ERROR: Failed to retrieve all channel info - {0}'.format(channels_call['error']))
        exit()

# Function To Search For A Specific Channel By Name
def get_channel(slackclient, channelname, nextcursor = 1):
    if nextcursor is 1:
        channels_call = slackclient.api_call(
            "conversations.list",
            limit = 1000,
            types = "public_channel, private_channel",
            exclude_archived = "true"
        )
    else:
        channels_call = slackclient.api_call(
            "conversations.list",
            limit = 1000,
            types = "public_channel, private_channel",
            cursor = nextcursor,
            exclude_archived = "true"
        )
    if channels_call.get('ok'):
        for channel in channels_call['channels']:
            channel_name = (channel['name'])
            if channelname == channel_name:
                print('INFO: Found {0} - {1}'.format(channel['name'], channel['id']))
                return channel
            else:
                metadata = channels_call['response_metadata']
                nextcursor = metadata['next_cursor']
                if nextcursor:
                    return(get_channel(slackclient, channelname, nextcursor))
    else:
        print('ERROR: Failed to retrieve channel info for {0} - {1}'.format(channelname, channels_call['error']))
    
# Function To Search For A Specific Channel By Id
def get_channelbyid(slackclient, channelid):
    channels_call = slackclient.api_call(
        "conversations.info",
        channel = channelid
    )
    if channels_call.get('ok'):
        print('INFO: Found {0}'.format(channelid))
        return channels_call['channel']
    else:
        print('ERROR: Failed to retrieve channel info for {0} - {1}'.format(channelid, channels_call['error']))

# Set Purpose Of A Channel
def set_channelpurpose(slackclient, channelinfo, channelpurpose):
    channelid = channelinfo['id']
    purpose_call = slackclient.api_call(
        "conversations.setPurpose",
        channel = channelid,
        purpose = channelpurpose
    )
    if purpose_call['ok']:
        print('INFO: Set {0} purpose to {1}'.format(channelinfo['name'], channelpurpose))
    else:
        print('ERROR: Failed to set channel purpose for {0} - {1}'.format(channelinfo['name'], purpose_call['error']))

# Archive A Channel
def archive_channel(slackclient, channelinfo):
    channelid = channelinfo['id']
    archive_call = slackclient.api_call(
        "conversations.archive",
        channel = channelid
    )
    if archive_call['ok']:
        print('INFO: Archived {0}'.format(channelinfo['name']))
    else:
        print('ERROR: Failed to archive {0} - {1}'.format(channelinfo['name'], archive_call['error']))
        if archive_call['error'] == "ratelimited":
            # If Rate Limited Sleep
            print('WARNING: Rate limited, sleeping for 90 seconds')
            time.sleep(90)
            return(archive_channel(slackclient, channelinfo))
        else:
            exit()

# Function To Search Channel History
def get_channelhistory(slackclient, channelinfo, getlatestonly = False, oldest = 0, messagedict = {}, nextcursor = 1):
    channelid = channelinfo['id']
    if getlatestonly == True:
        search_call = slackclient.api_call(
            "conversations.history",
            limit = 1,
            channel = channelid
        )
    elif nextcursor is 1:
        search_call = slackclient.api_call(
            "conversations.history",
            limit = 100,
            oldest = oldest,
            channel = channelid
        )
    else:
        search_call = slackclient.api_call(
            "conversations.history",
            limit = 100,
            channel = channelid,
            oldest = oldest,
            cursor = nextcursor
        )
    if search_call.get('ok'):
        # For Debugging
        #print(json.dumps(search_call, sort_keys=True,indent=4, separators=(',', ': ')))
        if len(search_call['messages']) == 0:
            print('WARNING: {0} has no messages in the range you specified'.format(channelinfo['name']))
            return None
        else:
            for message in search_call['messages']:
                if getlatestonly == True:
                    # For Debugging
                    #print(message['text'])
                    return message
                else:
                    # For Debugging
                    #print(message['text'])
                    messagedict.update( {message['ts'] : message} )
            if search_call['has_more'] == True:
                metadata = search_call['response_metadata']
                nextcursor = metadata['next_cursor']
                print('INFO: Retrieving page {0} of channel history'.format(nextcursor))
                return(get_channelhistory(slackclient, channelinfo, getlatestonly, oldest, messagedict, nextcursor))
            else:
                return messagedict
    else:
        print('ERROR: Failed to retrieve channel history for {0} - {1}'.format(channelinfo['name'], search_call['error']))
        if search_call['error'] == "ratelimited":
            # If Rate Limited Sleep
            print('WARNING: Rate limited, sleeping for 90 seconds')
            time.sleep(90)
            return(get_channelhistory(slackclient, channelinfo, getlatestonly, oldest, messagedict, nextcursor))
        else:
            exit()

# Function To Join Channel
# Note: If the channel does not exist, it is created!!
# WIP SHOULD CONVERT TO https://api.slack.com/methods/conversations.join
def join_channel(slackclient, channel_name):
    join_call = slackclient.api_call(
        "channels.join",
        name = channel_name
    )
    if join_call['ok'] is True:
        print('INFO: Added yourself to {0}'.format(channel_name))
    else:
        print('ERROR: Failed to add you to {0} - {1}'.format(channel_name, join_call['error']))

def create_channel(slackclient, channel_name, private = False):
    create_call = slackclient.api_call(
        "conversations.create",
        name = channel_name,
        is_private = private
    )
    if create_call['ok'] is True:
        print('INFO: Created {0}'.format(channel_name))
    else:
        print('ERROR: Failed to create {0} - {1}'.format(channel_name, create_call['error']))

#
# Members
#

# Function To Get Members Of A Channel
def get_members(slackclient, channelinfo, memberdict = {}, nextcursor = 1):
    channelid = channelinfo['id']
    if nextcursor is 1:
        members_call = slackclient.api_call(
            "conversations.members",
            channel = channelid,
            limit = 1000
        )
    else:
        members_call = slackclient.api_call(
            "conversations.members",
            channel = channelid,
            limit = 1000,
            cursor = nextcursor   
        )
    if members_call.get('ok'):
        for member in members_call['members']:
            memberdict.update( {member : member} )
        metadata = members_call['response_metadata']
        nextcursor = metadata['next_cursor']
        if nextcursor:
            return(get_members(slackclient, channelinfo, memberdict, nextcursor))
        else:
            #print('INFO: Returned {0} total members'.format(str(len(memberdict))))
            return memberdict
    else:
        print('ERROR: Pulling list of members for {0} - {1}'.format(channelid, members_call['error']))


#
# This Is For Unit Testing
#
if __name__ == '__main__':
    print('INFO: Ran The Channels Module As A Script'.format())