import requests
from datetime import datetime
import pandas as pd
import numpy as np

# https://docs.coingecko.com/reference/introduction

# https://api.coingecko.com/api/v3/coins/list

def formatMarketCap(marketCap):
    if marketCap >= 1_000_000_000_000:
        return f"{marketCap / 1_000_000_000_000:.2f} T"
    elif marketCap >= 1_000_000_000:
        return f"{marketCap / 1_000_000_000:.2f} B"
    elif marketCap >= 1_000_000:
        return f"{marketCap / 1_000_000:.2f} M"
    else:
        return str(marketCap)


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


def get_top_10_cryptos(btn_id):
    url = "https://api.coingecko.com/api/v3/coins/markets"
    params = {
        'vs_currency': 'usd',
        'order': 'market_cap_desc',
        'per_page': 10,
        'page': btn_id
    }
    response = requests.get(url, params=params)
    data = response.json()
    
    # Zpracujeme data do vhodného formátu pro předání šabloně
    # 
    processed_data = []
    for coin in data:
        # print(type(coin['current_price']))
        processed_data.append({
            'image': coin['image'],
            'name': coin['name'],
            'id': coin['id'],
            'market_cap': formatMarketCap(coin['market_cap']),
            'price': f"${coin['current_price']:,}",
            'high_24h': f"${coin['high_24h']:,}",
            'low_24h': f"${coin['low_24h']:,}",
            'price_int': coin['current_price'],
            'high_24h_int': coin['high_24h'],
            'low_24h_int': coin['low_24h']
        })

    return processed_data


def get_crypto_details(crypto_id):
    url = "https://api.coingecko.com/api/v3/coins/"
    url = url + crypto_id.lower()


    

    response = requests.get(url)
    if (response == 404):
        print(response)
        return 2
    if (response != 429):
        data = response.json()
        if (data == {'error': 'coin not found'} ):
            print(response)
            return 2
        
        print(data)
        if (len(data['links']['repos_url']['github']) == 2):
            open_source = data['links']['repos_url']['github'][0]
        else:
            open_source = data['links']['repos_url']['github']

        processed_data = {
                "symbol": data['symbol'],
                "launch_year": data['genesis_date'],
                "algorithm": data['hashing_algorithm'],
                'description': data['description']['en'],
                "twitter_link": ("https://x.com/" + data['links']['twitter_screen_name']),
                "reddit_link":  data['links']['subreddit_url'],
                "whitepaper":  data['links']['whitepaper'],
                "open_source":  open_source,
                'image': data['image']['small'],
                'name': data['name'],
                'market_cap': formatMarketCap(data["market_data"]["market_cap"]["usd"]),
                'price': f"${data["market_data"]["current_price"]["usd"]:,}",
                'high_24h': f"${data["market_data"]["high_24h"]["usd"]:,}",
                'low_24h': f"${data["market_data"]["low_24h"]["usd"]:,}",
                "circulating_supply": data["market_data"]["circulating_supply"],
                "total_supply": data["market_data"]["total_supply"],
                "trading_volume_24h": data["market_data"]["total_volume"]["usd"]
            }
        return processed_data
    else:
        print(response)
        return 1
        



# def FearAndGreesIndex():
#     r = requests.get('https://api.alternative.me/fng/?limit=0')
#     df = pd.DataFrame(r.json()['data'])
#     df.value = df.value.astype(int)
#     df.timestamp = pd.to_datetime(df.timestamp, unit='s')
#     df.set_index('timestamp', inplace=True)
#     df = df[::-1]
#     print(df)


def FearAndGreesIndex():
    # Načtení dat z API
    r = requests.get('https://api.alternative.me/fng/?limit=0')
    data = r.json()['data']
    df = pd.DataFrame(data)
    
    # Oprava datového typu
    df['value'] = df['value'].astype(int)
    df['timestamp'] = pd.to_numeric(df['timestamp'], errors='coerce')
    df['timestamp'] = pd.to_datetime(df['timestamp'], unit='s')
    
    # Nastavení timestamp jako indexu
    df.set_index('timestamp', inplace=True)
    
    # Získání nejnovějšího záznamu
    latest_entry = df.iloc[-1]
    
    # Příprava výsledku
    result = {
        'value_classification': latest_entry['value_classification'],
        'value': int(latest_entry['value']),  # Převod na standardní Python int
        'updated': latest_entry.name.strftime('%Y-%m-%d')
    }
    
    return result
