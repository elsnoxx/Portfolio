import yfinance as yf
import psycopg2
from psycopg2 import sql
import time

# Připojení k databázi PostgreSQL
def connect_to_db():
    conn = psycopg2.connect(
        dbname="porfolio",
        user="su",
        password="pi",
        host="192.168.88.158",
        port="5432"
    )
    return conn

# Funkce pro uložení společnosti do databáze
def insert_company(conn, name, ticker, sector, market_cap):
    with conn.cursor() as cur:
        cur.execute(
            """
            INSERT INTO companies (name, ticker, sector, market_cap)
            VALUES (%s, %s, %s, %s)
            ON CONFLICT (ticker) DO NOTHING
            RETURNING id;
            """, (name, ticker, sector, market_cap)
        )
        return cur.fetchone()[0]  # Vrať ID nově vložené společnosti

# Funkce pro uložení finančních údajů
def insert_financials(conn, company_id, year, revenue, expenses, net_income, dividend):
    with conn.cursor() as cur:
        cur.execute(
            """
            INSERT INTO financials (company_id, year, revenue, expenses, net_income, dividend)
            VALUES (%s, %s, %s, %s, %s, %s)
            ON CONFLICT (company_id, year) DO NOTHING;
            """, (company_id, year, revenue, expenses, net_income, dividend)
        )

# Funkce pro uložení historických cen
def insert_historical_prices(conn, company_id, data):
    with conn.cursor() as cur:
        for date, prices in data.items():
            cur.execute(
                """
                INSERT INTO historical_prices (company_id, date, open_price, close_price, high_price, low_price, volume)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
                ON CONFLICT (company_id, date) DO NOTHING;
                """, (company_id, date, prices['Open'], prices['Close'], prices['High'], prices['Low'], prices['Volume'])
            )

# Funkce pro uložení dividend
def insert_dividends(conn, company_id, dividends):
    with conn.cursor() as cur:
        for div in dividends:
            cur.execute(
                """
                INSERT INTO dividends (company_id, ex_date, amount)
                VALUES (%s, %s, %s);
                """, (company_id, div['Ex/EFF DATE'], div['DIVIDEND AMOUNT'])
            )

# Funkce pro získání tickerů
def get_tickers(conn):
    with conn.cursor() as cur:
        cur.execute(
            """
            SELECT DISTINCT SUBSTRING(details FROM 1 FOR POSITION('/' IN details) - 1) AS stock_symbol FROM trades;
            """
        )
        tickers = cur.fetchall()
        return [ticker[0] for ticker in tickers]  # Vraťte seznam tickerů jako řetězce

# Hlavní funkce pro získání dat a jejich uložení
def main():
    start = time.time()
    conn = connect_to_db()
    tickers = get_tickers(conn)
    
    print("Získané tickery:", tickers)

    for ticker in tickers:
        stock = yf.Ticker(ticker)

        # Získání základních údajů o společnosti
        info = stock.info
        name = info.get('longName', 'N/A')
        sector = info.get('sector', 'N/A')
        market_cap = info.get('marketCap', 0)

        # Uložení společnosti do databáze
        company_id = insert_company(conn, name, ticker, sector, market_cap)

        # Získání a uložení finančních údajů
        financials = stock.financials.transpose()  # Transponuje DataFrame
        for year in financials.index:
            year_as_int = year.year  # Ujistěte se, že `year` je typ `integer`
            insert_financials(conn, company_id, year_as_int, 
                              financials.loc[year]['Total Revenue'], 
                              financials.loc[year]['Gross Profit'], 
                              financials.loc[year]['Net Income'], 
                              info.get('dividendRate', 0))

        # Získání historických cen
        historical_data = stock.history(period="5y")  # Získání historických dat za posledních 5 let
        insert_historical_prices(conn, company_id, historical_data.to_dict(orient='index'))

        # Získání dividend
        dividends = stock.dividends.to_frame().reset_index().rename(columns={0: 'DIVIDEND AMOUNT'})
        print(dividends)
        insert_dividends(conn, company_id, dividends.to_dict(orient='records'))

    conn.commit()  # Uložení změn do databáze
    conn.close()  # Uzavření připojení
    konec = time.time()
    print("Cyklus běžel:", konec - start, "sekund")

if __name__ == "__main__":
    main()
