# slack-dataspill
This is the code for slack data spills

Requirements:
- python - pip install -U pip
- slackclient - pip install slackclient

Process:

- List All Channels - Private Channels Do Not Show Up In List And Doesn't Seem Like You Can Join Them With API
- Find Channel ID's From All Channel List Based On Channel Names You Supply
- ~~Join Channel On Channel Name~~ - Cannot Join Private Channels Programmatically Or Without An Invite :( 
- Find Files In Channel Based On Channel ID
- Find Files To Purge Based On Name And Get ID
- Purge Files Based On ID
- ~~Leave Channel On Channel Name~~

References:
- https://github.com/slackapi/python-slackclient
- https://api.slack.com/methods
- https://api.slack.com/custom-integrations/legacy-tokens