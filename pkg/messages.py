


#
# Messages
#

# Deletes A Message
def delete_message(slackclient, channelinfo, messageinfo):
    timestamp = messageinfo['ts']
    channelid = channelinfo['id']
    delete_call = slackclient.api_call(
        "chat.delete",
        channel = channelid,
        ts = timestamp
    )
    if delete_call['ok']:
        print('INFO: Deleted {0} - {1} - from {2}'.format(timestamp, messageinfo['text'], channelinfo['name']))
    else:
        print('ERROR: Failed to delete {0} from {1} - {2}'.format(timestamp, channelinfo['name'], delete_call['error']))

# Creates A Message
def create_message(slackclient, channelinfo, message, asuser = False, verbose = False):
    channelid = channelinfo['id']
    create_call = slackclient.api_call(
        "chat.postMessage",
        channel = channelid,
        text = message,
        as_user = asuser
    )
    if create_call['ok']:
        if verbose == True:
            print('INFO: Posted {0} to {1}'.format(message, channelinfo['name']))
        else:
            print('INFO: Posted message to {0}'.format(channelinfo['name']))
    else:
        print('ERROR: Posting a message about 0 members to {0} - {1}'.format(channelinfo['name'], create_call['error']))
        return 1


#
# This Is For Unit Testing
#
if __name__ == '__main__':
    print('INFO: Ran The Messages Module As A Script'.format())