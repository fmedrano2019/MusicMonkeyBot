import praw
import pdb
import re
import os

# Reddit API login
reddit = praw.Reddit("MusicMonkeyBot")

# To keep track of which comments it has responded to
if not os.path.isfile("comments_replied_to.txt"):
    comments_replied_to = []
elsimport praw
import pdb
import re
import os
import requests
from bs4 import BeautifulSoup

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


# Appends the comment to comments_replied_to.txt
def append_to_reply_list(comment_to_append):
    comments_replied_to.append(comment_to_append.id)
    with open("comments_replied_to.txt", "w") as f:
        for comment_id in comments_replied_to:
            f.write(comment_id + "\n")


# Requests song information from Genius based on the given song title and artist name
def request_song_info(song_title, artist_name):
    base_url = "https://api.genius.com"
    headers = {"Authorization": "Bearer " + "[INSERT ACCESS TOKEN HERE]"}
    search_url = base_url + "/search"
    data = {'q': song_title + ' ' + artist_name}
    response = requests.get(search_url, data=data, headers=headers)

    return response


# Retrieves the lyrics from the given URL
def scrap_song_url(url):
    page = requests.get(url)
    html = BeautifulSoup(page.text, 'html.parser')
    lyrics = html.find('div', class_='lyrics').get_text()

    return lyrics


# Retrieves the lyrics from Genius
def extract_lyrics(song_title, artist_name):
    response = request_song_info(song_title, artist_name)
    json = response.json()
    remote_song_info = None

    for hit in json['response']['hits']:
        if artist_name.lower() in hit['result']['primary_artist']['name'].lower():
            remote_song_info = hit
            break

    if remote_song_info:
        song_url = remote_song_info['result']['url']
        print("Song URL: " + song_url)
    else:
        print("No hits were found")
        return None

    lyrics = scrap_song_url(song_url)
    lyrics_fixed = lyrics.replace("\n", "  \n")

    return lyrics_fixed


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
                reply_header = '"' + song_title + '"' + " by " + artist_name
                lyrics = extract_lyrics(song_title, artist_name)
                if lyrics is not None:
                    reply = reply_header + "\n\n" + lyrics
                else:
                    reply = "No results were found :(  \nMake sure the song title and artist name are accurate"
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
e:
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
