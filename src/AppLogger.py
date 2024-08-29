import os
import datetime as dt
import logging

# Zajistí, že adresář pro logování existuje
def ensure_directory_exists(path):
    if not os.path.exists(path):
        os.makedirs(path)

# Vytvoří logger pro logování HTTP požadavků
def setup_request_logger():
    # Získání absolutní cesty pro složku logů
    base_path = os.path.abspath(os.path.dirname('logs'))
    folder_path = os.path.join(base_path, 'logs', 'http_requests')
    ensure_directory_exists(folder_path)
    
    # Získání jména log souboru
    log_file_name = os.path.join(folder_path, 'HttpRequests-' + str(dt.datetime.now().date()) + '.log')
    
    # Nastavení loggeru
    request_logger = logging.getLogger('http_requests')
    request_logger.setLevel(logging.INFO)
    
    # Vytvoření FileHandleru pro logování do souboru
    file_handler = logging.FileHandler(log_file_name)
    formatter = logging.Formatter('%(message)s')
    file_handler.setFormatter(formatter)
    request_logger.addHandler(file_handler)
    
    return request_logger
