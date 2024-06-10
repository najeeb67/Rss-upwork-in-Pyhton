import feedparser
from datetime import datetime, timedelta
from apscheduler.schedulers.background import BackgroundScheduler
from flask import Flask, render_template
from flask_cors import CORS
from flask_socketio import SocketIO
import sys
import requests
import time

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
CORS(app)
socketio = SocketIO(app, cors_allowed_origins="*")




RSS_react_url = "https://www.upwork.com/ab/feed/jobs/rss?location=Australia%2CCanada%2CChile%2CDenmark%2CFrance%2CGermany%2CItaly%2CNetherlands%2CNew%20Zealand%2CSaudi%20Arabia%2CSwitzerland%2CUnited%20Arab%20Emirates%2CUnited%20Kingdom%2CUnited%20States&paging=0-10&q=react.js%20NOT%20Expensify&sort=recency&api_params=1&securityToken=81e2b4b45c1bf6ef8752e649541dc096c20e5256d9034c5b7b5898739550d9fb376ac7e6e4e9632b1f46b176ab780d4ebb09f44ae9b3e5ee6b505b0bbfe61d2a&userUid=1672273345003061248&orgUid=1672273345003061249"
RSS_US_url ="https://www.upwork.com/ab/feed/topics/rss?securityToken=81e2b4b45c1bf6ef8752e649541dc096c20e5256d9034c5b7b5898739550d9fb376ac7e6e4e9632b1f46b176ab780d4ebb09f44ae9b3e5ee6b505b0bbfe61d2a&userUid=1672273345003061248&orgUid=1672273345003061249&sort=local_jobs_on_top&topic=domestic"
RSS_NODE_url = "https://www.upwork.com/ab/feed/jobs/rss?location=Australia%2CCanada%2CChile%2CDenmark%2CFrance%2CGermany%2CItaly%2CNetherlands%2CNew%20Zealand%2CSaudi%20Arabia%2CSwitzerland%2CUnited%20Arab%20Emirates%2CUnited%20Kingdom%2CUnited%20States&paging=0-10&q=node%20NOT%20Expensify&sort=recency&api_params=1&securityToken=81e2b4b45c1bf6ef8752e649541dc096c20e5256d9034c5b7b5898739550d9fb376ac7e6e4e9632b1f46b176ab780d4ebb09f44ae9b3e5ee6b505b0bbfe61d2a&userUid=1672273345003061248&orgUid=1672273345003061249"
RSS_PHP_url ="https://www.upwork.com/ab/feed/jobs/rss?location=Australia%2CCanada%2CDenmark%2CFrance%2CGermany%2CItaly%2CNetherlands%2CNew%20Zealand%2CSwitzerland%2CUnited%20Arab%20Emirates%2CUnited%20Kingdom%2CUnited%20States&paging=0-10&payment_verified=1&q=PHP&sort=recency&api_params=1&securityToken=81e2b4b45c1bf6ef8752e649541dc096c20e5256d9034c5b7b5898739550d9fb376ac7e6e4e9632b1f46b176ab780d4ebb09f44ae9b3e5ee6b505b0bbfe61d2a&userUid=1672273345003061248&orgUid=1672273345003061249"
RSS_WORDPRES_url = "https://www.upwork.com/ab/feed/jobs/rss?location=Australia%2CCanada%2CChile%2CDenmark%2CFrance%2CGermany%2CItaly%2CNetherlands%2CNew%20Zealand%2CSaudi%20Arabia%2CSwitzerland%2CUnited%20Arab%20Emirates%2CUnited%20Kingdom%2CUnited%20States&paging=0-10&q=wordpress%20NOT%20india&sort=recency&api_params=1&securityToken=81e2b4b45c1bf6ef8752e649541dc096c20e5256d9034c5b7b5898739550d9fb376ac7e6e4e9632b1f46b176ab780d4ebb09f44ae9b3e5ee6b505b0bbfe61d2a&userUid=1672273345003061248&orgUid=1672273345003061249"
RSS_QUICKBOOKS_url="https://www.upwork.com/ab/feed/jobs/rss?location=Australia%2CCanada%2CChile%2CDenmark%2CFrance%2CGermany%2CItaly%2CNetherlands%2CNew%20Zealand%2CSaudi%20Arabia%2CSwitzerland%2CUnited%20Arab%20Emirates%2CUnited%20Kingdom%2CUnited%20States&paging=0-10&q=quickbooks&sort=recency&api_params=1&securityToken=81e2b4b45c1bf6ef8752e649541dc096c20e5256d9034c5b7b5898739550d9fb376ac7e6e4e9632b1f46b176ab780d4ebb09f44ae9b3e5ee6b505b0bbfe61d2a&userUid=1672273345003061248&orgUid=1672273345003061249"
RSS_SHOPIFY_url = "https://www.upwork.com/ab/feed/jobs/rss?location=Australia%2CCanada%2CChile%2CDenmark%2CFrance%2CGermany%2CItaly%2CNetherlands%2CNew%20Zealand%2CSaudi%20Arabia%2CSwitzerland%2CUnited%20Arab%20Emirates%2CUnited%20Kingdom%2CUnited%20States&paging=0-10&q=shopify%20OR%20ecommerce&sort=recency&api_params=1&securityToken=81e2b4b45c1bf6ef8752e649541dc096c20e5256d9034c5b7b5898739550d9fb376ac7e6e4e9632b1f46b176ab780d4ebb09f44ae9b3e5ee6b505b0bbfe61d2a&userUid=1672273345003061248&orgUid=1672273345003061249"
RSS_API_INTEGRAGATION_url ="https://www.upwork.com/ab/feed/jobs/rss?location=Australia%2CCanada%2CChile%2CDenmark%2CFrance%2CGermany%2CItaly%2CNetherlands%2CNew%20Zealand%2CSaudi%20Arabia%2CSwitzerland%2CUnited%20Arab%20Emirates%2CUnited%20Kingdom%2CUnited%20States&paging=0-10&q=api%20integration&sort=recency&api_params=1&securityToken=81e2b4b45c1bf6ef8752e649541dc096c20e5256d9034c5b7b5898739550d9fb376ac7e6e4e9632b1f46b176ab780d4ebb09f44ae9b3e5ee6b505b0bbfe61d2a&userUid=1672273345003061248&orgUid=1672273345003061249"
RSS_PAYMENT_GETWAY_url ="https://www.upwork.com/ab/feed/jobs/rss?location=Australia%2CCanada%2CChile%2CDenmark%2CFrance%2CGermany%2CItaly%2CNetherlands%2CNew%20Zealand%2CSaudi%20Arabia%2CSwitzerland%2CUnited%20Arab%20Emirates%2CUnited%20Kingdom%2CUnited%20States&paging=0-10&q=payment%20gateway&sort=recency&api_params=1&securityToken=81e2b4b45c1bf6ef8752e649541dc096c20e5256d9034c5b7b5898739550d9fb376ac7e6e4e9632b1f46b176ab780d4ebb09f44ae9b3e5ee6b505b0bbfe61d2a&userUid=1672273345003061248&orgUid=1672273345003061249"
RSS_FULL_TIME_url ="https://www.upwork.com/ab/feed/jobs/rss?location=Australia%2CCanada%2CChile%2CDenmark%2CFrance%2CGermany%2CItaly%2CNetherlands%2CNew%20Zealand%2CSaudi%20Arabia%2CSwitzerland%2CUnited%20Arab%20Emirates%2CUnited%20Kingdom%2CUnited%20States&paging=0-10&q=full%20time&sort=recency&api_params=1&securityToken=81e2b4b45c1bf6ef8752e649541dc096c20e5256d9034c5b7b5898739550d9fb376ac7e6e4e9632b1f46b176ab780d4ebb09f44ae9b3e5ee6b505b0bbfe61d2a&userUid=1672273345003061248&orgUid=1672273345003061249"
RSS_CHATBOT_url = "https://www.upwork.com/ab/feed/jobs/rss?location=Australia%2CCanada%2CChile%2CDenmark%2CFrance%2CGermany%2CItaly%2CNetherlands%2CNew%20Zealand%2CSaudi%20Arabia%2CSwitzerland%2CUnited%20Arab%20Emirates%2CUnited%20Kingdom%2CUnited%20States&paging=0-10&q=chatbot&sort=recency&api_params=1&securityToken=81e2b4b45c1bf6ef8752e649541dc096c20e5256d9034c5b7b5898739550d9fb376ac7e6e4e9632b1f46b176ab780d4ebb09f44ae9b3e5ee6b505b0bbfe61d2a&userUid=1672273345003061248&orgUid=1672273345003061249"
RSS_SCRIPPTING_url ="https://www.upwork.com/ab/feed/jobs/rss?location=Australia%2CCanada%2CChile%2CDenmark%2CFrance%2CGermany%2CItaly%2CNetherlands%2CNew%20Zealand%2CSaudi%20Arabia%2CSwitzerland%2CUnited%20Arab%20Emirates%2CUnited%20Kingdom%2CUnited%20States&paging=0-10&q=scripting%20OR%20automation&sort=recency&api_params=1&securityToken=81e2b4b45c1bf6ef8752e649541dc096c20e5256d9034c5b7b5898739550d9fb376ac7e6e4e9632b1f46b176ab780d4ebb09f44ae9b3e5ee6b505b0bbfe61d2a&userUid=1672273345003061248&orgUid=1672273345003061249"
RSS_BUBBLE_url="https://www.upwork.com/ab/feed/jobs/rss?location=Australia%2CCanada%2CChile%2CDenmark%2CFrance%2CGermany%2CItaly%2CNetherlands%2CNew%20Zealand%2CSaudi%20Arabia%2CSwitzerland%2CUnited%20Arab%20Emirates%2CUnited%20Kingdom%2CUnited%20States&paging=0-10&q=bubble&sort=recency&api_params=1&securityToken=81e2b4b45c1bf6ef8752e649541dc096c20e5256d9034c5b7b5898739550d9fb376ac7e6e4e9632b1f46b176ab780d4ebb09f44ae9b3e5ee6b505b0bbfe61d2a&userUid=1672273345003061248&orgUid=1672273345003061249"
RSS_WEBRTC_url="https://www.upwork.com/ab/feed/jobs/rss?location=Australia%2CCanada%2CChile%2CDenmark%2CFrance%2CGermany%2CItaly%2CNetherlands%2CNew%20Zealand%2CSaudi%20Arabia%2CSwitzerland%2CUnited%20Arab%20Emirates%2CUnited%20Kingdom%2CUnited%20States&paging=0-10&q=webrtc%20OR%20socket&sort=recency&api_params=1&securityToken=81e2b4b45c1bf6ef8752e649541dc096c20e5256d9034c5b7b5898739550d9fb376ac7e6e4e9632b1f46b176ab780d4ebb09f44ae9b3e5ee6b505b0bbfe61d2a&userUid=1672273345003061248&orgUid=1672273345003061249"
RSS_VUE_url ="https://www.upwork.com/ab/feed/jobs/rss?location=Australia%2CCanada%2CChile%2CDenmark%2CFrance%2CGermany%2CItaly%2CNetherlands%2CNew%20Zealand%2CSaudi%20Arabia%2CSwitzerland%2CUnited%20Arab%20Emirates%2CUnited%20Kingdom%2CUnited%20States&paging=0-10&q=vue&sort=recency&api_params=1&securityToken=81e2b4b45c1bf6ef8752e649541dc096c20e5256d9034c5b7b5898739550d9fb376ac7e6e4e9632b1f46b176ab780d4ebb09f44ae9b3e5ee6b505b0bbfe61d2a&userUid=1672273345003061248&orgUid=1672273345003061249"
RSS_Pyhton_url = "https://www.upwork.com/ab/feed/jobs/rss?location=Australia%2CCanada%2CChile%2CDenmark%2CFrance%2CGermany%2CItaly%2CNetherlands%2CNew%20Zealand%2CSaudi%20Arabia%2CSwitzerland%2CUnited%20Arab%20Emirates%2CUnited%20Kingdom%2CUnited%20States&paging=0-10&q=python%20NOT%20india&sort=recency&api_params=1&securityToken=81e2b4b45c1bf6ef8752e649541dc096c20e5256d9034c5b7b5898739550d9fb376ac7e6e4e9632b1f46b176ab780d4ebb09f44ae9b3e5ee6b505b0bbfe61d2a&userUid=1672273345003061248&orgUid=1672273345003061249"

