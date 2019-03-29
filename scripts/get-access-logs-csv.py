# This script is used to retrieve the "access logs" for users on a workspace. 
# Each access log entry represents a user accessing Slack from a specific user, IP address, and user agent combination.

import os
import sys
import csv
import json
from slackclient import SlackClient

# Get Modules In pkg Folder
sys.path.append(os.getcwd()) 
from pkg import accesslogs, common

#
# Constants
#
slack_yml = common.import_yaml('./secrets/slack-automation.yml')
slack_client = SlackClient(slack_yml['token']) 
text = '"count", "country", "date_first", "date_last", "ip", "isp", "region", "user_agent", "user_id", "username"'

#
# The Fun Stuff
#
if __name__ == '__main__':
    access_logs = accesslogs.get_accesslogs(slack_client, 8)
    common.check_path("./outputs/access_logs.csv")
    # Write The Data To File
    access_csv = csv.writer(open("./outputs/access_logs.csv", "w+"))
    # Write CSV Header, If you dont need that, remove this line
    access_csv.writerow(["count", "country", "date_first", "date_last", "ip", "isp", "region", "user_agent", "user_id", "username"])
    for x in access_logs:
        date_first = common.get_readabletime(x["date_first"])
        date_last = common.get_readabletime(x["date_last"])
        parsed_agent = accesslogs.parse_user_agent(x["user_agent"])
        access_csv.writerow([x["count"],
                    x["country"],
                    date_first,
                    date_last,
                    x["ip"],
                    x["isp"],
                    x["region"],
                    parsed_agent,
                    x["user_id"],
                    x["username"]])
    with open('./outputs/access_logs.csv', mode='r') as infile:
        reader = csv.reader(infile)
    print('INFO: End of script')