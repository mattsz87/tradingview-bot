from flask import Flask, request
import requests

app = Flask(__name__)

BOT_TOKEN = '7739855211:AAHXtqN3BO4GQPtFg9xprvSUNpPdMbtBPWI'
CHAT_ID = '6622395147'

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.json
    signal = data.get("signal", "BRAK")
    symbol = data.get("symbol", "???")
    price = data.get("price", "???")

    message = f"🔔 SYGNAŁ: {signal} na {symbol} @ {price}"
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": message}
    requests.post(url, data=payload)
    return 'OK', 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
