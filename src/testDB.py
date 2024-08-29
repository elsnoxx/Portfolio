import pandas as pd
import pyodbc
import datetime

def convert(date_time):
    # Aktuální formát v CSV: "20/02/2024 16:55:20"
    format_csv = '%d/%m/%Y %H:%M:%S'
    # Formát pro převod do datetime objektu
    format_datetime = '%Y-%m-%d %H:%M:%S'
    
    datetime_str = datetime.datetime.strptime(date_time, format_csv)
    # Převedení na formát pro vložení do databáze
    datetime_str = datetime_str.strftime(format_datetime)

    return datetime_str

df = pd.read_csv(r'etoro-account-statement.csv')

database_file_path = r"C:\\Users\\admin\\Desktop\\TaskManagerV2\\DataBase\\TaskManagerDB.mdf"

connection_string = (
    r"Driver={ODBC Driver 17 for SQL Server};"
    r"Server=(localdb)\MSSQLLocalDB;"
    r"AttachDbFilename=" + database_file_path + ";"
    r"Database=MyDatabase;"
    r"Trusted_Connection=yes;"
)

try:
    # Připojení k databázi
    conn = pyodbc.connect(connection_string)
    print("Připojení úspěšné!")

    # Vytvoření kurzoru pro vykonávání dotazů
    cursor = conn.cursor()
    for index, row in df.iterrows():
        if (row["Type"] != "Dividend" and row["Type"] != 'Edit Stop Loss' and row["Type"] != 'Deposit'):
            # print(f"-------------------------------------------------------")
            # print(f"Hodnota ve sloupci 'Date': {row["Date"]}")
            # print(f"Hodnota ve sloupci 'Type': {row["Type"]}")
            # print(f"Hodnota ve sloupci 'Details': {row["Details"]}")
            # print(f"Hodnota ve sloupci 'Amount': {row["Amount"]}")
            # print(f"Hodnota ve sloupci 'Units': {row["Date"]}")
            if (row["Amount"] != '-' and row["Amount"] != ' ' and row["Units"] != '-'):
                cursor.execute("""
                    INSERT INTO [Portfolio].[dbo].[Trades] ( Date, Type, Details, Amount, Units)
                    VALUES (?, ?, ?, ?, ?)
                """, 
                convert(row["Date"]), row["Type"], row["Details"], float(row["Amount"]), float(row["Units"]))
            
        if (row["Type"] == "Dividend"):
            # print(f"-------------------------------------------------------")
            # print(f"Hodnota ve sloupci 'Date': {row["Date"]}")
            # print(f"Hodnota ve sloupci 'Type': {row["Type"]}")
            # print(f"Hodnota ve sloupci 'Details': {row["Details"]}")
            # print(f"Hodnota ve sloupci 'Amount': {row["Amount"]}")
            if (row["Amount"] != '-' or row["Amount"] != ' ' or row["Units"] != '-'):
                cursor.execute("""
                    INSERT INTO [Portfolio].[dbo].[Dividends] (Date, Type, Details, Amount)
                    VALUES (?, ?, ?, ?)
                """, 
                convert(row["Date"]), row["Type"], row["Details"], float(row["Amount"]))
    # Příklad dotazu
    cursor.execute("SELECT * FROM [Portfolio].[dbo].[Dividends]")
    cursor.execute("SELECT * FROM [Portfolio].[dbo].[Trades]")

    # Výpis výsledků dotazu
    for row in cursor.fetchall():
        print(row)

except pyodbc.Error as e:
    print(f"Chyba připojení: {e}")

finally:
    # Uzavření připojení
    conn.close()
