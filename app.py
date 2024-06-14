from flask import Flask, render_template
from flask_cors import CORS
from flask_socketio import SocketIO
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timedelta
import feedparser
import requests
import time

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///jobs.db'
CORS(app)
socketio = SocketIO(app, cors_allowed_origins="*", ping_timeout=600, ping_interval=25) 
db = SQLAlchemy(app)

# Job model to store job details
class Job(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    job_id = db.Column(db.String(255), unique=True, nullable=False)
    title = db.Column(db.String(255), nullable=False)
    link = db.Column(db.String(255), nullable=False)
    published = db.Column(db.DateTime, nullable=False)
    category = db.Column(db.String(255), nullable=False)

    def __init__(self, job_id, title, link, published, category):
        self.job_id = job_id
        self.title = title
        self.link = link
        self.published = published
        self.category = category


RSS_Pyhton_url = "https://www.upwork.com/ab/feed/jobs/rss?location=Australia%2CCanada%2CChile%2CDenmark%2CFrance%2CGermany%2CItaly%2CNetherlands%2CNew%20Zealand%2CSaudi%20Arabia%2CSwitzerland%2CUnited%20Arab%20Emirates%2CUnited%20Kingdom%2CUnited%20States&paging=0-10&q=python%20NOT%20india&sort=recency&api_params=1&securityToken=81e2b4b45c1bf6ef8752e649541dc096c20e5256d9034c5b7b5898739550d9fb376ac7e6e4e9632b1f46b176ab780d4ebb09f44ae9b3e5ee6b505b0bbfe61d2a&userUid=1672273345003061248&orgUid=1672273345003061249"
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
fetched_categories = set()
last_emitted_jobs = {}
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
                break
    print(f"Failed to fetch {url} after {max_retries} retries")
    return None

def fetch_url(url, count=50):
    return fetch_with_retry(url, count)


def check_feed(feed, category):
    if feed is None:
        print("Error: Failed to fetch feed.")
        return []

    new_entries = []
    current_time = datetime.now()

    for entry in feed.entries[:50]:
        job_id = entry.id
        if not Job.query.filter_by(job_id=job_id).first():  # Check if job already exists
            try:
                entry_time = datetime.strptime(entry.published, '%a, %d %b %Y %H:%M:%S %z')
                entry_time = entry_time.replace(tzinfo=None)
            except Exception as e:
                print(f"Error parsing datetime for entry: {e}")
                continue

            if current_time - entry_time < timedelta(days=1):
                new_job = Job(
                    job_id=job_id,
                    title=entry.title,
                    link=entry.link,
                    published=entry_time,
                    category=category
                )
                db.session.add(new_job)
                db.session.commit()
                new_entries.append(new_job)

    return new_entries


@app.route('/')
def index():
    entries = {}
    for key in feeds.keys():
        entries[key] = Job.query.filter_by(category=key).order_by(Job.published.desc()).limit(50).all()
    return render_template('index.html', **entries)

@socketio.on('connect')
def connect():
    print("Client connected")
    for key, url in feeds.items():
        # Adjust fetch_url to include a delay
        entries = check_feed(fetch_url(url, 50), key)
        for entry in entries:
            socketio.emit('new_job', {'job': {
                'title': entry.title,
                'link': entry.link,
                'published': entry.published.strftime('%a, %d %b %Y %H:%M:%S %z'),
                'category': entry.category
            }, 'category': key}, namespace='/')
            print(f"Emitted new_job event with data: {entry.title} for category: {key}")
            time.sleep(1)  


@socketio.on('disconnect')
def disconnect():
    print('Client disconnected')

def main():
    with app.app_context():
        db.create_all()
        socketio.run(app, debug=True)

if __name__ == "__main__":
    main()