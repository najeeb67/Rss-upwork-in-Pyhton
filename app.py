import feedparser
from datetime import datetime, timedelta
from apscheduler.schedulers.background import BackgroundScheduler
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_socketio import SocketIO
import sys
import traceback
import time

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///jobs.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
scheduler = BackgroundScheduler()
scheduler.start()


app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app, cors_allowed_origins="*")



class JobPosting(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255))
    link = db.Column(db.String(255))
    published = db.Column(db.DateTime)


def delete_old_data():
    threshold = datetime.utcnow() - timedelta(hours=24)
    JobPosting.query.filter(JobPosting.published < threshold).delete()
    db.session.commit()

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

Rss_File = "File.txt"




def fetch_with_retry(url, count=10, max_retries=3, retry_delay=5):
    retries = 0
    while retries < max_retries:
        try:
            url += f"&paging=0-{count}"
            return feedparser.parse(url)
        except Exception as e:
            print(f"Error fetching {url}: {e}")
            traceback.print_exc()
            retries += 1
            time.sleep(retry_delay)
    print(f"Failed to fetch {url} after {max_retries} retries")
    return None


def fetch_url(url, count=10):
    return fetch_with_retry(url, count)


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
        if current_time - entry_time < timedelta(days=2):
            new_job = JobPosting(title=entry.title, link=entry.link, published=entry_time)
            db.session.add(new_job)
            db.session.commit()
            new_entries.append({
                'title': entry.title,
                'link': entry.link,
                'published': entry_time,
            })
    return new_entries



@app.route('/')
def index():
    python_feed = fetch_url(RSS_Pyhton_url)
    react_feed = fetch_url(RSS_react_url)
    us_feed = fetch_url(RSS_US_url)
    node_feed = fetch_url(RSS_NODE_url)
    php_feed = fetch_url(RSS_PHP_url)
    wordpress_feed = fetch_url(RSS_WORDPRES_url)
    quickbooks_feed = fetch_url(RSS_QUICKBOOKS_url)
    shopify_feed = fetch_url(RSS_SHOPIFY_url)
    api_integration_feed = fetch_url(RSS_API_INTEGRAGATION_url)
    payment_gateway_feed = fetch_url(RSS_PAYMENT_GETWAY_url)
    full_time_feed = fetch_url(RSS_FULL_TIME_url)
    chatbot_feed = fetch_url(RSS_CHATBOT_url)
    scripting_feed = fetch_url(RSS_SCRIPPTING_url)
    bubble_feed = fetch_url(RSS_BUBBLE_url)
    webrtc_feed = fetch_url(RSS_WEBRTC_url)
    vue_feed = fetch_url(RSS_VUE_url)

    python_entries = check_feed(python_feed)
    react_entries = check_feed(react_feed)
    us_entries = check_feed(us_feed)
    node_entries = check_feed(node_feed)
    php_entries = check_feed(php_feed)
    wordpress_entries = check_feed(wordpress_feed)
    quickbooks_entries = check_feed(quickbooks_feed)
    shopify_entries = check_feed(shopify_feed)
    api_integration_entries = check_feed(api_integration_feed)
    payment_gateway_entries = check_feed(payment_gateway_feed)
    full_time_entries = check_feed(full_time_feed)
    chatbot_entries = check_feed(chatbot_feed)
    scripting_entries = check_feed(scripting_feed)
    bubble_entries = check_feed(bubble_feed)
    webrtc_entries = check_feed(webrtc_feed)
    vue_entries = check_feed(vue_feed)
    previous_job_postings = JobPosting.query.all()
    # print(python_entries)
    return render_template('index.html', python_entries=python_entries, react_entries=react_entries, us_entries=us_entries, node_entries=node_entries,php_entries=php_entries,wordpress_entries=wordpress_entries,
                           quickbooks_entries=quickbooks_entries,shopify_entries=shopify_entries,api_integration_entries=api_integration_entries,payment_gateway_entries=payment_gateway_entries,
                           full_time_entries=full_time_entries,chatbot_entries=chatbot_entries,scripting_entries=scripting_entries,bubble_entries=bubble_entries,webrtc_entries=webrtc_entries,vue_entries=vue_entries,previous_job_postings=previous_job_postings)





