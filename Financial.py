import yfinance as yf
import numpy as np
import pandas as pd

def CashflowGrowth(fcf):
    fcfGrowth = []
    for index, cash in enumerate(fcf):
        if index + 1 >= len(fcf):
            break
        fcfGrowth.append((fcf[index + 1] - cash) / cash)
    return fcfGrowth

def CashflowGrowthAverage(fcfGrowth):
    return sum(fcfGrowth) / len(fcfGrowth)

def CashflowFutureGrowth(cashflow, GrowthAverage):
    LastCashFlow = cashflow[-1]
    Futurefcf = []
    for i in range(1, 11):
        newCashFlow = LastCashFlow * (1 + GrowthAverage)
        Futurefcf.append(newCashFlow)
        LastCashFlow = newCashFlow
    return Futurefcf

def PVflowFutureGrowth(cashflow, DiscountRate):
    Futurefcf = []
    for i in range(1, 11):
        newCashFlow = cashflow[i-1] / (1 + DiscountRate)**i
        Futurefcf.append(newCashFlow)
    return Futurefcf

# Finanční ukazatele
def get_financial_ratios(info):
    ratios = {
        "Current Ratio": info.get("currentRatio", "N/A"),
        "Quick Ratio": info.get("quickRatio", "N/A"),
        "Debt to Equity Ratio": info.get("debtToEquity", "N/A"),
        "Interest Coverage Ratio": info.get("interestCoverage", "N/A"),
        "Gross Margin": info.get("grossMargins", "N/A") * 100,
        "Operating Margin": info.get("operatingMargins", "N/A") * 100,
        "Net Margin": info.get("profitMargins", "N/A") * 100
    }
    return ratios


def formatMarketCap(marketCap):
    if marketCap >= 1_000_000_000_000:
        return f"{marketCap / 1_000_000_000_000:.2f} T"
    elif marketCap >= 1_000_000_000:
        return f"{marketCap / 1_000_000_000:.2f} B"
    elif marketCap >= 1_000_000:
        return f"{marketCap / 1_000_000:.2f} M"
    else:
        return str(marketCap)




def calculate_financial_metrics(ticker, ticker_symbol):
    try:
        info = ticker.info
        f = open("log.txt", "a")
        f.write(str(info))
        # print(info)
        CashEquivalents = ticker.balance_sheet.loc["Total Assets"].to_list()[0]
        print("Cash Equivalents:", CashEquivalents)
        f.write(str(CashEquivalents))
        # Použijeme průměrný růst FCF místo růstu zisků
        cashflow = ticker.cashflow
        fcf = cashflow.loc["Free Cash Flow"].dropna().to_list()
        print("Free Cash Flow", fcf)
        fcf.reverse()
        print("Free Cash Flow", fcf)
        fcfGrowth = CashflowGrowth(fcf)
        print("FCF Growth:", fcfGrowth)

        GrowthAverage = CashflowGrowthAverage(fcfGrowth)
        print("Growth Average:", GrowthAverage)

        # Použijeme konzervativnější růst pro extrapolaci budoucích peněžních toků
        fcf.reverse()
        FutureFCF = CashflowFutureGrowth(fcf, GrowthAverage)
        print("Future FCF:", FutureFCF)

        PerpetualGrowthRate = 0.025  # 2.5% jako desetinné číslo
        DiscountRate = 0.08  # 8% jako desetinné číslo

        terminalValue = (FutureFCF[-1] * (1 + PerpetualGrowthRate)) / (DiscountRate - PerpetualGrowthRate)
        print("Terminal Value:", terminalValue)

        # Terminální hodnota musí být diskontována zpět do současnosti
        PVofTerminalValue = terminalValue / (1 + DiscountRate)**10

        PVofFutureFCF = PVflowFutureGrowth(FutureFCF, DiscountRate)
        print("PV of Future FCF:", PVofFutureFCF)

        SumOfFCF = sum(PVofFutureFCF) + PVofTerminalValue
        Debt = info["totalDebt"]

        print("Sum of FCF:", SumOfFCF)

        EquityValue = SumOfFCF - Debt + CashEquivalents
        print("Equity Value:", EquityValue)

        shares = info["sharesOutstanding"]
        print("Shares Outstanding:", shares)

        DCFprice = EquityValue / shares
        print("DCF Price per Share:", DCFprice)

        print("\n\n\n")
        cashflow = ticker.cashflow
        balance_sheet = ticker.balance_sheet
        income_statement = ticker.financials

        # Výpočet a tisk finančních ukazatelů
        financial_ratios = get_financial_ratios(info)
        print("Financial Ratios:")
        for ratio, value in financial_ratios.items():
            print(f"{ratio}: {value}")

        # Výpočet růstu tržeb a zisků
        revenue_growth = info.get("revenueGrowth", "N/A") * 100
        earnings_growth = info.get("earningsGrowth", "N/A") * 100
        print(f"Revenue Growth: {revenue_growth}%")
        print(f"Earnings Growth: {earnings_growth}%")

        # Získejte peněžní toky a vypočtěte DCF
        fcf = cashflow.loc["Free Cash Flow"].dropna().to_list()
        fcf.reverse()
        print(f"Free Cash Flow: {fcf}")
        print("tohle je symbol  "+info.get('symbol', 0))
        f.close()
        return {
            'TickerSymbol' : info.get('symbol', 0),
            'sector' : info.get("sector", 0),
            'longBusinessSummary' : info.get('longBusinessSummary', 0),
            'longName': info.get('longName', 0),
            'marketCap' : formatMarketCap(info.get('marketCap', 0)),
            'fiftyTwoWeekLow' : info.get('fiftyTwoWeekLow', 0),
            'fiftyTwoWeekHigh' : info.get('fiftyTwoWeekHigh', 0),
            'currentPrice': info.get('currentPrice', 0),
            'Cash Equivalents': info.get("cash", 0),
            'Free Cash Flow': fcf,
            'FCF Growth': fcfGrowth,
            'Growth Average': GrowthAverage,
            'Future FCF': FutureFCF,
            'Terminal Value': terminalValue,
            'PV of Future FCF': PVofFutureFCF,
            'Sum of FCF': SumOfFCF,
            'Equity Value': EquityValue,
            'Shares Outstanding': shares,
            'DCF Price per Share': DCFprice,
            'Financial Ratios': financial_ratios,
            'Revenue Growth': revenue_growth,
            'Earnings Growth': earnings_growth,
            'Target High Price': info.get('targetHighPrice', 0),
            'Target Low Price': info.get('targetLowPrice', 0),
            'Target Mean Price': info.get('targetMeanPrice', 0),
            'Target Median Price': info.get('targetMedianPrice', 0),
            'Recommendation Mean': info.get('recommendationMean', 0),
            'Recommendation Key': info.get('recommendationKey', 0),
            'Number of Analyst Opinions': info.get('numberOfAnalystOpinions', 0)
        }

    except Exception as e:
        return {'error': str(e)}


