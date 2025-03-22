import pandas as pd
import yfinance as yf
from datetime import datetime, timedelta

FAVORITE_STOCKS = [
    "NIFTY50.NS", "BANKNIFTY.NS", "TCS.NS", "INFY.NS", "RELIANCE.NS",
    "HDFCBANK.NS", "ICICIBANK.NS", "HINDUNILVR.NS", "BAJFINANCE.NS", "LT.NS"
]

def get_live_data():
    """Fetch live stock prices from Yahoo Finance."""
    live_data = []
    for stock in FAVORITE_STOCKS:
        try:
            ticker = yf.Ticker(stock)
            data = ticker.history(period="1d")
            latest_price = data["Close"].iloc[-1]  
            live_data.append({
                "symbol": stock,
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "price": round(latest_price, 2)
            })
        except Exception as e:
            print(f"Error fetching live data for {stock}: {e}")

    return live_data

def get_historical_data():
    """Fetch historical stock data (last 30 days)."""
    historical_data = {}
    end_date = datetime.today().strftime("%Y-%m-%d")
    start_date = (datetime.today() - timedelta(days=30)).strftime("%Y-%m-%d")

    for stock in FAVORITE_STOCKS:
        try:
            ticker = yf.Ticker(stock)
            data = ticker.history(start=start_date, end=end_date)
            historical_data[stock] = data[["Open", "High", "Low", "Close", "Volume"]].reset_index().to_dict(orient="records")
        except Exception as e:
            print(f"Error fetching historical data for {stock}: {e}")

    return historical_data

if __name__ == "__main__":
    print("Fetching Live Data...")
    print(get_live_data())

    print("\nFetching Historical Data...")
    print(get_historical_data())
