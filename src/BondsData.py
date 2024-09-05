import yfinance as yf
import matplotlib.pyplot as plt


treasury_rate_data = yf.download("^IRX ^FVX ^TNX ^TYX", start="2022-12-29", end=None)
df = treasury_rate_data["Adj Close"]

# df.info()
df = df.copy()
df['Close Date'] = df.index.strftime('%Y-%m-%d')

# Rename column names
new_column_names = {'^IRX': '13-week T-Bill',
                    '^FVX': '5-yr Treasury',
                    '^TNX': '10-yr Treasury',
                    '^TYX': '30-yr Treasury'}

df = df.rename(columns = new_column_names)

# Output columns
output_list = ['13-week T-Bill', '5-yr Treasury', '10-yr Treasury', '30-yr Treasury']


plt.figure(figsize=(6, 3))
plt.plot(df['13-week T-Bill'], label='13-week T-Bill', color='darkblue')
# plt.plot(df.index, df['5-yr Treasury'], label='5-yr Treasury', color='orange')
# plt.plot(df.index, df['10-yr Treasury'], label='10-yr Treasury', color='tomato')
# plt.plot(df.index, df['30-yr Treasury'], label='30-yr Treasury', color='darkred')
# plt.xlabel('Date')
# plt.ylabel('Yield')
# plt.legend()
plt.gca().spines['top'].set_visible(False)
plt.gca().spines['right'].set_visible(False)
plt.gca().spines['left'].set_visible(False)
plt.gca().spines['bottom'].set_visible(False)
plt.xticks([])
plt.yticks([])
# Žádná legenda, žádné mřížky
plt.grid(False)
plt.legend().set_visible(False)

# plt.grid(True)
plt.savefig('C:\\Users\\admin\\Documents\\GitHub\\Portfolio\\public\\img\\plt\\13-week T-Bill.png')
# plt.show()

print(df)