from slackclient import SlackClient

#
# SCIM Functions
#

def deactivate_user(token, userid):
    slackclient = SlackClient(token)
    userinfo = get_user(slackclient, userid)
    headers = {
        'Authorization': 'Bearer {}' .format(token)
    }
    url = 'https://api.slack.com/scim/v1/Users/' + userid
    try:
        r = requests.delete(url, headers=headers)
        print('INFO: Deleted {0} - {1}'.format(userid, userinfo['name']))
    except requests.exceptions.HTTPError as err:
        print('ERROR: Deleting {0} / {1} - {2}'.format(userid, userinfo['name'], err))


#
# This Is For Unit Testing
#
if __name__ == '__main__':
    print('INFO: Ran The SCIM Module As A Script'.format())