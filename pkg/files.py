

#
# Files
#

# Function To List All Files, All In A Channel, Or All Created By A User
def list_files(slackclient, fileslist, channelid = None, userid = None, page = 1):
    if (channelid is None) and (userid is None):
        print('INFO: Returning all files - page {0}'.format(str(page)))
        files_call = slackclient.api_call(
            "files.list",
            count = 200,
            page = page
        )
    if channelid:
        print('INFO: Returning all files for channelid - {0} - page {1}'.format(channelid, str(page)))
        files_call = slackclient.api_call(
            "files.list",
            count = 200,
            channel = channelid,
            page = page
        )
    if userid:
        print('INFO: Returning all files for userid - {0} - page {1}'.format(userid, str(page)))
        files_call = slackclient.api_call(
            "files.list",
            count = 200,
            user = userid,
            page = page
        )
    if files_call.get('ok'):
        if files_call['files']:
            for f in files_call['files']:
                #print(json.dumps(f['name'] + " - " + f['id'], sort_keys=True,indent=4, separators=(',', ': ')))
                if f['name'] in fileslist:
                    delete_file(slackclient, f['id'])
            paging = files_call['paging']
            page_current = paging['page']
            pages_total = paging['pages']
            if page_current < pages_total:
                page += 1
                list_files(slackclient, fileslist, channelid = channelid, userid = userid, page = page)
        else:
            if channelid:
                print('INFO: Channel - {0} - has no files in it or has returned all its files'.format(channelid))
            if userid:
                print('INFO: User - {0} - has no files or has returned all its files'.format(userid))
    else:
        print('ERROR: Retrieving files - {0}'.format(files_call['error']))

# Function To Get A Files Info
def get_file(slackclient, fileid):
    file_info = slackclient.api_call(
        "files.info",
        file = fileid
    )
    if file_info.get('ok'):
        return file_info['file']
    else:
        print('ERROR: Finding - {0} - {1}'.format(fileid, file_info['error']))
        return 1
        

# Function To Delete A File
def delete_file(slackclient, fileid):
    fileinfo = get_file(slackclient, fileid)
    if fileinfo is not 1:
        file_delete = slackclient.api_call(
            "files.delete",
            file = fileid
        )
        if file_delete.get('ok'):
            print('INFO: Successfully deleted {0} - {1}'.format(fileid, fileinfo['name']))
        else:
            print('ERROR: Deleting -  {0} - {1}'.format(fileid, file_delete['error']))


#
# This Is For Unit Testing
#
if __name__ == '__main__':
    print('INFO: Ran The Files Module As A Script'.format())