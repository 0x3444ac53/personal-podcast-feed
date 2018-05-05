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
        self.gereate_feed()

    def gereate_feed(self):
        pubtime = datetime.datetime.now().strftime("%I:%M%p on %B %d, %Y")
        files = os.listdir('./')
        for i in files:
            if '.mp3' not in i:
                files.pop(files.index(i))
        with open('feed.rss', 'w') as f:
            f.truncate()
            f.write("""
                <?xml version="1.0" encoding="utf-8"?>
                <rss version="2.0" xmlns:itunes="http://www.itunes.com/DTDs/Podcast-1.0.dtd">

                <channel>
                <title> Tanners Podcast </title>
                <description> ???? </description>
                <itunes:author>Tanner Galyean </itunes:author>
                <link> http://104.131.56.81/ </link>
                <itunes:image href="podcast_logo_grey.png" />
                <pubDate> Sun, 09 Oct 2005 21:00:00 PST </pubDate>
                <language>en-us</language>
                <copyright> 1997 tanner galyean </copyright>
                    """)
            for i in files:
                f.write("""
                    <item>
                    <title> {} </title>
                    <description> A description of your podcast episode </description>
                    <itunes:author> Tanner Galyean </itunes:author>
                    <pubDate> {} </pubDate>
                    <enclosure url="http://104.131.56.81/" + {} length={} type="audio/mpeg" /> </item>
                    """.format(
                    i.strip('.mp3'), pubtime, i,
                    os.stat(i).st_size))
            f.write("</channel></rss>")


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
