# slack-scripts

## Pre-requistes:

- **Python3, Pip, virtualenv**

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
