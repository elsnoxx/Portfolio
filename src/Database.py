import pandas as pd
import pyodbc
import datetime
import psycopg2

# database_file_path = r"C:\\Users\\admin\\Documents\\GitHub\\Portfolio\\Portfolio.mdf"

# connection_string = (
#     r"Driver={ODBC Driver 17 for SQL Server};"
#     r"Server=(localdb)\MSSQLLocalDB;"
#     r"AttachDbFilename=" + database_file_path + ";"
#     r"Database=MyDatabase;"
#     r"Trusted_Connection=yes;"
# )



# Parametry pro připojení
# connection = psycopg2.connect(
#     dbname="porfolio",
#     user="su",
#     password="pi",
#     host="192.168.88.158",
#     port="5432"
# )

def GetDividends_ALL():
    connection = psycopg2.connect(
        dbname="porfolio",
        user="su",
        password="pi",
        host="192.168.88.158",
        port="5432"
    )
    try:
        cursor = connection.cursor()

        # Zavolání procedury
        # cursor.execute("SELECT * FROM get_dividend_totals();")
        cursor.execute("SELECT * FROM calculate_portfolio();")

        # Získání a vytištění výsledků
        results = cursor.fetchall()
        return results

    except psycopg2.Error as e:
        print(f"Chyba při dotazu: {e}")

    finally:
        # Uzavření kurzoru a spojení
        cursor.close()
        connection.close()
