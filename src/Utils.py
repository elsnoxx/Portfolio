import os
import psutil
import datetime as dt

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
    print("OS name " + os.name)
    base_path = os.path.abspath(os.path.dirname('logs'))
    folder_path = os.path.join(base_path, 'logs', 'FileDelete')
    nameOfFile = os.path.join(folder_path, 'FileDelete-' + str(dt.datetime.now().date()) + '.txt')
    
    # Vytvoření složky, pokud neexistuje
    ensure_directory_exists(folder_path)
    
    with open(nameOfFile, 'a+') as f:
        base_path = os.path.abspath(os.path.dirname('logs'))
        logs_folders = ['ram', 'cpu', 'fileDelete', 'http_requests']
        for path in logs_folders:
            folder_path = os.path.join(base_path, 'logs', path)

            dir_list = os.listdir(folder_path)

            if (len(dir_list) >= 5 and os.name == 'nt'):
                file_sort = sorted(dir_list)
                os.remove(folder_path + '\\' + file_sort[0])
                f.write('Deleted: ' + folder_path + '\\' + file_sort[0] + '\n')
            else:
                file_sort = sorted(dir_list)
                os.remove(folder_path + '/' + file_sort[0])
                f.write('Deleted: ' + folder_path + '/' + file_sort[0] + '\n')


def log_delete(folder_path, file_name):
    base_path = os.path.abspath(os.path.dirname('logs'))
    folder_path = os.path.join(base_path, 'logs', 'FileDelete')
    nameOfFile = os.path.join(folder_path, 'FileDelete-' + str(dt.datetime.now().date()) + '.txt')

    ensure_directory_exists(folder_path)
    
    if os.name == 'nt':
        with open(nameOfFile, 'a+') as f:
            f.write('Deleted: ' + folder_path + '\\' + file_name + '\n')
            
    if os.name == 'posix':
        with open(nameOfFile, 'a+') as f:
            f.write('Deleted: ' + folder_path + '/' + file_name + '\n')