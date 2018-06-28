from __future__ import unicode_literals
from __future__ import absolute_import, print_function
import youtube_dl
# author=rhnvrm<hello@rohanverma.net>
import tweepy
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import json
import key
global api
import os
import datetime
import lone_feed_gen
import random
import string
import re
from urllib import parse


url_regex = re.compile('https?://+')

class StdOutListener(StreamListener):
    """ A listener handles tweets that are received from the stream.
    This is a basic listener that just prints received tweets to stdout.
    """

    def on_data(self, data):
        d = json.loads(data)
        print(d)
        tweett = d["text"].split(' ')
        link = tweett[1]
        tweett.pop(1)
        tweett.pop(0)
        screen_name = d['user']['screen_name']
        tweetId = d['id']
        title = ''
        for i in tweett:
            title += i+' '
        print(title)
        self.download_aud(link, title, screen_name, tweetId)
        return True

    def on_direct_message(self, data):
        print(data)

    def on_error(self, status):
        print(status)

    def download_aud(self, urll, title, screen_name, tweet_id):
        os.system('mkdir {}'.format(title.replace(' ', '\ ')))
        os.chdir(title)
        ydl_opts = {
            'format':
            'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
            'outtmpl': '%(playlist_index)s---%(title)s-%(id)s.%(ext)s'
        }
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            ydl.download([urll])
        os.chdir('../')
        file_string = lone_feed_gen.generate_feed(title).split('/')[1]
        os.chdir('../')
        self.reply(file_string, screen_name, tweet_id)

    def reply(self, file_string, screen_name, tweet_id):
        link_text = parse("http://sailor.pictures/{}".format(file_string))
        api.update_status("@{} {}".format(tweet_id, link_text), tweet_id)
        


def start():
    nolonger = StdOutListener()
    auth = OAuthHandler(key.consumer_key, key.consumer_secret)
    auth.set_access_token(key.access_token, key.access_token_secret)
    api = tweepy.API(auth)
    stream = Stream(auth, nolonger)
    # change filters to listen to various types of tweets
    # eg try 'coldplay', '@rhnvrm', '#ACMSNU' etc
    stream.filter(track=["#personal-feed"])


start()
