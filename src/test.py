import requests
import psycopg2

def connect_to_db():
    conn = psycopg2.connect(
        dbname="porfolio",
        user="su",
        password="pi",
        host="192.168.88.158",
        port="5432"
    )
    return conn

def insert_financials(conn, CIK, ticker, name):
    with conn.cursor() as cur:
        cur.execute(
            """
            INSERT INTO cik_tables (cik, ticker, name)
            VALUES (%s, %s, %s)
            """, (CIK, ticker, name)
        )

        
# Definuj URL endpointu pro EDGAR Company Search API
url = "https://www.sec.gov/files/company_tickers.json"

headers = {
    'User-Agent': 'my-email@example.com',  # Tvůj email
    'Accept': 'application/json',
}

def fetch_sec_data(cik):
    url = f"https://data.sec.gov/api/xbrl/companyfacts/CIK{cik}.json"
    print(url)
    
    headers = {
        'User-Agent': 'my-email@example.com',  # Tvůj email
        'Accept': 'application/json',
    }
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        return response.json()  # Vrátí JSON data
    else:
        print(f"Chyba při volání API: {response.status_code}")
        return None
    
# Pošli GET požadavek na server
response = requests.get(url, headers=headers)
conn = connect_to_db()

# Zpracuj odpověď
if response.status_code == 200:
    data = response.json()
    
    # Výpis seznamu společností s CIK čísly
    # for key, value in data.items():
    #     cik_str = str(value['cik_str']).zfill(10)
    #     print(f"Společnost {value['title']} (Ticker: {value['ticker']}) má CIK: {cik_str}")
    #     insert_financials(conn, cik_str, value['ticker'], value['title'])
    
    # Načti CIK pro ticker 'AAPL'
    with conn.cursor() as cur:
        cur.execute("SELECT cik FROM cik_tables WHERE ticker = %s;", ('AAPL',))
        cik_result = cur.fetchone()  # Získání prvního výsledku
        
        if cik_result:  # Pokud CIK existuje
            cik_str = str(cik_result[0]).zfill(10)  # Ujisti se, že CIK má 10 znaků
            print(f"CIK pro ticker 'AAPL' je: {cik_str}")
            
            # Zavolej SEC API s CIK
            sec_data = fetch_sec_data(cik_str)
            if sec_data:
                print(sec_data)  # Zpracuj data podle potřeby
        else:
            print("CIK nebyl nalezen pro ticker 'AAPL'.")
            
    # conn.commit()
    conn.close()

else:
    print(f"Chyba: {response.status_code}")
