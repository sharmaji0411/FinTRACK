from flask import Flask, jsonify
from flask_cors import CORS
import portfolio as pf  
import livedata 
import news
app = Flask(__name__)
CORS(app, origins=["http://localhost:5173"]) 
@app.route("/portfolio", methods=["GET"])
def get_portfolio():
    """Fetch portfolio data (holdings, positions, statistics)."""
    return jsonify({
        "holdings": pf.holdings(),
        "positions": pf.positions(),
        "statistics": pf.statistics(),
              
    })

@app.route("/live", methods=["GET"])
def get_live_data():
    """Fetch latest live stock prices."""
    return jsonify({
        "live_data": livedata.get_live_data()  
    })

@app.route("/historical", methods=["GET"])
def get_historical_data():
    """Fetch historical stock data (last 30 days)."""
    return jsonify({
        "historical_data": livedata.get_historical_data()
    })


@app.route("/news", methods=["GET"])
def get_stock_news():
    """Fetch latest stock market news from Google News & NewsAPI"""
    return jsonify({"news": news.fetch_combined_news()})

if __name__ == "__main__":
    app.run(debug=True, port=5000)
