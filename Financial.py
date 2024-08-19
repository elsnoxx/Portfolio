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

def calculate_financial_metrics(ticker_symbol):
    try:
        # Nastavíme ticker symbol
        ticker = yf.Ticker(ticker_symbol)

        info = ticker.info
        CashEquivalents = ticker.balance_sheet.loc["Cash Cash Equivalents And Short Term Investments"].to_list()[0]
        print("Cash Equivalents:", CashEquivalents)

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

        return {
            'Ticker' : ticker_symbol,
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
            'Earnings Growth': earnings_growth
        }

    except Exception as e:
        return {'error': str(e)}
