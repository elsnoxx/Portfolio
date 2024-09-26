import pandas as pd
import pyodbc
import datetime

database_file_path = r"C:\\Users\\admin\\Documents\\GitHub\\Portfolio\\Portfolio.mdf"

connection_string = (
    r"Driver={ODBC Driver 17 for SQL Server};"
    r"Server=(localdb)\MSSQLLocalDB;"
    r"AttachDbFilename=" + database_file_path + ";"
    r"Database=MyDatabase;"
    r"Trusted_Connection=yes;"
)


def GetDividends_ALL():
    conn = pyodbc.connect(connection_string)

    cursor = conn.cursor()
    cursor.execute("EXEC Portfolio.dbo.Dividend_Total_ALL")
    # Pokud uložená procedura vrací data, můžeme je načíst
    rows = cursor.fetchall()

    conn.close()
    return rows