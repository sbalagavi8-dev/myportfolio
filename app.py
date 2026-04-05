import os

from flask import Flask, jsonify, render_template
from dotenv import load_dotenv
from getportfolioholdings import get_dhan_holdings, simplify_holdings

load_dotenv()

app = Flask(__name__, static_folder="static", template_folder=".")

ACCESS_TOKEN = os.getenv("DHAN_ACCESS_TOKEN")


def sample_holdings():
    return [
        {
            "tradingSymbol": "AAPL",
            "stockName": "Apple Inc.",
            "totalQty": 12,
            "avgCostPrice": 145.75,
            "lastPrice": 171.23,
            "exchange": "NASDAQ",
        },
        {
            "tradingSymbol": "TSLA",
            "stockName": "Tesla, Inc.",
            "totalQty": 6,
            "avgCostPrice": 595.50,
            "lastPrice": 683.92,
            "exchange": "NASDAQ",
        },
        {
            "tradingSymbol": "INFY",
            "stockName": "Infosys Ltd.",
            "totalQty": 18,
            "avgCostPrice": 1200.0,
            "lastPrice": 1348.35,
            "exchange": "NSE",
        },
        {
            "tradingSymbol": "NIFTYBEES",
            "stockName": "Nippon India ETF Nifty Bees",
            "totalQty": 10,
            "avgCostPrice": 250.0,
            "lastPrice": 265.5,
            "exchange": "NSE",
        },
    ]


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/holdings")
def api_holdings():
    if not ACCESS_TOKEN:
        holdings = simplify_holdings({"holdings": sample_holdings()})
        return jsonify({"source": "sample", "holdings": holdings})

    data = get_dhan_holdings(ACCESS_TOKEN)
    holdings = simplify_holdings(data)
    source = "api" if data else "error"
    return jsonify({"source": source, "holdings": holdings})


if __name__ == "__main__":
    app.run(debug=True, port=5000)