feeds = {
        "python_entries": RSS_Pyhton_url,
        "react_entries": RSS_react_url,
        "us_entries": RSS_US_url,
        "node_entries": RSS_NODE_url,
        "php_entries": RSS_PHP_url,
        "wordpress_entries": RSS_WORDPRES_url,
        "quickbooks_entries": RSS_QUICKBOOKS_url,
        "shopify_entries": RSS_SHOPIFY_url,
        "api_integration_entries": RSS_API_INTEGRAGATION_url,
        "payment_gateway_entries": RSS_PAYMENT_GETWAY_url,
        "full_time_entries": RSS_FULL_TIME_url,
        "chatbot_entries": RSS_CHATBOT_url,
        "scripting_entries": RSS_SCRIPPTING_url,
        "bubble_entries": RSS_BUBBLE_url,
        "webrtc_entries": RSS_WEBRTC_url,
        "vue_entries": RSS_VUE_url,
    }


Rss_File = "File.txt"

def fetch_with_retry(url, count=10, max_retries=3, retry_delay=1, fetch_delay=2):
    retries = 0
    while retries < max_retries:
        try:
            url_with_paging = f"{url}&paging=0-{count}"
            response = requests.get(url_with_paging)
            response.raise_for_status()  
            time.sleep(fetch_delay) 
            return feedparser.parse(response.text)
        except requests.exceptions.RequestException as e:
            print(f"Error fetching {url}: {e}")
            if isinstance(e, requests.exceptions.HTTPError) and e.response.status_code == 429:
                wait_time = 2 ** retries * retry_delay
                print(f"Rate limit exceeded. Retrying in {wait_time} seconds...")
                time.sleep(wait_time)
                retries += 1
            else:
                print("Non-rate-limit error encountered. Exiting retry loop.")
                break
    print(f"Failed to fetch {url} after {max_retries} retries")
    return None


