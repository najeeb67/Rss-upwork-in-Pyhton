import feedparser
from datetime import datetime, timedelta
from win10toast import ToastNotifier
from flask import Flask, render_template
from flask_socketio import SocketIO
import sys

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app, cors_allowed_origins="*")


Rss_Notificaation =  ToastNotifier()

RSS_US_URL ="https://www.upwork.com/ab/feed/topics/rss?securityToken=81e2b4b45c1bf6ef8752e649541dc096c20e5256d9034c5b7b5898739550d9fb376ac7e6e4e9632b1f46b176ab780d4ebb09f44ae9b3e5ee6b505b0bbfe61d2a&userUid=1672273345003061248&orgUid=1672273345003061249&sort=local_jobs_on_top&topic=domestic"
RSS_react_url = "https://www.upwork.com/ab/feed/jobs/rss?location=Australia%2CCanada%2CChile%2CDenmark%2CFrance%2CGermany%2CItaly%2CNetherlands%2CNew%20Zealand%2CSaudi%20Arabia%2CSwitzerland%2CUnited%20Arab%20Emirates%2CUnited%20Kingdom%2CUnited%20States&paging=0-10&q=react.js%20NOT%20Expensify&sort=recency&api_params=1&securityToken=81e2b4b45c1bf6ef8752e649541dc096c20e5256d9034c5b7b5898739550d9fb376ac7e6e4e9632b1f46b176ab780d4ebb09f44ae9b3e5ee6b505b0bbfe61d2a&userUid=1672273345003061248&orgUid=1672273345003061249"
RSS_NODE_URL = "https://www.upwork.com/ab/feed/jobs/rss?location=Australia%2CCanada%2CChile%2CDenmark%2CFrance%2CGermany%2CItaly%2CNetherlands%2CNew%20Zealand%2CSaudi%20Arabia%2CSwitzerland%2CUnited%20Arab%20Emirates%2CUnited%20Kingdom%2CUnited%20States&paging=0-10&q=node%20NOT%20Expensify&sort=recency&api_params=1&securityToken=81e2b4b45c1bf6ef8752e649541dc096c20e5256d9034c5b7b5898739550d9fb376ac7e6e4e9632b1f46b176ab780d4ebb09f44ae9b3e5ee6b505b0bbfe61d2a&userUid=1672273345003061248&orgUid=1672273345003061249"
RSS_PHP_URL ="https://www.upwork.com/nx/search/jobs/?location=Australia,Canada,Chile,Denmark,France,Germany,Italy,Netherlands,New%20Zealand,Saudi%20Arabia,Switzerland,United%20Arab%20Emirates,United%20Kingdom,United%20States&q=php%20NOT%20india&sort=recency&verified_payment_only=1"
RSS_WORDPRESS = "https://www.upwork.com/ab/feed/jobs/rss?location=Australia%2CCanada%2CChile%2CDenmark%2CFrance%2CGermany%2CItaly%2CNetherlands%2CNew%20Zealand%2CSaudi%20Arabia%2CSwitzerland%2CUnited%20Arab%20Emirates%2CUnited%20Kingdom%2CUnited%20States&paging=0-10&q=wordpress%20NOT%20india&sort=recency&api_params=1&securityToken=81e2b4b45c1bf6ef8752e649541dc096c20e5256d9034c5b7b5898739550d9fb376ac7e6e4e9632b1f46b176ab780d4ebb09f44ae9b3e5ee6b505b0bbfe61d2a&userUid=1672273345003061248&orgUid=1672273345003061249"
RSS_QUICKBOOKS_URL="https://www.upwork.com/ab/feed/jobs/rss?location=Australia%2CCanada%2CChile%2CDenmark%2CFrance%2CGermany%2CItaly%2CNetherlands%2CNew%20Zealand%2CSaudi%20Arabia%2CSwitzerland%2CUnited%20Arab%20Emirates%2CUnited%20Kingdom%2CUnited%20States&paging=0-10&q=quickbooks&sort=recency&api_params=1&securityToken=81e2b4b45c1bf6ef8752e649541dc096c20e5256d9034c5b7b5898739550d9fb376ac7e6e4e9632b1f46b176ab780d4ebb09f44ae9b3e5ee6b505b0bbfe61d2a&userUid=1672273345003061248&orgUid=1672273345003061249"
RSS_SHOPIFY_URL = "https://www.upwork.com/ab/feed/jobs/rss?location=Australia%2CCanada%2CChile%2CDenmark%2CFrance%2CGermany%2CItaly%2CNetherlands%2CNew%20Zealand%2CSaudi%20Arabia%2CSwitzerland%2CUnited%20Arab%20Emirates%2CUnited%20Kingdom%2CUnited%20States&paging=0-10&q=shopify%20OR%20ecommerce&sort=recency&api_params=1&securityToken=81e2b4b45c1bf6ef8752e649541dc096c20e5256d9034c5b7b5898739550d9fb376ac7e6e4e9632b1f46b176ab780d4ebb09f44ae9b3e5ee6b505b0bbfe61d2a&userUid=1672273345003061248&orgUid=1672273345003061249"
RSS_API_INTEGRAGATION_URL ="https://www.upwork.com/ab/feed/jobs/rss?location=Australia%2CCanada%2CChile%2CDenmark%2CFrance%2CGermany%2CItaly%2CNetherlands%2CNew%20Zealand%2CSaudi%20Arabia%2CSwitzerland%2CUnited%20Arab%20Emirates%2CUnited%20Kingdom%2CUnited%20States&paging=0-10&q=api%20integration&sort=recency&api_params=1&securityToken=81e2b4b45c1bf6ef8752e649541dc096c20e5256d9034c5b7b5898739550d9fb376ac7e6e4e9632b1f46b176ab780d4ebb09f44ae9b3e5ee6b505b0bbfe61d2a&userUid=1672273345003061248&orgUid=1672273345003061249"
RSS_PAYMENT_GETWAY_URL ="https://www.upwork.com/ab/feed/jobs/rss?location=Australia%2CCanada%2CChile%2CDenmark%2CFrance%2CGermany%2CItaly%2CNetherlands%2CNew%20Zealand%2CSaudi%20Arabia%2CSwitzerland%2CUnited%20Arab%20Emirates%2CUnited%20Kingdom%2CUnited%20States&paging=0-10&q=payment%20gateway&sort=recency&api_params=1&securityToken=81e2b4b45c1bf6ef8752e649541dc096c20e5256d9034c5b7b5898739550d9fb376ac7e6e4e9632b1f46b176ab780d4ebb09f44ae9b3e5ee6b505b0bbfe61d2a&userUid=1672273345003061248&orgUid=1672273345003061249"
RSS_FULL_TIME_URL ="https://www.upwork.com/ab/feed/jobs/rss?location=Australia%2CCanada%2CChile%2CDenmark%2CFrance%2CGermany%2CItaly%2CNetherlands%2CNew%20Zealand%2CSaudi%20Arabia%2CSwitzerland%2CUnited%20Arab%20Emirates%2CUnited%20Kingdom%2CUnited%20States&paging=0-10&q=full%20time&sort=recency&api_params=1&securityToken=81e2b4b45c1bf6ef8752e649541dc096c20e5256d9034c5b7b5898739550d9fb376ac7e6e4e9632b1f46b176ab780d4ebb09f44ae9b3e5ee6b505b0bbfe61d2a&userUid=1672273345003061248&orgUid=1672273345003061249"
RSS_CHATBOT_URL = "https://www.upwork.com/ab/feed/jobs/rss?location=Australia%2CCanada%2CChile%2CDenmark%2CFrance%2CGermany%2CItaly%2CNetherlands%2CNew%20Zealand%2CSaudi%20Arabia%2CSwitzerland%2CUnited%20Arab%20Emirates%2CUnited%20Kingdom%2CUnited%20States&paging=0-10&q=chatbot&sort=recency&api_params=1&securityToken=81e2b4b45c1bf6ef8752e649541dc096c20e5256d9034c5b7b5898739550d9fb376ac7e6e4e9632b1f46b176ab780d4ebb09f44ae9b3e5ee6b505b0bbfe61d2a&userUid=1672273345003061248&orgUid=1672273345003061249"
RSS_SCRIPPTING_URL ="https://www.upwork.com/ab/feed/jobs/rss?location=Australia%2CCanada%2CChile%2CDenmark%2CFrance%2CGermany%2CItaly%2CNetherlands%2CNew%20Zealand%2CSaudi%20Arabia%2CSwitzerland%2CUnited%20Arab%20Emirates%2CUnited%20Kingdom%2CUnited%20States&paging=0-10&q=scripting%20OR%20automation&sort=recency&api_params=1&securityToken=81e2b4b45c1bf6ef8752e649541dc096c20e5256d9034c5b7b5898739550d9fb376ac7e6e4e9632b1f46b176ab780d4ebb09f44ae9b3e5ee6b505b0bbfe61d2a&userUid=1672273345003061248&orgUid=1672273345003061249"
RSS_BUBBLE_URL="https://www.upwork.com/ab/feed/jobs/rss?location=Australia%2CCanada%2CChile%2CDenmark%2CFrance%2CGermany%2CItaly%2CNetherlands%2CNew%20Zealand%2CSaudi%20Arabia%2CSwitzerland%2CUnited%20Arab%20Emirates%2CUnited%20Kingdom%2CUnited%20States&paging=0-10&q=bubble&sort=recency&api_params=1&securityToken=81e2b4b45c1bf6ef8752e649541dc096c20e5256d9034c5b7b5898739550d9fb376ac7e6e4e9632b1f46b176ab780d4ebb09f44ae9b3e5ee6b505b0bbfe61d2a&userUid=1672273345003061248&orgUid=1672273345003061249"
RSS_WEBRTC_URL="https://www.upwork.com/ab/feed/jobs/rss?location=Australia%2CCanada%2CChile%2CDenmark%2CFrance%2CGermany%2CItaly%2CNetherlands%2CNew%20Zealand%2CSaudi%20Arabia%2CSwitzerland%2CUnited%20Arab%20Emirates%2CUnited%20Kingdom%2CUnited%20States&paging=0-10&q=webrtc%20OR%20socket&sort=recency&api_params=1&securityToken=81e2b4b45c1bf6ef8752e649541dc096c20e5256d9034c5b7b5898739550d9fb376ac7e6e4e9632b1f46b176ab780d4ebb09f44ae9b3e5ee6b505b0bbfe61d2a&userUid=1672273345003061248&orgUid=1672273345003061249"
RSS_Pyhton_url = "https://www.upwork.com/ab/feed/jobs/rss?location=Australia%2CCanada%2CChile%2CDenmark%2CFrance%2CGermany%2CItaly%2CNetherlands%2CNew%20Zealand%2CSaudi%20Arabia%2CSwitzerland%2CUnited%20Arab%20Emirates%2CUnited%20Kingdom%2CUnited%20States&paging=0-10&q=python%20NOT%20india&sort=recency&api_params=1&securityToken=81e2b4b45c1bf6ef8752e649541dc096c20e5256d9034c5b7b5898739550d9fb376ac7e6e4e9632b1f46b176ab780d4ebb09f44ae9b3e5ee6b505b0bbfe61d2a&userUid=1672273345003061248&orgUid=1672273345003061249"
RSS_VUE_URL ="https://www.upwork.com/ab/feed/jobs/rss?location=Australia%2CCanada%2CChile%2CDenmark%2CFrance%2CGermany%2CItaly%2CNetherlands%2CNew%20Zealand%2CSaudi%20Arabia%2CSwitzerland%2CUnited%20Arab%20Emirates%2CUnited%20Kingdom%2CUnited%20States&paging=0-10&q=vue&sort=recency&api_params=1&securityToken=81e2b4b45c1bf6ef8752e649541dc096c20e5256d9034c5b7b5898739550d9fb376ac7e6e4e9632b1f46b176ab780d4ebb09f44ae9b3e5ee6b505b0bbfe61d2a&userUid=1672273345003061248&orgUid=1672273345003061249"

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


