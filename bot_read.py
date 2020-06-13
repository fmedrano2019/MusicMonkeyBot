import praw
import pdb
import re
import os

# Reddit API login
reddit = praw.Reddit("MusicMonkeyBot")

# To keep track of which comments it has responded to
if not os.path.isfile("comments_replied_to.txt"):
    comments_replied_to = []
else:
    with open("comments_replied_to.txt", "r") as f:
        comments_replied_to = f.read()
        comments_replied_to = comments_replied_to.split("\n")
        comments_replied_to = list(filter(None, comments_replied_to))

# Subreddit to browse
subreddit = reddit.subreddit("testingground4bots")

# Activation phrase
keyphrase = "!lyrics "


# Retrieves the song title from the given phrase
def get_song_title(phrase):
    if phrase.count('"') >= 2:
        return phrase[phrase.find('"') + 1:phrase.rfind('"')]
    else:
        print("The given phrase had an invalid amount of quotation marks to get the song title")
        return None


# Retrieves the artist name from the given phrase
def get_artist_name(phrase):
    if phrase.count('"') >= 2:
        name = phrase[phrase.rfind('"') + 1:]
        # If there's a space at the front of name
        if name[0] == " ":
            return name[1:]
        else:
            return name
    else:
        print("The given phrase had an invalid amount of quotation marks to get the artist name")
        return None


def append_to_reply_list(comment_to_append):
    comments_replied_to.append(comment_to_append.id)
    with open("comments_replied_to.txt", "w") as f:
        for comment_id in comments_replied_to:
            f.write(comment_id + "\n")


# Monitors the comment stream for activation phrase
for comment in subreddit.stream.comments():
    if comment.id not in comments_replied_to:
        if re.search(keyphrase, comment.body, re.IGNORECASE):
            # Removes the keyphrase from the line to get the title and artist
            compile_temp = re.compile(keyphrase, re.IGNORECASE)
            song_information_phrase = compile_temp.sub("", comment.body)
            print("Phrase received: " + song_information_phrase)

            # Gets the song title and artist name with their respective methods
            song_title = get_song_title(song_information_phrase)
            artist_name = get_artist_name(song_information_phrase)
            print("Song title gotten: " + str(song_title))
            print("Artist gotten: " + str(artist_name))

            # If there were no errors in the comment
            if song_title is not None and artist_name is not None:
                # Replies with the lyrics
                reply = '"' + song_title + '"' + " by " + artist_name + "\n\n[INSERT LYRICS HERE]"
            # If there were errors in the comment
            else:
                # Replies with an error message
                reply = "There was an error in your comment's formatting. Make sure there are quotations marks " \
                        "around ONLY the title and the artist name is directly afterwards. The keyphrase has to be " \
                        "called at the end of your comment. "

            # Sends the reply
            comment.reply(reply)
            print("Bot replied to: " + comment.author.name)
            print("Reply contents: \n" + reply)

            # To separate between responses
            print("-------------------------------------------")

            # Appends the comment ID to the comments_replied_to list
            append_to_reply_list(comment)
