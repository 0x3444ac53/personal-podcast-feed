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
import feed_gen

class StdOutListener(StreamListener):
    """ A listener handles tweets that are received from the stream.
    This is a basic listener that just prints received tweets to stdout.
    """

    def on_data(self, data):
        d = json.loads(data)
        print(d["text"] + '\n')
        url_list = d["text"].split()
        url_string = url_list[1]
        self.download_aud(url_string)
        return True

    def on_direct_message(self, data):
        print(data)

    def on_error(self, status):
        print(status)

    def download_aud(self, urll):
        ydl_opts = {
            'format':
            'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
        }
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            ydl.download([urll])
        feed_gen.generate_feed()


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