def Dividend_Discount_Model(ticker):
    if 'dividendRate' not in ticker.info:
        print("Dividend rate not available for this ticker.")
        return None
    
    stock = ticker.actions
    stock_split = stock["Stock Splits"].to_numpy()
    stock_split_replaced = np.where(stock_split == 0, 1, stock_split)
    stock_split_comp = np.cumprod(stock_split_replaced, axis=0)
    
    stock["stocksplit_adj"] = stock_split_comp.tolist()
    stock["div_adj"] = stock["Dividends"] * stock["stocksplit_adj"]
    stock['year'] = stock.index.year
    stock_grp = stock.groupby(by=["year"]).sum()
    stock_grp["div_PCT_Change"] = stock_grp["div_adj"].pct_change(fill_method=None)
    
    median_growth = stock_grp["div_PCT_Change"].median()
    lst_Div = stock_grp.at[2021,'Dividends']
    exp_future_div = round(lst_Div * (1 + median_growth), 2)
    risk_free_rate = 0.03
    mkt_return = .11
    MKT_Risk_prem = mkt_return - risk_free_rate
    beta = ticker.info["beta"]
    COE = round(beta * MKT_Risk_prem + risk_free_rate, 4)
    fair_sharePrice = round(exp_future_div / ( median_growth - COE), 2)
    stock_price = ticker.history(period="1d")
    stock_price_close = round(stock_price.iloc[0]['Close'], 4)
    expected_gain_loss = fair_sharePrice / stock_price_close - 1
    expected_gain_loss = "{:.0%}".format(expected_gain_loss)

    # Vrátíme relevantní data
    return {
        'ticker': ticker.ticker,
        'stock_price_close': stock_price_close,
        'fair_share_price': fair_sharePrice,
        'expected_gain_loss': expected_gain_loss,
        'lst_div': lst_Div,
        'median_growth': round(median_growth * 100, 2),  # přepočet na procenta
        'coe': round(COE * 100, 2),  # přepočet na procenta
        'exp_future_div': exp_future_div,
        'stock_grp': stock_grp['div_adj'].to_dict()  # rok a odpovídající dividendy
    }