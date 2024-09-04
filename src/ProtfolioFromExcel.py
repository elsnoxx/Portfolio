import pandas as pd
import yfinance as yf
import os
from datetime import datetime, timedelta




def portfolioTickers():
    # Cesta k tvému Excel souboru
    excel_file = r'etoro-account-statement.csv'

    # Načtení Excel souboru do DataFrame
    df = pd.read_csv(excel_file)
    # Výpis prvních několika řádků (pro kontrolu)
    # print(df.head())

    tickers = {}
    dividends = {}

    types = []

    for index, row in df.iterrows():
        if (row["Type"] not in types):
            types.append(row["Type"])
        if (row["Type"] == "Position closed" or row["Type"] == 'Open Position'):
            
            ticker = row["Details"].split('/')[0]
            if (ticker not in tickers):
                tickers.update({ticker: 0})

            if (row["Type"] == 'Position closed'):
                tickers[ticker] -= float(row["Units"])
            if (row["Type"] == 'Open Position'):
                tickers[ticker] += float(row["Units"])

            # print(f"-------------------------------------------------------")
            # print(f"Hodnota ve sloupci 'Date': {row["Date"]}")
            # print(f"Hodnota ve sloupci 'Details': {ticker}")
            # print(f"Hodnota ve sloupci 'Type': {row["Type"]}")
            # print(f"Hodnota ve sloupci 'Units': {row["Units"]}")
            
        if (row["Type"] == "Dividend"):
            ticker = row["Details"].split('/')[0]
            if (ticker not in dividends):
                dividends.update({ticker: 0})

            dividends[ticker] += float(row["Amount"])

            # print(f"-------------------------------------------------------")
            # print(f"Hodnota ve sloupci 'Date': {row["Date"]}")
            # print(f"Hodnota ve sloupci 'Type': {row["Type"]}")
            # ticker = row["Details"].split('/')[0]
            # print(f"Hodnota ve sloupci 'Details': {ticker}")
            # print(f"Hodnota ve sloupci 'Amount': {row["Amount"]}")
            
        
    for tic in list(tickers.keys()):
        if tickers[tic] == 0:
            tickers.pop(tic)

    for tic in list(dividends.keys()):
        if tic not in tickers:
            dividends.pop(tic)

    for tic in list(tickers):
        tickers[tic] = f'{tickers[tic]:.2f}'

    return tickers


def PortfolioFile():
    # Získání dnešního data
    today = datetime.now()
    
    # Vypočítání data před rokem
    one_year_ago = today - timedelta(days=365)
    
    # Formátování data do řetězce ve formátu YYYY-MM-DD
    end_date = today.strftime('%Y-%m-%d')
    start_date = one_year_ago.strftime('%Y-%m-%d')

    portfolio = portfolioTickers()
    data = yf.download(list(portfolio), start=start_date, end=end_date)

    # Určení cesty k adresáři pro uložení dat
    base_path = os.path.abspath(os.path.dirname('public'))
    folder_path = os.path.join(base_path, 'public', 'stock-data')

    # Vytvoření složky pro uložení dat, pokud neexistuje
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    cnt = 0
    # Uložení dat pro každý ticker zvlášť
    for ticker in list(portfolio):
        # Získání dat pro konkrétní ticker
        ticker_data = data['Adj Close'][ticker].dropna()  # Používáme 'Adj Close' jako příklad

        ticker_data = ticker_data.round(2)

        cnt += 1
        # Uložení dat do CSV souboru
        file_path = os.path.join(folder_path, f'{ticker}.csv')
        ticker_data.to_csv(file_path)

    print("Data byla úspěšně uložena do souborů.")