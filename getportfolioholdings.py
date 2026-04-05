import math
import requests
from dotenv import load_dotenv
import os

load_dotenv()

ETF_LIST = ["CONSUMER", "ITBEES", "GROWWRAIL", "MOREALTY"]

def safe_float(value, default=0.0):
    try:
        if value is None or value == "":
            return default
        return float(value)
    except (ValueError, TypeError):
        return default


def get_dhan_holdings(access_token: str):
    """
    Fetch holdings from Dhan API using the provided JWT access token.
    """
    url = "https://api.dhan.co/v2/holdings"
    headers = {
        "Content-Type": "application/json",
        "access-token": access_token
    }

    try:
        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            data = response.json()
            return data
        else:
            print("Error:", response.status_code, response.text)
            return None

    except requests.exceptions.RequestException as e:
        print("Request failed:", e)
        return None


def normalize_holding(item: dict, instruments: dict = None):
    symbol = item.get("tradingSymbol") or item.get("symbol") or item.get("tradingsymbol") or "Unknown"
    name = item.get("stockName") or item.get("companyName") or item.get("symbolName") or symbol
    exchange = item.get("exchange") or item.get("stockExchange") or item.get("market") or "N/A"

    qty = safe_float(item.get("totalQty") or item.get("qty") or item.get("quantity"))
    avg_cost = safe_float(item.get("avgCostPrice") or item.get("averageCost") or item.get("averagePrice"))
    last_price = item.get("lastPrice")
    if last_price is None:
        last_price = item.get("closePrice") or item.get("lastTradedPrice") or item.get("price")
    last_price = safe_float(last_price, default=None)

    total_invested = qty * avg_cost
    profit = None
    profit_percent = None

    if last_price is not None and math.isfinite(last_price) and avg_cost != 0:
        profit = (last_price - avg_cost) * qty
        profit_percent = ((last_price - avg_cost) / avg_cost) * 100

    instrument_type = "ETF" if symbol in ETF_LIST else "STK"

    normalized = {
        "tradingSymbol": symbol,
        "stockName": name,
        "exchange": exchange,
        "totalQty": qty,
        "avgCostPrice": avg_cost,
        "lastPrice": last_price,
        "totalInvested": total_invested,
        "profit": profit,
        "profitPercent": profit_percent,
        "instrumentType": instrument_type,
    }
    normalized.update({k: v for k, v in item.items() if k not in normalized})
    return normalized


def simplify_holdings(data, instruments: dict = None):
    if not data:
        return []
    if isinstance(data, list):
        holdings = data
    elif isinstance(data, dict):
        if "data" in data and isinstance(data["data"], list):
            holdings = data["data"]
        elif "holdings" in data and isinstance(data["holdings"], list):
            holdings = data["holdings"]
        else:
            holdings = [data]
    else:
        return []

    return [normalize_holding(item) for item in holdings]


if __name__ == "__main__":
    # Replace with your actual Dhan JWT token
    ACCESS_TOKEN = os.getenv("DHAN_ACCESS_TOKEN")

    holdings_data = get_dhan_holdings(ACCESS_TOKEN)
    holdings = simplify_holdings(holdings_data)

    print(f"Found {len(holdings)} holdings")
    for h in holdings[:5]:  # Print first 5
        print(f"{h}")
