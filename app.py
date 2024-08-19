from flask import Flask, request, jsonify, render_template
import RSSdataroma
import Financial

app = Flask(__name__, static_folder='public')

@app.route('/')
def home():
    return render_template('index.html', name='World')

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


if __name__ == '__main__':
    app.run(debug=True)
