import os
import psutil
import datetime as dt

def get_CPU_usage():
    return { 'cpu_usage' : psutil.cpu_percent()}

def get_RAM_usage():
    return {'ram_usage': psutil.virtual_memory().percent}




    