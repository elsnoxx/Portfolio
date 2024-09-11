import yfinance as yf
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import plotly.graph_objects as go

# Stažení historických dat
ticker = 'KO'
data = yf.download(ticker, period='1y', interval='1d')

# Výpočet základních trendů pomocí klouzavého průměru
data['SMA_50'] = data['Close'].rolling(window=50).mean()
data['SMA_200'] = data['Close'].rolling(window=200).mean()

# Výpočet maxima a minima za poslední období
data['Support'] = data['Low'].rolling(window=30).min()
data['Resistance'] = data['High'].rolling(window=30).max()

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

# Detekce Hammer formace
def is_hammer(row):
    body = abs(row['Close'] - row['Open'])
    lower_shadow = row['Open'] - row['Low'] if row['Close'] > row['Open'] else row['Close'] - row['Low']
    upper_shadow = row['High'] - row['Close'] if row['Close'] > row['Open'] else row['High'] - row['Open']
    return lower_shadow > 2 * body and upper_shadow < body

data['Hammer'] = data.apply(is_hammer, axis=1)

# Plotly grafy
fig = go.Figure()

# Graf cen akcií a SMA
fig.add_trace(go.Scatter(x=data.index, y=data['Close'], mode='lines', name='Close'))
fig.add_trace(go.Scatter(x=data.index, y=data['SMA_50'], mode='lines', name='SMA 50'))
fig.add_trace(go.Scatter(x=data.index, y=data['SMA_200'], mode='lines', name='SMA 200'))

# Graf RSI
fig.add_trace(go.Scatter(x=data.index, y=data['RSI'], mode='lines', name='RSI'))
fig.add_trace(go.Scatter(x=data.index, y=[70]*len(data), mode='lines', name='RSI Upper Band', line=dict(color='red', dash='dash')))
fig.add_trace(go.Scatter(x=data.index, y=[30]*len(data), mode='lines', name='RSI Lower Band', line=dict(color='green', dash='dash')))

# Graf MACD
fig.add_trace(go.Scatter(x=data.index, y=data['MACD'], mode='lines', name='MACD'))
fig.add_trace(go.Scatter(x=data.index, y=data['MACD_Signal'], mode='lines', name='MACD Signal'))

# Konfigurace layoutu
fig.update_layout(title=f'{ticker} - Technical Analysis', xaxis_title='Date', yaxis_title='Value')

# Uložení do HTML souboru
fig.write_html('technical_analysis.html')
