import re 

FEEDS = [
    # "https://www.bloomberg.com/feed/podcast/etf-report.xml",
    "https://finance.yahoo.com/news/rssindex",
    "https://www.cnbc.com/id/100003114/device/rss/rss.html",
    "https://www.marketwatch.com/rss/topstories",
    "https://www.investing.com/rss/news_25.rss",
    # "https://www.ft.com/?edition=international",  # FT may need parsing or API
    # "https://www.nasdaq.com/feed/rssoutbound?category=News"
]

SOURCE_NAME = {
    re.compile("https://finance.yahoo.com/.*"):"Yahoo.com",
    re.compile("https://www.cnbc.com/.*"):"CNBC.com",
    re.compile("https://www.marketwatch.com/.*"):"MarketWatch.com",
    re.compile("https://www.investing.com/.*"):"Investing.com"
}