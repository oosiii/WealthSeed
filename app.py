from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/calculator', methods=['GET', 'POST'])
def calculator():
    result = None
    if request.method == 'POST':
        principal = float(request.form['principal'])
        rate = float(request.form['rate']) / 100
        years = int(request.form['years'])
        contribution = float(request.form['contribution'])
        
        # Compound interest with monthly contributions
        balance = principal
        for year in range(years):
            for month in range(12):
                balance += contribution
                balance *= (1 + rate / 12)
        
        result = round(balance, 2)
    
    return render_template('calculator.html', result=result)

if __name__ == '__main__':
    app.run(debug=True)