def fetch_url(url, count=50):
    return fetch_with_retry(url, count)

def get_title():
    try:
        with open('rss_title.txt', 'r') as file: 
            return file.read().strip()
    except FileNotFoundError:
        return None

def set_title(title):
    with open('rss_title.txt', 'w', encoding="utf-8") as file:  
        file.write(title)

def latest_entry(feed):
    if feed is not None and 'entries' in feed:
        return feed.entries[0] if feed.entries else None
    else:
        print("Error: Failed to parse feed.")
        return None


fetched_categories = set()

def check_feed(feed):
    global fetched_categories
    if feed is None:
        print("Error: Failed to fetch feed.")
        return []

    new_entries = []
    latest = latest_entry(feed)
    new_get_titles = get_title()
    current_time = datetime.now()

    if latest:
        try:
            latest_title = latest['title'].encode(sys.stdout.encoding, errors='replace').decode(sys.stdout.encoding)
        except Exception as e:
            print(f"Error encoding latest title: {e}")
            latest_title = None

        if latest_title and latest_title != new_get_titles:
            new_job = {
                'title': latest_title,
                'link': latest['link'],
                'published': latest['published'],
            }
            new_entries.append(new_job)
            set_title(latest_title)
            print(f"New job posting: {latest_title}")

            category = latest_title.split()[0]
            if category not in fetched_categories:
                print(f"New category Fetch: {category}")
                fetched_categories.add(category)

    for entry in feed.entries[:50]:  # Ensure we only take the first 50 entries
        try:
            entry_time = datetime.strptime(entry.published, '%a, %d %b %Y %H:%M:%S %z')
            entry_time = entry_time.replace(tzinfo=None)
        except Exception as e:
            print(f"Error parsing datetime for entry: {e}")
            continue

        if current_time - entry_time < timedelta(days=1):
            new_job = {
                'title': entry.title,
                'link': entry.link,
                'published': entry.published,
            }
            new_entries.append(new_job)

            socketio.emit('new_job', new_job)
            print(f"Emitted new_job event with data: {new_job} for category: {new_entries}")

    return new_entries



@app.route('/')
def index():

    entries = {key: check_feed(fetch_url(url)) for key, url in feeds.items()}
    # previous_job_postings = JobPosting.query.all()
    
    return render_template('index.html', **entries)

@socketio.on('connect')
def connect():
    print("client connected")
    for key, url in feeds.items():
        entries = check_feed(fetch_url(url))
        return entries
        for entry in entries:
            socketio.emit('new_job', {'job': entry, 'category': key}, namespace='/')
            print(f"Emitted new_job event with data: {entry} for category: {key}")

@socketio.on('disconnect')
def disconnect():
    print('Client disconnected')

def main():
    socketio.run(app, debug=True)

if __name__ == "__main__":
    # db.create_all
    main()


