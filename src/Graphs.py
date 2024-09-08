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


#  upravit na check pokud je stasiho data to smazat a vrati aby vytvoril nove
def check_graph(folder_path, file_name):
    dir_list = os.listdir(folder_path)
    for file in dir_list:
        if str(datetime.now().date()) > file.split('#')[1]:
            log_delete(folder_path, file_name)
            os.remove(folder_path + '\\' + file)
            print("dnesni datum " + str(datetime.now().date()) + ' je vetsi nez souboru '+  file.split('#')[1])

def stockGraph(ticker):
    base_path = os.path.abspath(os.path.dirname('public'))
    folder_path = os.path.join(base_path, 'public' ,'img', 'graph')
    ensure_directory_exists(folder_path)
    
    if os.name == 'nt':
        save_path = folder_path + '\\' 
    if os.name == 'posix':
        save_path = folder_path + '/' 
        
    file_name = ticker + '#'+ str(datetime.now().date()) +'#'+'.png'

    # Získání dnešního data
    today = datetime.now()
    
    # Vypočítání data před 2 roky
    two_year_ago = today - timedelta(days=365 *3)
    
    # Formátování data do řetězce ve formátu YYYY-MM-DD
    end_date = today.strftime('%Y-%m-%d')
    start_date = two_year_ago.strftime('%Y-%m-%d')

    if check_graph(folder_path, file_name) != 2:
        df = yf.download(ticker, start=start_date, end=end_date)

        df['SMA200'] = df['Close'].rolling(window=200).mean()
        

        plt.figure(figsize=(15, 3))
        plt.plot(df['Close'], label=ticker.upper(), color='darkblue')
        plt.plot(df['SMA200'], label='SMA 200', color='orange', linestyle='--')
        plt.xlabel('Date')
        # plt.ylabel('Yield')
        plt.legend()

        # plt.grid(True)
        plt.savefig(save_path + file_name)
        plt.close()
        return(file_name)
        # plt.show()
    else:
        print('uz je vytvoren')
        return(file_name)



