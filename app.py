from flask import Flask, request, jsonify, render_template, url_for
import os
from flask_apscheduler import APScheduler
from src.Utils import logCpuUsage, logRamUsage, deleteLogs, get_files_tree
import yfinance as yf
import threading
from src.RSSdataroma import get_feed_html
from src.metrick import technicalAnalysis
from src.Financial import calculate_financial_metrics, Dividend_Discount_Model, getNews, BasicInfo
from src.DataCrypto import get_crypto_details, bitcoinData, get_top_10_cryptos, FearAndGreesIndex
from src.ProtfolioFromExcel import portfolioTickers
from src.AppLogger import setup_request_logger
from src.HWmonitoring import get_CPU_usage, get_RAM_usage
from src.Graphs import stockGraph
from src.Images import generate_image_from_html
from src.Database import GetDividends_ALL
import datetime as dt
import time

app = Flask(__name__, static_folder='public')
scheduler = APScheduler()

# Vytvoření loggeru při startu aplikace
request_logger = setup_request_logger()


@app.before_request
def log_request_info():
    log_message = f'{request.remote_addr} - - [{dt.datetime.now().strftime("%d/%b/%Y %H:%M:%S")}] "{request.method} {request.path} HTTP/1.1"'
    request_logger.info(log_message)


@app.route('/')
def home():
    return render_template('index.html')

@app.route('/hwmonitoring')
def hwmonitoring():
    return render_template('/hwmonitoring/hwmonitoring.html')

@app.route('/api/cpu-usage', methods=['POST'])
def cpu_usage():
    return jsonify(get_CPU_usage())

@app.route('/api/ram-usage', methods=['POST'])
def ram_usage():
    return jsonify(get_RAM_usage())

@app.route('/api/crypto_fear_and_greed')
def crypto_fear_and_greed():
    data = FearAndGreesIndex()
    return render_template('/crypto/fearAndGreed.html', data=data)


@app.route('/api/deletelogs', methods=['GET'])
def get_deletelogs():
    base_path = os.path.abspath(os.path.dirname('logs'))
    folder_path = os.path.join(base_path, 'logs', 'fileDelete')
    dir_list = os.listdir(folder_path)
    dir_list = sorted(dir_list, reverse=True)  # Seřadíme soubory podle jména (datum v názvu)
    
    # Omezíme počet na max. 4 soubory
    files_to_display = dir_list[:4]
    
    logs_data = []
    
    for filename in files_to_display:
        log_path = os.path.join(folder_path, filename)
        
        try:
            with open(log_path, 'r') as log_file:
                log_lines = log_file.readlines()
            # Zobrazení pouze posledních 10 řádků
            # last_lines = log_lines[-100:]
            logs_data.append({
                'filename': filename,
                'content': log_lines
            })
        except FileNotFoundError:
            logs_data.append({
                'filename': filename,
                'content': ['Log soubor nebyl nalezen.']
            })

    return render_template('/hwmonitoring/logsFile.html', logs=logs_data, name=filename.split('.')[0].split('-')[0] )

@app.route('/api/httprequesteslogs', methods=['GET'])
def get_httprequesteslogs():
    base_path = os.path.abspath(os.path.dirname('logs'))
    folder_path = os.path.join(base_path, 'logs', 'http_requests')
    dir_list = os.listdir(folder_path)
    dir_list = sorted(dir_list, reverse=True)  # Seřadíme soubory podle jména (datum v názvu)
    
    # Omezíme počet na max. 4 soubory
    files_to_display = dir_list[:4]
    
    logs_data = []
    
    for filename in files_to_display:
        log_path = os.path.join(folder_path, filename)
        
        try:
            with open(log_path, 'r') as log_file:
                log_lines = reversed(log_file.readlines())
            # Zobrazení pouze posledních 10 řádků
            # last_lines = log_lines[-10:]
            logs_data.append({
                'filename': filename,
                'content': log_lines
            })
        except FileNotFoundError:
            logs_data.append({
                'filename': filename,
                'content': ['Log soubor nebyl nalezen.']
            })

    return render_template('/hwmonitoring/logsFile.html', logs=logs_data, name=filename.split('.')[0].split('-')[0] )

