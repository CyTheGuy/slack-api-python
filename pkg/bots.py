


#
# Bots
#

# Function To Get Bot Info
def get_bot(slackclient, botid):
    bot_call = slackclient.api_call(
        "bots.info",
        bot = botid
    )
    if bot_call.get('ok'):
        botinfo = bot_call['bot']
        return botinfo
    else:
        print('ERROR: Getting bot info {0} - {1}'.format (botid, bot_call['error']))


#
# This Is For Unit Testing
#
if __name__ == '__main__':
    print('INFO: Ran The Bots Module As A Script'.format())