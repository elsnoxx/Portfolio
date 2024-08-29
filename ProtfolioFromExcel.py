import pandas as pd





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
            
        
    print("\n\n")
    print(types)

    print("\n\n")
    for tic in list(tickers.keys()):
        if tickers[tic] == 0:
            tickers.pop(tic)

    

    print("\n\n")
    for tic in list(dividends.keys()):
        if tic not in tickers:
            dividends.pop(tic)

    print(dividends)
    print(tickers)
    return tickers