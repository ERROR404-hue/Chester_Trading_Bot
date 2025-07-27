from flask import Flask, request
import ccxt

app = Flask(__name__)

@app.route('/')
def home():
    return 'Trading bot is live!'

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.json
    print(f"Received alert: {data}")

    # Example logic (customize this later)
    exchange = ccxt.binance({
        'apiKey': 'YOUR_API_KEY',
        'secret': 'YOUR_SECRET_KEY',
    })

    try:
        symbol = data.get("symbol", "BTC/USDT")
        side = data.get("side", "buy")
        amount = float(data.get("amount", 0.001))

        if side == "buy":
            order = exchange.create_market_buy_order(symbol, amount)
        else:
            order = exchange.create_market_sell_order(symbol, amount)

        return {'status': 'order executed', 'details': order}, 200
    except Exception as e:
        return {'status': 'error', 'message': str(e)}, 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
