import numpy as np
import numpy_financial as npf  
import pandas as pd
import os
from dotenv import load_dotenv
from kiteconnect import KiteConnect
from datetime import datetime, timedelta



load_dotenv()

API_KEY = os.getenv("ZERODHA_API_KEY")
API_SECRET = os.getenv("ZERODHA_API_SECRET")
ACCESS_TOKEN = os.getenv("ZERODHA_ACCESS_TOKEN")

kite = KiteConnect(api_key=API_KEY)

kite.set_access_token(ACCESS_TOKEN)


def check_connection():
    """Check if Zerodha connection is active."""
    try:
        profile = kite.profile()
        return {"status": "Connected", "user": profile["user_name"]}
    except Exception as e:
        return {"status": "Error", "message": str(e)}


def holdings():
    """Fetch Zerodha Holdings with calculated P&L."""
    try:
        holdings_data = kite.holdings()
        holdings_list = []

        for stock in holdings_data:
            invested = stock["quantity"] * stock["average_price"]
            current = stock["quantity"] * stock["last_price"]
            change = current - invested

            holdings_list.append({
                "symbol": stock["tradingsymbol"],
                "quantity": stock["quantity"],
                "invested_amount": round(invested, 2),
                "current_value": round(current, 2),
                "profit_loss": round(change, 2),
                "profit_loss_percent": round((change / invested) * 100, 2) if invested else 0
            })

        return holdings_list

    except Exception as e:
        return {"error": str(e)}


def positions():
    """Fetch Zerodha Positions with calculated P&L."""
    try:
        positions_data = kite.positions()["net"]
        positions_list = []

        for position in positions_data:
            invested = position["quantity"] * position["average_price"]
            current = position["quantity"] * position["last_price"]
            change = current - invested

            positions_list.append({
                "symbol": position["tradingsymbol"],
                "quantity": position["quantity"],
                "invested_amount": round(invested, 2),
                "current_value": round(current, 2),
                "profit_loss": round(change, 2),
                "profit_loss_percent": round((change / invested) * 100, 2) if invested else 0
            })

        return positions_list

    except Exception as e:
        return {"error": str(e)}


def sector_allocation():
    """Fetch Sector-Wise Portfolio Allocation (% of total investment)."""
    try:
        holdings_data = kite.holdings()
        df = pd.DataFrame(holdings_data)

        df["invested_amount"] = df["quantity"] * df["average_price"]
        total_investment = df["invested_amount"].sum()


        if "sector" not in df.columns:
            df["sector"] = df["tradingsymbol"]  

        sector_allocation = df.groupby("sector")["invested_amount"].sum().reset_index()
        sector_allocation["percentage_invested"] = round((sector_allocation["invested_amount"] / total_investment) * 100, 2)

        return sector_allocation.to_dict(orient="records")

    except Exception as e:
        return {"error": str(e)}


def statistics():
    """Calculate Portfolio Performance Metrics."""
    try:
        holdings_data = kite.holdings()
        df = pd.DataFrame(holdings_data)

        df["invested_amount"] = df["quantity"] * df["average_price"]
        df["current_value"] = df["quantity"] * df["last_price"]
        df["profit_loss"] = df["current_value"] - df["invested_amount"]

        df["return_percent"] = df.apply(lambda row: (row["profit_loss"] / row["invested_amount"]) * 100 if row["invested_amount"] > 0 else 0, axis=1)

        cashflows = []
        for _, row in df.iterrows():
            buy_date = row.get("exchange_timestamp", None)
            if buy_date:
                buy_date = datetime.strptime(buy_date, "%Y-%m-%d %H:%M:%S")
            else:
                buy_date = datetime.now()  

            if row["invested_amount"] > 0:
                cashflows.append((-row["invested_amount"], buy_date))  
            cashflows.append((row["current_value"], datetime.now()))  

        if len(cashflows) > 1:
            xirr = calculate_xirr(cashflows) * 100
        else:
            xirr = 0

        years = 1  
        if len(cashflows) > 1:
            years = (datetime.now() - cashflows[0][1]).days / 365
        invested_sum = df["invested_amount"].sum()
        cagr = ((df["current_value"].sum() / invested_sum) ** (1 / years) - 1) * 100 if invested_sum > 0 else 0

        weighted_return = (df["return_percent"] * df["invested_amount"] / invested_sum).sum() if invested_sum > 0 else 0

        return {
            "XIRR (%)": round(xirr, 2),
            "CAGR (%)": round(cagr, 2),
            "Return (%)": round(df["return_percent"].sum(), 2),
            "Weighted Return (%)": round(weighted_return, 2),
        }

    except Exception as e:
        return {"error": str(e)}

def calculate_xirr(cashflows):
    """Calculate XIRR using cash flows and dates."""
    try:
        amounts, dates = zip(*cashflows)
        years = np.array([(d - dates[0]).days / 365.0 for d in dates])
        return npf.irr(amounts) 
    except Exception:
        return 0


if __name__ == "__main__":
    print(check_connection())
    print(statistics())
    
