import praw
import pdb
import re
import os

reddit = praw.Reddit("MusicMonkeyBot")

if not os.path.isfile("posts_replied_to.txt"):
    posts_replied_to = []
else:
    with open("posts_replied_to.txt", "r") as f:
        posts_replied_to = f.read()
        posts_replied_to = posts_replied_to.split("\n")
        posts_replied_to = list(filter(None, posts_replied_to))

subreddit = reddit.subreddit("testingground4bots")

for submission in subreddit.stream.submissions():
    if submission.id not in posts_replied_to:
        if re.search("lyrics", submission.title, re.IGNORECASE):
            submission.reply("They are coming soon asshole")
            print("Bot replied to: " + submission.title)
            posts_replied_to.append(submission.id)
            with open("posts_replied_to.txt", "w") as f:
                for post_id in posts_replied_to:
                    f.write(post_id + "\n")