@socketio.on('connect')
def connect():
    print("client connected")
    python_feed = fetch_url(RSS_Pyhton_url)
    react_feed = fetch_url(RSS_react_url)
    us_feed = fetch_url(RSS_US_url)
    node_feed = fetch_url(RSS_NODE_url)
    php_feed = fetch_url(RSS_PHP_url)
    wordpress_feed = fetch_url(RSS_WORDPRES_url)
    quickbooks_feed = fetch_url(RSS_QUICKBOOKS_url)
    shopify_feed = fetch_url(RSS_SHOPIFY_url)
    api_integration_feed = fetch_url(RSS_API_INTEGRAGATION_url)
    payment_gateway_feed = fetch_url(RSS_PAYMENT_GETWAY_url)
    full_time_feed = fetch_url(RSS_FULL_TIME_url)
    chatbot_feed = fetch_url(RSS_CHATBOT_url)
    scripting_feed = fetch_url(RSS_SCRIPPTING_url)
    bubble_feed = fetch_url(RSS_BUBBLE_url)
    webrtc_feed = fetch_url(RSS_WEBRTC_url)
    vue_feed = fetch_url(RSS_VUE_url)

    latest_python_entry = latest_entry(python_feed)
    latest_react_entry = latest_entry(react_feed)
    latest_us_entry = latest_entry(us_feed)
    latest_node_entry = latest_entry(node_feed)
    latest_php_entry = latest_entry(php_feed)
    latest_wordpress_entry = latest_entry(wordpress_feed)
    latest_quickbooks_entry = latest_entry(quickbooks_feed)
    latest_shopify_entry = latest_entry(shopify_feed)
    latest_api_integration_entry = latest_entry(api_integration_feed)
    latest_payment_gateway_entry = latest_entry(payment_gateway_feed)
    latest_full_time_entry = latest_entry(full_time_feed)
    latest_chatbot_entry = latest_entry(chatbot_feed)
    latest_scripting_entry = latest_entry(scripting_feed)
    latest_bubble_entry = latest_entry(bubble_feed)
    latest_webrtc_entry = latest_entry(webrtc_feed)
    latest_vue_entry = latest_entry(vue_feed)
    



    if latest_react_entry:
        socketio.emit('new_react_job', latest_react_entry)
   
    if latest_python_entry:
        socketio.emit('new_python_job', latest_python_entry)

    if latest_us_entry:
        socketio.emit('new_us_job', latest_us_entry)
    if latest_node_entry:
        socketio.emit('new_node_job', latest_node_entry)
    if latest_php_entry:
        socketio.emit('new_php_job', latest_php_entry)
    if latest_wordpress_entry:
        socketio.emit('new_wordpress_job', latest_wordpress_entry)
    if latest_quickbooks_entry:
        socketio.emit('new_quickbooks_job', latest_quickbooks_entry)
    if latest_shopify_entry:
        socketio.emit('new_shopify_job', latest_shopify_entry)
    if latest_api_integration_entry:
        socketio.emit('new_api_integration_job', latest_api_integration_entry)
    if latest_payment_gateway_entry:
        socketio.emit('new_payment_gateway_job', latest_payment_gateway_entry)
    if latest_full_time_entry:
        socketio.emit('new_full_time_job', latest_full_time_entry)
    if latest_chatbot_entry:
        socketio.emit('new_chatbot_job', latest_chatbot_entry) 
    if latest_scripting_entry:
        socketio.emit('new_scripting_job', latest_scripting_entry)
    if latest_bubble_entry:
        socketio.emit('new_bubble_job', latest_bubble_entry)
    if latest_webrtc_entry:
        socketio.emit('new_webrtc_job', latest_webrtc_entry)
    if latest_vue_entry:
        socketio.emit('new_vue_job', latest_vue_entry)


scheduler.add_job(delete_old_data, 'interval', hours=24)

def main():
    socketio.run(app, debug=True)

if __name__ == "__main__":
    db.create_all
    main()


# @socketio.on('connect')
# def connect():
#     print("client connected")
#     feeds = {
#         'new_react_job': RSS_react_url,
#         'new_python_job': RSS_Pyhton_url,
#         'new_us_job': RSS_US_url,
#         'new_node_job': RSS_NODE_url,
#         'new_php_job': RSS_PHP_url,
#         'new_wordpress_job': RSS_WORDPRES_url,
#         'new_quickbooks_job': RSS_QUICKBOOKS_url,
#         'new_shopify_job': RSS_SHOPIFY_url,
#         'new_api_integration_job': RSS_API_INTEGRAGATION_url,
#         'new_payment_gateway_job': RSS_PAYMENT_GETWAY_url,
#         'new_full_time_job': RSS_FULL_TIME_url,
#         'new_chatbot_job': RSS_CHATBOT_url,
#         'new_scripting_job': RSS_SCRIPPTING_url,
#         'new_bubble_job': RSS_BUBBLE_url,
#         'new_webrtc_job': RSS_WEBRTC_url,
#         'new_vue_job': RSS_VUE_url
#     }

#     for job_type, url in feeds.items():
#         feed = fetch_url(url)
#         latest_entry_data = latest_entry(feed)
#         if latest_entry_data:
#             socketio.emit(job_type, latest_entry_data)