from flask import Flask, request, jsonify, render_template
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
    ticker_symbol = request.form['ticker_symbol']
    metrics = Financial.calculate_financial_metrics(ticker_symbol.upper())
    if (metrics == 1):
        return jsonify("Bad ticker")
    else:
        return jsonify(metrics)

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
