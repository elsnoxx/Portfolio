import yfinance as yf
import pandas as pd

def technicalAnalysis(ticker):
    data = yf.download(ticker, period='1y', interval='1d')
    ticker = yf.Ticker(ticker)
    info = ticker.info

    # Výpočet základních trendů pomocí klouzavého průměru
    data['SMA_50'] = data['Close'].rolling(window=50).mean()
    data['SMA_200'] = data['Close'].rolling(window=200).mean()

    # Definice trendu
    if data['SMA_50'].iloc[-1] > data['SMA_200'].iloc[-1]:
        trend = 'Rostoucí'
        trend_recommendation = 'Buy'
    elif data['SMA_50'].iloc[-1] < data['SMA_200'].iloc[-1]:
        trend = 'Klesající'
        trend_recommendation = 'Sell'
    else:
        trend = 'Boční'
        trend_recommendation = 'Hold'
    
    # Výpočet maxima a minima za poslední období (např. 30 dní)
    data['Support'] = data['Low'].rolling(window=30).min()
    data['Resistance'] = data['High'].rolling(window=30).max()

    support = data['Support'].iloc[-1]
    resistance = data['Resistance'].iloc[-1]

    # Výpočet klouzavého průměru (SMA) a exponenciálního klouzavého průměru (EMA)
    data['SMA_20'] = data['Close'].rolling(window=20).mean()
    data['EMA_20'] = data['Close'].ewm(span=20, adjust=False).mean()

    # Výpočet RSI
    delta = data['Close'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
    rs = gain / loss
    data['RSI'] = 100 - (100 / (1 + rs))
    
    # Výpočet MACD
    short_ema = data['Close'].ewm(span=12, adjust=False).mean()
    long_ema = data['Close'].ewm(span=26, adjust=False).mean()
    data['MACD'] = short_ema - long_ema
    data['MACD_Signal'] = data['MACD'].ewm(span=9, adjust=False).mean()

    # Příklad detekce Hammer formace
    def is_hammer(row):
        body = abs(row['Close'] - row['Open'])
        lower_shadow = row['Open'] - row['Low'] if row['Close'] > row['Open'] else row['Close'] - row['Low']
        upper_shadow = row['High'] - row['Close'] if row['Close'] > row['Open'] else row['High'] - row['Open']
        return lower_shadow > 2 * body and upper_shadow < body

    data['Hammer'] = data.apply(is_hammer, axis=1)

    hammer_found = data['Hammer'].iloc[-1]

    # Vytvoření výsledného slovníku
    result = {
        'trend': trend,
        'current_price': info['currentPrice'],
        'trend_recommendation': trend_recommendation,
        'support': round(support, 2),
        'resistance': round(resistance, 2),
        'sma_20': round(data['SMA_20'].iloc[-1], 2),
        'ema_20': round(data['EMA_20'].iloc[-1], 2),
        'rsi': round(data['RSI'].iloc[-1], 2),
        'macd': round(data['MACD'].iloc[-1], 2),
        'macd_signal': round(data['MACD_Signal'].iloc[-1], 2),
        'hammer_found': hammer_found,
        'hammer_recommendation': 'Buy' if hammer_found else 'Sell'
    }
    
    return result
