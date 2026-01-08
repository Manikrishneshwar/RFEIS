import time
import feedparser
from producer.utils import generate_event_id
from producer.feeds import SOURCE_NAME

def scrape_events(URL):
    
    feed=feedparser.parse(URL)
    events=[]
    for entry in feed.entries[:5]:
        title = entry.title.strip()
        published = entry.get("published", None)
        link = entry.get("link", None)

        event_id = generate_event_id(title, SOURCE_NAME)

        event = {
            "event_id": event_id,
            "source": SOURCE_NAME,
            "title": title,
            "url": link,
            "published_at": published,
            "ingested_at": time.time()
        }
        events.append(event)

        
    # print(headlines)
    return events
