# slack-scripts
This is the code for slack related scripts. **If the channel is private you need to be invited to it**

If you get tickets asking for things you can track requests for scripts  and link the Jira ticket

Other [scripts]( https://github.palantir.build/collabtools/slack-tools)

## Pre-requistes:

- **Python 2.7, Pip, virtualenv**
- This [doc](https://rtfm.palantir.build/docs/docs-for-docs/master/python.html#docs4docs-python) is SUPER helpful for installing the pre-reqs and making sure things are ready to go smoothly with this script.

## Configure Your Envrionment:

1. Generate [Slack Legacy Token](https://api.slack.com/custom-integrations/legacy-tokens) and save it to .config/slack_token.txt
    - You will need to be a workspace admin to do this or you can use the existing 
2. Run setup.sh to run virtualenv and install the requirements. Then activate virtualenv:

   ```
   sh ./config/setup.sh
   source venv/bin/activate
   ```

## References:
- https://github.com/slackapi/python-slackclient
- https://api.slack.com/methods
- https://api.slack.com/custom-integrations/legacy-tokens
