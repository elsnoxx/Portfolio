from flask import Flask, request, jsonify, render_template
import yfinance as yf
import RSSdataroma
import Financial
import DataCrypto

app = Flask(__name__, static_folder='public')

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/feed')
def feed():
    feed_html = RSSdataroma.get_feed_html()
    return feed_html


@app.route('/submit', methods=['POST'])
def submit():
    ticker_symbol = request.form['ticker_symbol'].upper()
    ticker = yf.Ticker(ticker_symbol.upper())
    
    # Získání finančních metrik
    metrics = Financial.calculate_financial_metrics(ticker, ticker_symbol)

    # Získání výsledků Dividend Discount Modelu (DDM)
    DividendDiscountModel = Financial.Dividend_Discount_Model(ticker)

    print(metrics)
    common_data = {
                'TickerSymbol': metrics['TickerSymbol'],
                'sector': metrics['sector'],
                'longBusinessSummary': metrics['longBusinessSummary'],
                'longName': metrics['longName'],
                'marketCap': metrics['marketCap'],
                'fiftyTwoWeekLow': metrics['fiftyTwoWeekLow'],
                'fiftyTwoWeekHigh': metrics['fiftyTwoWeekHigh'],
                'currentPrice': metrics['currentPrice'],
                'shares_outstanding': metrics['Shares Outstanding'],
                'target_high_price': metrics['Target High Price'],
                'target_low_price': metrics['Target Low Price'],
                'target_mean_price': metrics['Target Mean Price'],
                'target_median_price': metrics['Target Median Price'],
                'recommendation_mean': metrics['Recommendation Mean'],
                'recommendation_key': metrics['Recommendation Key'],
                'number_of_analyst_opinions': metrics['Number of Analyst Opinions']
            }

    if metrics == 1:
        return jsonify({"error": "Bad ticker"})
    else:
        if DividendDiscountModel is not None:

            # Data specifická pro DCF.html
            dcf_data = {
                'Terminal_Value': metrics['Terminal Value'],
                'Sum_of_FCF': metrics['Sum of FCF'],
                'Equity_Value': metrics['Equity Value'],
                'Shares_Outstanding': metrics['Shares Outstanding'],
                'Revenue_Growth': metrics['Revenue Growth'],
                'Earnings_Growth': metrics['Earnings Growth'],
                'dcf_price_per_share': metrics['DCF Price per Share'],
                'currentPrice': metrics['currentPrice']
            }

            # Data specifická pro DDM
            ddm_data = {
                'stock_price_close': DividendDiscountModel['stock_price_close'],
                'fair_share_price': DividendDiscountModel['fair_share_price'],
                'expected_gain_loss': DividendDiscountModel['expected_gain_loss'],
                'lst_div': DividendDiscountModel['lst_div'],
                'median_growth': DividendDiscountModel['median_growth'],
                'coe': DividendDiscountModel['coe'],
                'exp_future_div': DividendDiscountModel['exp_future_div'],
                'stock_grp': DividendDiscountModel['stock_grp'].items()
            }


            rendered_html_dcf = render_template('/financeModels/DCF.html', **dcf_data)

            rendered_html = render_template('/financeModels/result.html', **common_data, **ddm_data)
        else:
            rendered_html = render_template('/financeModels/result.html',
                                            **common_data,
                                            stock_price_close=None,
                                            fair_share_price=None,
                                            expected_gain_loss=None,
                                            lst_div=None,
                                            median_growth=None,
                                            coe=None,
                                            exp_future_div=None,
                                            stock_grp='None')

        return jsonify({'html': rendered_html + rendered_html_dcf})





@app.route('/portfolio')
def portfolio():
    return render_template('portfolio.html')

@app.route('/crypto')
def crypto():
    return render_template('crypto.html')

@app.route('/bitcoinData')
def bitcoinData():
    url = "https://api.coingecko.com/api/v3/coins/bitcoin"
    data = DataCrypto.bitcoinData(url)
    return jsonify(data)

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html')

if __name__ == '__main__':
    app.run(debug=True)
