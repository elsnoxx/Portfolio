import psycopg2
import pandas as pd

# Připojení k databázi
connection_string = {
    "dbname": "porfolio",
    "user": "su",
    "password": "pi",
    "host": "localhost",
    "port": "5432"
}

try:
    conn = psycopg2.connect(**connection_string)
    print("Připojení úspěšné!")
    cursor = conn.cursor()
    cursor.execute("""TRUNCATE TABLE Dividends RESTART IDENTITY;""")
    conn.commit()
    cursor.execute("""TRUNCATE TABLE Trades RESTART IDENTITY;""")
    conn.commit()
    
    # Předpokládáme, že máme DataFrame s daty
    # Zde vytvoříme příklad DataFrame
    df = pd.read_csv(r'etoro-account-statement.csv')

    for index, row in df.iterrows():
        if row["Type"] == "Dividend":
            # Vkládání do tabulky Dividends
            cursor.execute("""
                INSERT INTO Dividends (date, type, details, amount)
                VALUES (%s, %s, %s, %s)
            """, (row["Date"], row["Type"], row["Details"], row["Amount"]))
        if (row["Amount"] != '-' and row["Amount"] != ' ' and row["Units"] != '-'):
            # Vkládání do tabulky Trades
            cursor.execute("""
                INSERT INTO Trades (date, type, details, amount, units)
                VALUES (%s, %s, %s, %s, %s)
            """, (row["Date"], row["Type"], row["Details"], row["Amount"], row["Units"]))
    
    # Uložení změn do databáze
    conn.commit()

    # Dotaz na data z tabulky Dividends
    cursor.execute("SELECT * FROM Dividends")
    dividends = cursor.fetchall()
    print("Dividends:")
    for row in dividends:
        print(row)

    # Dotaz na data z tabulky Trades
    cursor.execute("SELECT * FROM Trades")
    trades = cursor.fetchall()
    print("Trades:")
    for row in trades:
        print(row)

except psycopg2.Error as e:
    print(f"Chyba připojení: {e}")

