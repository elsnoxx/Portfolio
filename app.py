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

@app.route('/stock')
def stock():
    return render_template('/financeModels/stock.html')

@app.route('/submit', methods=['POST'])
def submit():
    ticker_symbol = request.form['ticker_symbol'].upper()
    ticker = yf.Ticker(ticker_symbol.upper())
    
    # Získání finančních metrik
    metrics = Financial.calculate_financial_metrics(ticker, ticker_symbol)

    # Získání výsledků Dividend Discount Modelu (DDM)
    DividendDiscountModel = Financial.Dividend_Discount_Model(ticker)

    print(metrics)
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
        # rendered_html = render_template('/financeModels/result.html', **common_data)
        # return jsonify({'html': rendered_html})
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
                'currentPrice': metrics['currentPrice'],
                'stock_grp': DividendDiscountModel['stock_grp'].items()
            }

            # Data specifická pro DDM
            ddm_data = {
                'stock_price_close': DividendDiscountModel['stock_price_close'],
                'fair_share_price': DividendDiscountModel['fair_share_price'],
                'expected_gain_loss': DividendDiscountModel['expected_gain_loss'],
                'lst_div': DividendDiscountModel['lst_div'],
                'median_growth': DividendDiscountModel['median_growth'],
                'coe': DividendDiscountModel['coe'],
                'exp_future_div': DividendDiscountModel['exp_future_div']
            }


            rendered_html_dcf = render_template('/financeModels/DCF.html', **dcf_data)

            rendered_html = render_template('/financeModels/result.html', **common_data)
            return jsonify({'html': rendered_html + rendered_html_dcf})
        else:
            rendered_html = render_template('/financeModels/result.html',
                                            **common_data,
                                            stock_price_close=None,
                                            fair_share_price=None,
                                            expected_gain_loss=None,
                                            lst_div=None,
                                            median_growth=None,
                                            coe=None,
                                            exp_future_div=None)
            
        
            return jsonify({'html': rendered_html })

@app.route('/portfolio')
def portfolio():
    return render_template('portfolio.html')

@app.route('/crypto')
def crypto():
    top_10_cryptos = DataCrypto.get_top_10_cryptos()
    # print(top_10_cryptos)
    return render_template('crypto.html', cryptos=top_10_cryptos)

@app.route('/crypto/<crypto_id>')
def crypto_detail(crypto_id):
    print(crypto_id)
    # Získání detailů o kryptoměně z API
    crypto_data = DataCrypto.get_crypto_details(crypto_id)
    if (crypto_data == 1):
        return render_template('/general/toomanyrequests.html')
    if (crypto_data == 2):
        return render_template('/general/notfound.html')
    else:
        return render_template('/crypto/infoCrypto.html', crypto=crypto_data)

@app.route('/bitcoinData', methods=['POST'])
def bitcoinData():
    ticker_symbol = request.form['crypto_symbol'].upper()
    url = "https://api.coingecko.com/api/v3/coins/bitcoin"
    data = DataCrypto.bitcoinData(url, ticker_symbol)

    rendered_html = render_template('/crypto/infoCrypto.html', 
                                    symbol=data['symbol'], 
                                    current_price=data['current_price'], 
                                    high_24h = data['high_24h'], 
                                    low_24h = data['low_24h'], 
                                    price_change_percentage_24h = data['price_change_percentage_24h'],
                                    ath_change_percentage = data['ath_change_percentage'],
                                    ath = data['ath'], 
                                    market_cap = data['market_cap'])
    return jsonify({'html': rendered_html })
    # return jsonify(data)

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html')

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
    # app.run(debug=True)
