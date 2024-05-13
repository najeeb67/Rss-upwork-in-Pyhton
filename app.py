import feedparser
from datetime import datetime, timedelta
from win10toast import ToastNotifier
from flask import Flask, render_template
from flask_socketio import SocketIO
import sys

app = Flask(__name__)
socketio = SocketIO(app)

Rss_Notificaation =  ToastNotifier()

RSS_url = "https://www.upwork.com/ab/feed/jobs/rss?paging=0-10&q=react&sort=recency&api_params=1&securityToken=073a50eb2fb6ed496cf838810a0be7818cce3a0fe2575d1aa678faeb28ed753c12fa6e4cf20e774bdb02bb9e248b7dc11c1770c2bdba64bd68bf786bba3132fd&userUid=1638833218228867072&orgUid=1638833218228867073"
RSS_url = "https://www.upwork.com/ab/feed/jobs/rss?paging=0-10&q=python&sort=recency&api_params=1&securityToken=073a50eb2fb6ed496cf838810a0be7818cce3a0fe2575d1aa678faeb28ed753c12fa6e4cf20e774bdb02bb9e248b7dc11c1770c2bdba64bd68bf786bba3132fd&userUid=1638833218228867072&orgUid=1638833218228867073"
Rss_File = "File.txt"



def fetch_url(url, count=10):

    url += f"&paging=0-{count}"
    return feedparser.parse(url)

def get_title():
    try:
        with open(Rss_File, 'r') as file:
            return file.read().strip()
    except FileNotFoundError:
        return None

def set_title(title):
    with open(Rss_File, 'w', encoding="utf-8") as file:
        file.write(title)
  

def check_feed(feed):
    new_entries = []
    new_get_titles = get_title()
    curret_time = datetime.now()
    latest_entry = feed.entries[0] if feed.entries else None
    if latest_entry and latest_entry.title != new_get_titles:
        new_entries.append({
            'title': latest_entry.title,
            'link':latest_entry.link,
            'published': latest_entry.published,
        })
        set_title(latest_entry.title)
        encoded_title = latest_entry.title.encode(sys.stdout.encoding, errors='replace')
        Rss_Notificaation.show_toast("Upwork Notification", encoded_title.decode(sys.stdout.encoding), duration=5)

    for entry in feed.entries:
        entry_time = datetime.strptime(entry.published,'%a, %d %b %Y %H:%M:%S %z')
        entry_time = entry_time.replace(tzinfo=None) 
        if curret_time - entry_time < timedelta(days=1):
            new_entries.append({
                'title': entry.title,
                'link':entry.link,
                'published': entry.published,
            })
    return new_entries



@app.route('/')
def index():
    recent_feed = fetch_url(RSS_url)
    all_entries = check_feed(recent_feed)
    
    previous_feed = fetch_url(RSS_url, count=500)
    previous_entries = check_feed(previous_feed)
    
    return render_template("index.html", all_entries=all_entries, previous_entries=previous_entries)


@socketio.on('connect')
def connect():
    print("client connected")

def main():
    socketio.run(app, debug=True)

if __name__ == "__main__":
    main()


