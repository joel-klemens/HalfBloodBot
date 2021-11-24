import os
import praw
import csv
import time
from datetime import datetime
from replit import db
from keep_alive import keep_alive

# env variables to hide login info
reddit = praw.Reddit(
  client_id = os.environ['client_id'],
  password = os.environ['password'],
  username = os.environ['username'],
  client_secret = os.environ['client_secret'],
  user_agent = "<HalfBloodBot1.0>"
)

class myBot:
  def __init__(self, filename):
    self.reply_list = []

    # pull previous info from db 
    if len(db) == 0:
      with open(filename) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=",")
        for row in csv_reader:
          self.reply_list.append({
            'phrase': row[0], 
            'reply': row[1]
          })
      db['reply_list'] = self.reply_list
    else:
      print("Pulling from DB")
      self.reply_list = db['reply_list']
  
  def find_match(self, comment):
    # iterate through our replies and get back dictionary 
    # if the phrase is in the comment body then we will know a post needs to be made
    for i, dictionary in enumerate(self.reply_list):
            if dictionary['phrase'] in comment.body:
                if self.wait_period(i):
                    self.make_reply(i, comment)

  def wait_period(self, i):
    # check to see if we have recently posted (don't want to spam)
    dictionary = self.reply_list[i]
    if 'last_posted' not in dictionary.keys():
      # Means we have never posted on this previously
      return True
    else:
      # put the time in the db of when the last time this post was made 
      now = datetime.now()
      duration = now - datetime.fromtimestamp(dictionary['last_posted'])
      duration_seconds = duration.total_seconds()
      hours = divmod(duration_seconds, 3600)[0]
      # can repost every hour 
      if hours >= 1:
          return True
      else:
          print(f"Couldn't post {dictionary['phrase']} Cool Down time: {hours}")

    return False

  def make_reply(self, i, comment):
    dictionary = self.reply_list[i]
    try:
      # uncomment next line
      # comment.reply(dictionary['reply'])
      print(comment.body)
      print(dictionary['phrase'])
      print(dictionary['reply'])
      # This will put the bot to sleep after posting to avoid spam 
      # time.sleep(60 * 60 * 3)
    except Exception as e:
      print(e)

    now = datetime.now()
    self.reply_list[i]['last_posted'] = now.timestamp()
    db['reply_list'] = self.reply_list

# keep alive is going to act as a webserver using flask (make an app)
# we are also going to use a free service called UpTimeRobot to keep the webserver running as 
# replit will shut it down after 2 hours if the url is not visited 
# keep_alive()

bot = myBot("replies.csv")
subreddit = reddit.subreddit("harrypotter")
for comment in subreddit.stream.comments(skip_existing=True):
  print(comment.body)

