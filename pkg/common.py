import os
import sys
import json
import yaml
import time
import smtplib
from email.mime.text import MIMEText
from datetime import datetime, timedelta

#
# Read File Functions
#

# Check If File Exists
def check_path(path):
    if os.path.isfile(path) != True:
        print('WARNING: {0} does not exist, creating it'.format(path))
        file = open(path, "w+")

# Read In File
def read_file(file_list):
    with open(file_list, "r") as file:
        objects = file.read().splitlines()
    if len(objects) != 0:
        return objects
    else:
        print('ERROR: You need to add something to {0}'.format(str(file_list)))
        exit()

def import_json(file):
    with open(file) as json_data:
        return json.load(json_data)

def import_yaml(file):
    with open(file) as yaml_data:
        return yaml.safe_load(yaml_data)


#
# Time Functions
#

# Convert Unix Timestamp To Readable Time
def get_readabletime(ts):
    try:
        return datetime.utcfromtimestamp(float(ts))
    except Exception as e:
        print('ERROR: Failed to convert {0} to readable time - {1}'.format(ts, str(e)))
        exit()

# Convert Readable Time To Unix Timestamp
def get_unixtime(ts):
    try:
        return time.mktime(ts.timetuple())
    except Exception as e:
        print('ERROR: Failed to convert {0} to unix time - {1}'.format(ts, str(e)))
        exit()

# Get Difference In Time Between Now And Days
def get_timediff(days):
    try:
        return datetime.now() - timedelta(days)
    except Exception as e:
        print('ERROR: Failed to get time diff - {0}'.format(str(e)))
        exit()

#
# Email Functions
#

# Send Email
def send_email(fromaddress, toaddress, subject, contents, smtp, text = ''):
    # Converts The Dict To A List For Sorting
    contents = sorted(contents)
    for k in contents:
        text += '{0}\n'.format(k)

    msg = MIMEText(text)
    msg['Subject'] = subject
    msg['From'] = fromaddress
    msg['To'] = toaddress

    s = smtplib.SMTP(smtp)
    s.sendmail(fromaddress, toaddress, msg.as_string())
    s.quit()


#
# This Is For Unit Testing
#
if __name__ == '__main__':
    print('INFO: Ran The Common Functions Module As A Script'.format())