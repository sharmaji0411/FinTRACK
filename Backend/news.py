import os
import requests
import feedparser
from dotenv import load_dotenv


load_dotenv()
NEWSAPI_KEY = os.getenv("NEWSAPI_KEY")


GOOGLE_NEWS_RSS = "https://news.google.com/rss/search?q=stock+market+OR+dividend+OR+earnings+OR+investment&hl=en-IN&gl=IN&ceid=IN:en"


FINANCIAL_KEYWORDS = [
    "dividend", "stock split", "bonus issue", "funding", "investment",
    "capital raise", "earnings", "quarterly results", "profit", "loss",
    "financials", "balance sheet", "PE ratio", "ROE", "debt-to-equity",
    "buyback", "share offering", "revenue", "EBITDA", "EPS", "IPO", "merger",
    "inflation", "interest rates", "stock market", "bond yield", "Federal Reserve",
    "GDP", "credit rating", "market outlook", "global economy", "growth forecast",
    "economic recovery", "economic growth", "economic outlook", "economic forecast",
    "economic indicators", "economic data", "economic news", "economic events",
    "economic analysis", "economic commentary", "economic report", "economic update",
    "economic forecast", "economic outlook", "economic growth", "economic indicators",
    "economic data", "economic news", "economic events", "economic analysis",
    "economic commentary", "economic report", "economic update", "economic impact",
]

def fetch_google_news():
    """Fetch latest stock market news from Google News RSS."""
    news_list = []

    try:
        feed = feedparser.parse(GOOGLE_NEWS_RSS)

        for entry in feed.entries:
            title = entry.title
            link = entry.link

            
            if any(keyword in title.lower() for keyword in FINANCIAL_KEYWORDS):
                news_list.append({
                    "news_title": title,
                    
                    "source": "Google News",
                    "url": link
                })

    except Exception as e:
        print("Error fetching Google News:", e)

    return news_list

def fetch_newsapi_news():
    """Fetch stock market news from NewsAPI as a fallback."""
    news_list = []

    try:
        url = f"https://newsapi.org/v2/everything?q=stock+market&language=en&apiKey={NEWSAPI_KEY}&pageSize=20"
        response = requests.get(url)
        data = response.json()

        if "articles" in data:
            for article in data["articles"]:
                news_list.append({
                    "news_title": article["title"],
                    "detail": article["description"] if article["description"] else "No details available.",
                    "source": article["source"]["name"],
                    "url": article["url"]
                })

    except Exception as e:
        print("Error fetching NewsAPI:", e)

    return news_list

def fetch_combined_news():
    """Combine news from Google News RSS & NewsAPI, ensuring at least 20 articles."""
    google_news = fetch_google_news()
    if len(google_news) < 20:
        newsapi_news = fetch_newsapi_news()
        google_news.extend(newsapi_news[: (50 - len(google_news))]) 

    return google_news[:50]

if __name__ == "__main__":
    print(fetch_combined_news())
