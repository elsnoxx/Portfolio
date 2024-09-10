import os
import psutil
import datetime as dt
from pathlib import Path

def ensure_directory_exists(path):
    if not os.path.exists(path):
        os.makedirs(path)

def logRamUsage():
    # Získání absolutní cesty pro složku
    base_path = os.path.abspath(os.path.dirname('logs'))
    folder_path = os.path.join(base_path, 'logs', 'ram')
    nameOfFile = os.path.join(folder_path, 'LogRam-' + str(dt.datetime.now().date()) + '.txt')
    # Vytvoření složky, pokud neexistuje
    ensure_directory_exists(folder_path)
    
    # Získání a zapsání zprávy
    message = f'RAM usage {dt.datetime.now()}: {psutil.virtual_memory().percent} %'

    with open(nameOfFile, 'a+') as f:
        f.write(message + '\n')

def logCpuUsage():
    # Získání absolutní cesty pro složku
    base_path = os.path.abspath(os.path.dirname('logs'))
    folder_path = os.path.join(base_path, 'logs', 'cpu')
    nameOfFile = os.path.join(folder_path, 'LogCPU-' + str(dt.datetime.now().date()) + '.txt')
    
    # Vytvoření složky, pokud neexistuje
    ensure_directory_exists(folder_path)
    
    # Získání a zapsání zprávy
    message = f'CPU usage {dt.datetime.now()}: {psutil.cpu_percent()} %'

    with open(nameOfFile, 'a+') as f:
        f.write(message + '\n')


def deleteLogs():
    # Získání absolutní cesty pro složku
    base_path = os.path.abspath(os.path.dirname('logs'))
    folder_path = os.path.join(base_path, 'logs', 'fileDelete')
    nameOfFile = os.path.join(folder_path, 'fileDelete-' + str(dt.datetime.now().date()) + '.txt')
    
    # Vytvoření složky, pokud neexistuje
    ensure_directory_exists(folder_path)
    
    with open(nameOfFile, 'a+') as f:
        base_path = os.path.abspath(os.path.dirname('logs'))
        logs_folders = ['ram', 'cpu', 'fileDelete', 'http_requests']
        
        for path in logs_folders:
            folder_path = os.path.join(base_path, 'logs', path)

            # Kontrola, jestli složka existuje, pokud ne, přeskočit
            if not os.path.exists(folder_path):
                continue

            dir_list = os.listdir(folder_path)

            if len(dir_list) >= 5:
                file_sort = sorted(dir_list)
                file_to_delete = os.path.join(folder_path, file_sort[0])  # Použití os.path.join pro správné cesty

                # Odstranění souboru
                os.remove(file_to_delete)
                f.write('Deleted: ' + str(dt.datetime.now()) + ' ' + file_to_delete + '\n')


def log_delete(folder_path, file_name):
    # Získání absolutní cesty pro složku
    base_path = os.path.abspath(os.path.dirname('logs'))
    folder_path = os.path.join(base_path, 'logs', 'fileDelete')
    nameOfFile = os.path.join(folder_path, 'fileDelete-' + str(dt.datetime.now().date()) + '.txt')

    # Vytvoření složky, pokud neexistuje
    ensure_directory_exists(folder_path)
    
    # Vytvoření cesty ke smazanému souboru
    file_to_delete = os.path.join(folder_path, file_name)
    
    # Zápis do souboru
    with open(nameOfFile, 'a+') as f:
        f.write('Deleted: ' + str(dt.datetime.now()) + ' ' + file_to_delete + '\n')


def get_files_tree(startpath):
    file_tree = []
    for item in sorted(Path(startpath).iterdir()):
        file_tree.append({'name': item.name, 'path': str(item), 'is_dir': item.is_dir()})
    return file_tree

