# Half Blood Bot 

This project creates a simple webserver to run a bot that makes comments on reddit posts. 

## About

Using the reddit api you can retrieve new comments that are made on a specific subreddit. In this case we are using the Harry Potter subreddit. 

Each comment is compared against a dictionary made up of phrases to which the bot will reply to. Example: "Lily Evans" Reply: "Always." If a match is found a comment will be made.  There are restrictions that stop the bot from commenting too frequently or commenting the same reply too frequently. 

The code for the bot is run on Replit, it will create a small flask webserver to keep the bot running at all times, however, if the URL for the sever is not visited every 2 hours then Replit will shut it down. To avoid this, UpTimeRobot is used to consistently visit the site. This needs to be done to avoid paying to keep the bot running 24/7. 

