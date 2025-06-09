import requests
import os

ALPHAVANTAGE_API_KEY = os.getenv("ALPHAVANTAGE_API_KEY")

def fetch_quote(symbol):
    url = f"https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={symbol}&apikey={ALPHAVANTAGE_API_KEY}"
    response = requests.get(url)
    data = response.json()
    return data.get("Global Quote", {})

def fetch_time_series_daily(symbol, outputsize='compact'):
    url = f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={symbol}&outputsize={outputsize}&apikey={ALPHAVANTAGE_API_KEY}"
    response = requests.get(url)
    data = response.json()
    return data.get("Time Series (Daily)", {})

def fetch_time_series_intraday(symbol, interval='5min', outputsize='compact'):
    url = f"https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol={symbol}&interval={interval}&outputsize={outputsize}&apikey={ALPHAVANTAGE_API_KEY}"
    response = requests.get(url)
    data = response.json()
    return data.get(f"Time Series ({interval})", {})

def fetch_company_overview(symbol):
    url = f"https://www.alphavantage.co/query?function=OVERVIEW&symbol={symbol}&apikey={ALPHAVANTAGE_API_KEY}"
    response = requests.get(url)
    data = response.json()
    return data

def fetch_news_sentiment(symbol):
    url = f"https://www.alphavantage.co/query?function=NEWS_SENTIMENT&symbol={symbol}&apikey={ALPHAVANTAGE_API_KEY}"
    response = requests.get(url)
    data = response.json()
    return data.get("news", [])

# Additional utility functions can be added here as needed.