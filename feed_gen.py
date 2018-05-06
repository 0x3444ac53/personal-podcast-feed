import datetime
import os


def generate_feed():
    pubtime = datetime.datetime.now().strftime("%I:%M%p on %B %d, %Y")
    files = os.listdir('./')
    approved = ['.mp3']
    files[:] = [url for url in files if any(sub in url for sub in approved)]

    with open('feed.rss', 'w') as f:
        f.truncate()
        f.write("""<?xml version="1.0" encoding="utf-8"?>
<rss xmlns:dc="http://purl.org/dc/elements/1.1/" xmlns:content="http://purl.org/rss/1.0/modules/content/" xmlns:itunes="http://www.itunes.com/dtds/podcast-1.0.dtd" version="2.0">
  <channel>
    <title>Tanner's Podcast</title>
    <link>http://104.131.56.81/</link>
    <description>podcast</description>
     <itunes:summary />
     <itunes:subtitle />
    <itunes:category text=""></itunes:category>
    <language>en-us</language>
    <copyright>2006. All rights reserved.</copyright>
    <pubDate>Sat, 05 May 2018 23:34:57 GMT</pubDate>
    <lastBuildDate>Sat, 05 May 2018 23:34:57 GMT</lastBuildDate>
    <generator>Podcastblaster.com</generator>
    <managingEditor>sprinklelong@gmail.com(Tanner Galyean)</managingEditor>
    <webMaster>sprinklelong@gmail.com</webMaster>
    <image>
    <url>http://104.131.56.81/podcast_logo_grey.png</url>
    <title>Tanner's Podcast</title>
    <link>http://104.131.56.81/</link>
    <width>100</width>
    <height>100</height>
    </image>
    <itunes:owner>
      <itunes:name>Tanner Galyean</itunes:name>
      <itunes:email>sprinklelong@gmail.com</itunes:email>
    </itunes:owner>
    
    <itunes:author></itunes:author>
    <itunes:explicit>no</itunes:explicit>""")
        for i in files:
            f.write("""
                    <item>
                    <title> {} </title>
                    <description> A description of your podcast episode </description>
                    <itunes:author> Tanner Galyean </itunes:author>
                    <pubDate> {} </pubDate>
                    <enclosure url="http://104.131.56.81/{}" length={} type="audio/mpeg" /> </item>
                    """.format(
                i.strip('.mp3'), pubtime, i,
                os.stat(i).st_size))
        f.write("</channel></rss>")
