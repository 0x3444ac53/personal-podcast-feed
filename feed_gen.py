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
                    <enclosure url="http://104.131.56.81/{}" length={} type="audio/mpeg" /> </item>
                    """.format(
                i.strip('.mp3'), pubtime, i,
                os.stat(i).st_size))
        f.write("</channel></rss>")
