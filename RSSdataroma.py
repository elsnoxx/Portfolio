import feedparser
import re

def extract_tickers(text):
    pattern = r'<b>(Bought|Added to):</b> ([A-Z\.]+(?:\s[A-Z\.]+)*)<br />'
    matches = re.findall(pattern, text)
    tickers = {'Bought': [], 'Added to': []}
    for match in matches:
        category, tickers_str = match
        tickers[category].extend(tickers_str.split())
    return tickers

def format_tickers(tickers):
    formatted_output = []
    if tickers['Bought']:
        bought_line = '<b>Bought:</b> ' + ' '.join(f'<a href="https://finance.yahoo.com/quote/{ticker}/" target="_blank" rel="noopener noreferrer">{ticker}</a>' for ticker in tickers['Bought'])
        formatted_output.append(bought_line)
    if tickers['Added to']:
        added_to_line = '<b>Added to:</b> ' + ' '.join(f'<a href="https://finance.yahoo.com/quote/{ticker}/" target="_blank" rel="noopener noreferrer">{ticker}</a>' for ticker in tickers['Added to'])
        formatted_output.append(added_to_line)
    return "<br />".join(formatted_output)

def get_feed_html():
    url = 'https://feeds.feedburner.com/dataroma'
    feed = feedparser.parse(url)
    html_output = []

    html_output.append(f"<h1>Portfolio updates</h1>")
    html_output.append(f"<p>{feed.feed.description}</p>")

    for entry in feed.entries:
        html_output.append(f'<div class="feed_info card">')
        html_output.append(f'<div class="card-body">')
        html_output.append(f'<h3 class="card-title" >{entry.title}</h3>')
        html_output.append(f'<a href="{entry.link}" target="_blank" rel="noopener noreferrer">link</a><br>')
        html_output.append(f'<div class="card-text">')
        tickers = extract_tickers(entry.description)
        formatted_html = format_tickers(tickers)
        html_output.append(formatted_html)
        html_output.append(f"</div>")
        html_output.append(f"</div>")
        html_output.append(f"</div>")

    return ''.join(html_output)
