import requests
from kafka import KafkaProducer
import json
import time
from bs4 import BeautifulSoup

KAFKA_TOPIC="Financial_news"
KAFKA_BROKER="localhost:9092"

producer=KafkaProducer(
    bootstrap_servers=KAFKA_BROKER,
    value_serializer=lambda v: json.dumps(v).encode("utf-8")
)

URL = "https://www.w3schools.com/html/html_headings.asp"

def scrape_headlines():
    resp=requests.get(URL)
    soup=BeautifulSoup(resp.text,"lxml")
    headlines=[]
    for h in soup.find_all("h2"):
        text=h.get_text().strip()
        if text:
            headlines.append(text)
    # print(headlines)
    return headlines

while True:
    news=scrape_headlines()
    for headline in news:
        msg={"text":headline,"timestamp": time.time()}
        producer.send(KAFKA_TOPIC, msg)
        print("Sent: ",msg)
    time.sleep(0.5)
    
        