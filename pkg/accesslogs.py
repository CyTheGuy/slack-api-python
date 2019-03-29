

#
# Access Logs 
# 

# Get Team Access Logs
def get_accesslogs(slackclient, maxpages = 100, page = 1, accesslist = []):        
    team_info = slackclient.api_call(
        "team.accessLogs",
        before = "now",
        count = 1000,
        page = page
    )
    if team_info.get('ok'):
        paging = team_info['paging']
        page = paging['page']
        pages = paging['pages']
        print('INFO: Retrieved page {0} out of {1} of logs'.format(str(page), str(pages)))
        for logins in team_info['logins']:
            # WILL NEED TO CHANGE THIS SINCE USERNAME IS NOT UNIQUE CUZ THERE ARE MULTIPLE PLATFORMS
            #accessdict.update( {logins['username'] : logins} )
            # MAY WANT TO USE LIST INSTEAD OF DICT FOR THIS REASON SO IT DOES NOT OVERWRITE KEYS
            accesslist.append(logins)
        if page < maxpages:
            page += 1
            return(get_accesslogs(slackclient, maxpages, page, accesslist))
        else:
            return accesslist
    else:
        print('ERROR: Failed to retrieve access logs for page {0} - {1}'.format(str(page), team_info['error']))
        if team_info['error'] == "ratelimited":
            # If Rate Limited Sleep
            print('WARNING: Rate limited, sleeping for 90 seconds')
            time.sleep(90)
            return(get_accesslogs(slackclient, maxpages, page, accesslist))
        else:
            exit()
'''
# Get Team Access Logs
def get_accesslogs(slackclient, enddate, page = 1, accesslist = [], maxpages = 100):        
    team_info = slackclient.api_call(
        "team.accessLogs",
        before = "now",
        count = 1000,
        page = page
    )
    if team_info.get('ok'):
        paging = team_info['paging']
        page = paging['page']
        pages = paging['pages']
        print('INFO: Retrieved page {0} out of {1} of logs'.format(str(page), str(pages)))
        for logins in team_info['logins']:
            if logins['date_last'] > enddate:
                # WILL NEED TO CHANGE THIS SINCE USERNAME IS NOT UNIQUE CUZ THERE ARE MULTIPLE PLATFORMS
                # MAY WANT TO USE LIST INSTEAD OF DICT FOR THIS REASON SO IT DOES NOT OVERWRITE KEYS
                #accessdict.update( {logins['username'] : logins} )
                accesslist.append(logins)
            else:
                print('INFO: Reached targeted end date of logs - {0}'.format(str(enddate)))
                return accesslist
        if page < maxpages:
            page += 1
            return(get_accesslogs(slackclient, enddate, page, accesslist, maxpages))
        else:
            return accesslist
    else:
        print('ERROR: Failed to retrieve access logs for page {0} - {1}'.format(str(page), team_info['error']))
        if team_info['error'] == "ratelimited":
            # If Rate Limited Sleep
            print('WARNING: Rate limited, sleeping for 90 seconds')
            time.sleep(90)
            return(get_accesslogs(slackclient, enddate, page, accesslist, maxpages))
        else:
            exit()
'''

def parse_user_agent(agent):
    if "iPhone" in agent:
        parsed_agent = "iPhone"
    elif "SlackWeb" in agent:
        parsed_agent = "SlackWeb"
    elif "Android" in agent:
        parsed_agent = "Android"
    elif "ApiApp" in agent:
        parsed_agent = "ApiApp"
    elif "iPad" in agent:
        parsed_agent = "iPad"
    elif "Windows Phone" in agent:
        parsed_agent = "Windows Phone"
    else:
        #print('WARNING: Invalid agent type for {0}'.format(agent))
        parsed_agent = agent
    return parsed_agent

'''def parse_user_agent(agent):
    if "iPhone" in agent:
        parsed_agent = "iPhone"
    elif "SlackWeb" in agent:
        parsed_agent = "SlackWeb"
    elif "Google Pixel 2" in agent:
        parsed_agent = "Google Pixel 2"
    elif "samsung" in agent:
        parsed_agent = "Samsung"
    elif "Google Pixel 2" in agent:
        parsed_agent = "Google Pixel 2"
    elif "Google Pixel 2" in agent:
        parsed_agent = "Google Pixel 2"

    else:
        print("Invalid agent type for " + agent)
        #exit()
    return parsed_agent'''


#
# This Is For Unit Testing
#
if __name__ == '__main__':
    print('INFO: Ran The Access Logs Module As A Script'.format())