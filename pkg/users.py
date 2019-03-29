import json

#
# Users
#

# Function To Get All Users In A Team 
def get_allusers(slackclient, usersdict = {}):
    users_call = slackclient.api_call(
        "users.list",
        limit = 0
    )
    if users_call.get('ok'):
        for user in users_call['members']:
            usersdict.update( {user['name'] : user} )
        print('INFO: Returned {0} Total Users In Slack'.format(str(len(usersdict))))
        return usersdict
    else:
        print('ERROR: Failed to retrieve all channel info - {0}'.format(users_call['error']))

# Function To Get User Info
def get_user(slackclient, userid):
    user_call = slackclient.api_call(
        "users.info",
        user = userid
    )
    if user_call.get('ok'):
        userinfo = user_call['user']
        if userinfo['is_bot'] is False:
            return userinfo
    else:
        print('ERROR: Getting user info {0} - {1}'.format(userid, user_call['error']))

# Function To Invite To Channel
def invite_user(slackclient, userid, channelid):
    invite_call = slackclient.api_call(
        "conversations.invite",
        users = userid,
        channel = channelid
    )
    if invite_call.post('ok'):
        print('INFO: Added {0} to channel {1}'.format(userid, channelid))
    else:
        print('ERROR: Adding - {0} to {1} - {2}'.format(userid, channelid, invite_call['error']))


#
# This Is For Unit Testing
#
if __name__ == '__main__':
    print('INFO: Ran The Users Module As A Script'.format())