def latest_entry(feed):
    latest_entry = feed.entries[0] if feed.entries else None
    if latest_entry:
        return {
            'title': latest_entry.title,
            'link': latest_entry.link,
            'published': latest_entry.published,
        }
    else:
        return None



def check_feed(feed):
    new_entries = []
    latest = latest_entry(feed) 
    new_get_titles = get_title()
    current_time = datetime.now()

    if latest and latest['title'] != new_get_titles:  
        new_entries.append({
            'title': latest['title'],
            'link': latest['link'],
            'published': latest['published'],
        })
        set_title(latest['title'])
        encoded_title = latest['title'].encode(sys.stdout.encoding, errors='replace')
        # Rss_Notificaation.show_toast("Upwork Notification", encoded_title.decode(sys.stdout.encoding), duration=5)

    for entry in feed.entries:
        entry_time = datetime.strptime(entry.published, '%a, %d %b %Y %H:%M:%S %z')
        entry_time = entry_time.replace(tzinfo=None)
        if current_time - entry_time < timedelta(days=1):
            new_entries.append({
                'title': entry.title,
                'link': entry.link,
                'published': entry.published,
            })
    return new_entries



@app.route('/')
def index():
    python_feed = fetch_url(RSS_Pyhton_url)
    react_feed = fetch_url(RSS_react_url)
    
    
    python_entries = check_feed(python_feed)
    react_entries = check_feed(react_feed)
    
    return render_template("index.html", python_entries=python_entries, react_entries=react_entries)




@socketio.on('connect')
def connect():
    print("client connected")
    python_feed = fetch_url(RSS_Pyhton_url)
    react_feed = fetch_url(RSS_react_url)
    
    latest_python_entry = latest_entry(python_feed)
    latest_react_entry = latest_entry(react_feed)
    
    if latest_python_entry:
        socketio.emit('new_python_job', latest_python_entry)
    
    if latest_react_entry:
        socketio.emit('new_react_job', latest_react_entry)


def main():
    socketio.run(app, debug=True)

if __name__ == "__main__":
    main()


