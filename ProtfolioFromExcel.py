import pandas as pd

# Cesta k tvému Excel souboru
excel_file = r'etoro-account-statement.csv'

# Načtení Excel souboru do DataFrame
df = pd.read_csv(excel_file)

# Výpis prvních několika řádků (pro kontrolu)
# print(df.head())

for index, row in df.iterrows():
    if (row["Type"] != "Dividend" and row["Type"] != 'Edit Stop Loss' and row["Amount"] == '-'):
        print(f"-------------------------------------------------------")
        print(f"Hodnota ve sloupci 'Date': {row["Date"]}")
        print(f"Hodnota ve sloupci 'Type': {row["Type"]}")
        print(f"Hodnota ve sloupci 'Details': {row["Details"]}")
        if (row["Amount"] != '-' or row["Amount"] != ' '):
            print(f"Hodnota ve sloupci 'Amount': {float(row["Amount"])}")
        
        
        print(f"Hodnota ve sloupci 'Units': {row["Units"]}")
        
    # if (row["Type"] == "Dividend"):
    #     print(f"-------------------------------------------------------")
    #     print(f"Hodnota ve sloupci 'Date': {row["Date"]}")
    #     print(f"Hodnota ve sloupci 'Type': {row["Type"]}")
    #     print(f"Hodnota ve sloupci 'Details': {row["Details"]}")
    #     print(f"Hodnota ve sloupci 'Amount': {row["Amount"]}")
        
    
    
    
