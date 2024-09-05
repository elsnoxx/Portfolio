import yfinance as yf
import matplotlib.pyplot as plt
import os
import datetime as dt

def log_delete(folder_path, file_name):
    base_path = os.path.abspath(os.path.dirname('logs'))
    folder_path = os.path.join(base_path, 'logs', 'FileDelete')
    nameOfFile = os.path.join(folder_path, 'FileDelete-' + str(dt.datetime.now().date()) + '.txt')

    ensure_directory_exists(folder_path)
    
    with open(nameOfFile, 'a+') as f:
        f.write('Deleted: ' + folder_path + '\\' + file_name + '\n')

def ensure_directory_exists(path):
    if not os.path.exists(path):
        os.makedirs(path)


#  upravit na check pokud je stasiho data to smazat a vrati aby vytvoril nove
def check_graph(folder_path, file_name):
    dir_list = os.listdir(folder_path)
    for file in dir_list:
        if str(dt.datetime.now().date()) > file.split('#')[1]:
            log_delete(folder_path, file_name)
            os.remove(folder_path + '\\' + file)
            print("dnesni datum " + str(dt.datetime.now().date()) + ' je vetsi nez souboru '+  file.split('#')[1])

def stockGraph(ticker):
    base_path = os.path.abspath(os.path.dirname('public'))
    folder_path = os.path.join(base_path, 'public' ,'img', 'graph')
    ensure_directory_exists(folder_path)
    save_path = folder_path + '\\' 
    file_name = ticker + '#'+ str(dt.datetime.now().date()) +'#'+'.png'

    if check_graph(folder_path, file_name) != 2:
        df = yf.download(ticker, start="2022-12-29", end=None)
        plt.figure(figsize=(6, 3))
        plt.plot(df['Close'], label=ticker.upper(), color='darkblue')
        plt.xlabel('Date')
        # plt.ylabel('Yield')
        plt.legend()

        # plt.grid(True)
        plt.savefig(save_path + file_name)
        return(file_name)
        # plt.show()
    else:
        print('uz je vytvoren')
        return(file_name)