@app.route('/api/filesTree', methods=['GET'])
def get_files_tree_view():
    logs_folders = ['ram', 'cpu', 'fileDelete', 'http_requests']
    log_files_tree = {}
    
    # Procházení složek a shromažďování dat
    for log in logs_folders:
        folder_path = 'logs/' + log
        files_tree = get_files_tree(folder_path)
        log_files_tree[log] = files_tree  # Přidání dat do slovníku podle složky

    # Získání dat pro obrázky
    img_files_tree = get_files_tree('public/img/graph')

    # Generování URL pro obrázky
    for item in img_files_tree:
        if not item['is_dir']:
            # Vytvoření URL pro obrázek
            item['url'] = url_for('static', filename='img/graph/' + item['name'])
        else:
            item['url'] = None  # Pokud je to složka, URL není potřeba

    # Renderování šablony s předanými daty
    return render_template('/hwmonitoring/filetree.html', log_files_tree=log_files_tree, img_files_tree=img_files_tree)


@app.route('/feed')
def feed():
    feed_html = get_feed_html()
    return feed_html

@app.route('/stock')
def stock():
    return render_template('/financeModels/stock.html')

@app.route('/submit', methods=['POST'])
def submit():
    ticker_symbol = request.form['ticker_symbol'].upper()
    ticker = yf.Ticker(ticker_symbol.upper())
    getNews( ticker )
    # Získání finančních metrik
    metrics = calculate_financial_metrics(ticker, ticker_symbol)

    # Získání výsledků Dividend Discount Modelu (DDM)
    DividendDiscountModel = Dividend_Discount_Model(ticker)

    print(metrics)
    print(metrics)
    

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

            rendered_html = render_template('/financeModels/basicData.html', **common_data)
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
    #  data = portfolioTickers()
    data = GetDividends_ALL()
    print(data)
    return render_template('portfolio.html', data=data)

@app.route('/basicData/<ticker_symbol>', methods=['POST'])
def basicData(ticker_symbol):
    ticker = yf.Ticker(ticker_symbol.upper())
    data = BasicInfo(ticker, ticker_symbol)
    html_output = render_template('/financeModels/basicData.html', **data)
    return jsonify({'html': html_output})


@app.route('/graph/<ticker_symbol>', methods=['POST'])
def route(ticker_symbol):
    file_name = stockGraph(ticker_symbol)
    image_url = url_for('static', filename=f'img/graph/{ file_name }')
    
    # Vytvoření HTML stringu s obrázkem
    img_tag = f'<img src="{image_url}" alt="{ticker_symbol}">'
    
    return jsonify({'html': img_tag })

@app.route('/technicalanalysis/<ticker_symbol>', methods=['POST'])
def technicalanalysis(ticker_symbol):
    data = technicalAnalysis(ticker_symbol.upper())
    html_output = render_template('/financeModels/technicalanalysis.html', **data)
    return jsonify({'html': html_output})

@app.route('/crypto')
def crypto():
    # top_10_cryptos = DataCrypto.get_top_10_cryptos()
    # print(top_10_cryptos)
    # return render_template('crypto.html', cryptos=top_10_cryptos)
    return render_template('crypto.html')

@app.route('/crypto/<crypto_id>')
def crypto_detail(crypto_id):
    print(crypto_id)
    # Získání detailů o kryptoměně z API
    crypto_data = get_crypto_details(crypto_id)
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
    data = bitcoinData(url, ticker_symbol)

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

@app.route('/bitcoinDataOverview/<btn_id>', methods=['POST'])
def bitcoinDataOverviewPOST(btn_id):
    top_10_cryptos = get_top_10_cryptos(btn_id)
    return render_template('/crypto/dashboard.html', cryptos=top_10_cryptos)


@app.route('/crypto/bitcoinDataOverview/<btn_id>', methods=['GET'])
def bitcoinDataOverviewGET(btn_id):
    top_10_cryptos = get_top_10_cryptos(btn_id)
    return render_template('/crypto/dashboard.html', cryptos=top_10_cryptos)

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html')


def run_initial_job():
    # Tato funkce se spustí v samostatném vlákně
    deleteLogs()

def run_img_fear_index_job():
    time.sleep(10)
    print("start")
    with app.app_context():  # Vytvoř aplikační kontext
        html_template = render_template('/crypto/fearAndGreed.html', data=FearAndGreesIndex())
        generate_image_from_html(html_template)



if __name__ == '__main__':
    scheduler.add_job(func=logCpuUsage, trigger='interval', seconds=5, id='cpujob')
    scheduler.add_job(func=logRamUsage, trigger='interval', seconds=5, id='ramjob')
    scheduler.add_job(func=deleteLogs, trigger='cron', hour=2, minute=0, id='logDelete')

    # Spuštění úlohy při startu aplikace v samostatném vlákně
    threading.Thread(target=run_initial_job).start()
    # threading.Thread(target=run_img_fear_index_job).start()

    scheduler.start()
    app.run(host="0.0.0.0", port=8000, debug=True)
