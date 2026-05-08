from flask import Flask, render_template, request
import yfinance as yf

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/calculator', methods=['GET', 'POST'])
def calculator():
    result = None
    breakdown = None
    if request.method == 'POST':
        principal = float(request.form['principal'])
        rate = float(request.form['rate']) / 100
        years = int(request.form['years'])
        contribution = float(request.form['contribution'])

        # Compound interest with monthly contributions
        balance = principal
        total_contributed = principal
        for year in range(years):
            for month in range(12):
                balance += contribution
                total_contributed += contribution
                balance *= (1 + rate / 12)

        result = round(balance, 2)
        breakdown = {
            'contributed': round(total_contributed, 2),
            'interest': round(balance - total_contributed, 2),
            'years': years
        }

    return render_template('calculator.html', result=result, breakdown=breakdown)

@app.route('/stocks', methods=['GET', 'POST'])
def stocks():
    stock_data = None
    error = None

    if request.method == 'POST':
        ticker = request.form['ticker'].upper().strip()
        try:
            stock = yf.Ticker(ticker)
            info = stock.info
            hist = stock.history(period='1mo')

            if hist.empty or 'currentPrice' not in info and 'regularMarketPrice' not in info:
                error = f"Couldn't find data for '{ticker}'. Try a valid ticker like AAPL, MSFT, or TSLA."
            else:
                current_price = info.get('currentPrice') or info.get('regularMarketPrice')
                prev_close = info.get('previousClose', current_price)
                change = current_price - prev_close
                change_pct = (change / prev_close) * 100 if prev_close else 0

                # Get last 30 days of closing prices for the mini chart
                prices = [round(p, 2) for p in hist['Close'].tolist()]
                dates = [d.strftime('%m/%d') for d in hist.index]

                stock_data = {
                    'ticker': ticker,
                    'name': info.get('longName', ticker),
                    'price': round(current_price, 2),
                    'change': round(change, 2),
                    'change_pct': round(change_pct, 2),
                    'is_up': change >= 0,
                    'market_cap': info.get('marketCap'),
                    'sector': info.get('sector', 'N/A'),
                    'prices': prices,
                    'dates': dates,
                    'high_52': info.get('fiftyTwoWeekHigh'),
                    'low_52': info.get('fiftyTwoWeekLow'),
                }
        except Exception as e:
            error = f"Something went wrong looking up '{ticker}'. Please try again."

    return render_template('stocks.html', stock=stock_data, error=error)

@app.route('/learn')
def learn():
    return render_template('learn.html')

if __name__ == '__main__':
    app.run(debug=True)