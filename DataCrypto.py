import requests
from datetime import datetime

# https://docs.coingecko.com/reference/introduction

# https://api.coingecko.com/api/v3/coins/list

def bitcoinData(url, ticker):
    try:
        response = requests.get(url)
        response.raise_for_status()  # zkontroluje, zda nedošlo k chybě
        data = response.json()  # převede odpověď na JSON

        if data["market_data"]["market_cap"]["usd"] > 1000000000000:
            market_cap = data["market_data"]["market_cap"]["usd"] / 1000000000000
            market_cap = "{:.2f} T".format(market_cap)
        else:
            market_cap = data["market_data"]["market_cap"]["usd"] / 1000000000
            market_cap = "{:.2f} B".format(market_cap)

        ratios = {
            "symbol": data['symbol'],
            "current_price": data["market_data"]["current_price"]["usd"],
            "ath": data["market_data"]["ath"]["usd"],
            "ath_change_percentage": data["market_data"]["ath_change_percentage"]["usd"],
            "market_cap": market_cap,
            "high_24h": data["market_data"]["high_24h"]["usd"],
            "low_24h": data["market_data"]["low_24h"]["usd"],
            "price_change_percentage_24h": data["market_data"]["price_change_percentage_24h"]
        }
        print(ratios)
        return ratios

    except requests.exceptions.HTTPError as err:
        print(f"HTTP error occurred: {err}")
    except Exception as err:
        print(f"Other error occurred: {err}")
