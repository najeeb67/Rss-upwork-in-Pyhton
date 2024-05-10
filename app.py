import feedparser
import time
from flask import Flask, render_template
from flask_socketio import SocketIO
import requests

app = Flask(__name__)
socketio = SocketIO(app)

RSS_url = "https://www.upwork.com/ab/feed/jobs/rss?paging=0-10&q=react&sort=recency&api_params=1&securityToken=073a50eb2fb6ed496cf838810a0be7818cce3a0fe2575d1aa678faeb28ed753c12fa6e4cf20e774bdb02bb9e248b7dc11c1770c2bdba64bd68bf786bba3132fd&userUid=1638833218228867072&orgUid=1638833218228867073"
RSS_url = "https://www.upwork.com/ab/feed/jobs/rss?paging=0-10&q=python&sort=recency&api_params=1&securityToken=073a50eb2fb6ed496cf838810a0be7818cce3a0fe2575d1aa678faeb28ed753c12fa6e4cf20e774bdb02bb9e248b7dc11c1770c2bdba64bd68bf786bba3132fd&userUid=1638833218228867072&orgUid=1638833218228867073"
Rss_File = "File.txt"




def fetch_url(url):

    return feedparser.parse(url)

def get_title():
    try:
        with open(Rss_File, 'r') as file:
            return file.read().strip()
    except FileNotFoundError:
        return None

def set_title(title):
    with open(Rss_File, 'w') as file:
        file.write(title)

def check_feed(feed):
    new_entries = []
    new_get_titles = get_title()
    for entry in reversed(feed.entries):
        print(entry)
        if entry.title == new_get_titles:
            break
        new_entries.append({
            'title': entry.title,
            'link': entry.link,
            'published': entry.published
        })
    if feed.entries:
        set_title(feed.entries[0].title)
    print(new_entries)
    return new_entries[::-1]

@app.route('/')
def index():
    feed = fetch_url(RSS_url)
    all_entries = check_feed(feed) 
    return render_template("index.html", all_entries=all_entries)
  


@socketio.on('connect')
def connect():
    print("client connected")

def main():
    socketio.run(app, debug=True)

if __name__ == "__main__":
    main()
