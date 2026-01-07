import requests
from kafka import KafkaProducer
import json
import time
from bs4 import BeautifulSoup
import feedparser

KAFKA_TOPIC="Financial_news"
KAFKA_BROKER="localhost:9092"

producer=KafkaProducer(
    bootstrap_servers=KAFKA_BROKER,
    value_serializer=lambda v: json.dumps(v).encode("utf-8")
)

URL = "https://feeds.marketwatch.com/marketwatch/topstories"

def scrape_headlines():
    # resp=requests.get(URL)
    feed=feedparser.parse(URL)
    headlines=[]
    for entry in feed.entries[:5]:
        print(entry.id)
        headlines.append(entry.title.strip())
        
    # print(headlines)
    return headlines



while True:

    news=scrape_headlines()
    for headline in news:

        msg={"text":headline,"timestamp": time.time()}
        producer.send(KAFKA_TOPIC, msg)
        print("Sent: ",msg)
    time.sleep(5)
    
        