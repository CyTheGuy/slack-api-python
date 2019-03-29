import json

#
# User Groups
#

def get_usergroups(slackclient):
    groups_call = slackclient.api_call(
        "usergroups.list",
        include_count = True,
        include_disabled = False,
        include_users = False
    )
    if groups_call['ok'] is True:
        for group in groups_call['usergroups']:
            #print(json.dumps(group, sort_keys=True,indent=4, separators=(',', ': ')))
            print(json.dumps(group['name'], sort_keys=True,indent=4, separators=(',', ': ')))
    else:
        print('ERROR: Failed to pull all user groups - {1}'.format(groups_call['error']))


#
# This Is For Unit Testing
#
if __name__ == '__main__':
    print('INFO: Ran The User Groups Module As A Script'.format())