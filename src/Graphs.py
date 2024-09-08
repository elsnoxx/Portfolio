import yfinance as yf
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import pandas as pd
import os
from datetime import datetime, timedelta
from src.Utils import log_delete

def ensure_directory_exists(path):
    if not os.path.exists(path):
        os.makedirs(path)

# Upravená funkce pro kontrolu souborů
def check_graph(folder_path, file_name):
    dir_list = os.listdir(folder_path)
    today_date = str(datetime.now().date())
    
    for file in dir_list:
        # Extrahujeme datum ze souboru pomocí rozdělení
        file_date = file.split('#')[1]
        if today_date > file_date:
            log_delete(folder_path, file)
            file_path = os.path.join(folder_path, file)
            os.remove(file_path)  # Použití os.path.join pro multiplatformní mazání
            print(f"Dnešní datum {today_date} je větší než datum souboru {file_date}")
            return 2  # Vracíme 2, pokud byl soubor smazán
    return 1  # Pokud nebylo nic smazáno, vrátíme 1

def stockGraph(ticker):
    # Získání cesty do složky
    base_path = os.path.abspath(os.path.dirname('public'))
    folder_path = os.path.join(base_path, 'public', 'img', 'graph')
    ensure_directory_exists(folder_path)

    # Vytvoření cesty k uložení souboru, multiplatformní
    save_path = os.path.join(folder_path, '')
    
    # Název souboru podle tickeru a aktuálního data
    file_name = f"{ticker}#{str(datetime.now().date())}#.png"
    
    # Získání dnešního data
    today = datetime.now()
    
    # Vypočítání data před 3 roky
    three_years_ago = today - timedelta(days=365 * 3)
    
    # Formátování dat do řetězce ve formátu YYYY-MM-DD
    end_date = today.strftime('%Y-%m-%d')
    start_date = three_years_ago.strftime('%Y-%m-%d')

    # Kontrola, zda existuje graf pro dnešní datum
    if check_graph(folder_path, file_name) != 2:
        # Stáhnutí dat pro daný ticker za poslední 3 roky
        df = yf.download(ticker, start=start_date, end=end_date)

        # Výpočet 200denního klouzavého průměru
        df['SMA200'] = df['Close'].rolling(window=200).mean()

        # Vytvoření grafu
        plt.figure(figsize=(15, 3))
        plt.plot(df['Close'], label=ticker.upper(), color='darkblue')
        plt.plot(df['SMA200'], label='SMA 200', color='orange', linestyle='--')
        plt.xlabel('Date')
        plt.legend()

        # Uložení grafu do souboru
        plt.savefig(os.path.join(save_path, file_name))
        plt.close()

        return file_name
    else:
        print('Graf pro tento den již existuje')
        return file_name
