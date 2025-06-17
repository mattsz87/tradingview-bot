from flask import Flask, request
import requests

app = Flask(__name__)

BOT_TOKEN = '7739855211:AAHXtqN3BO4GQPtFg9xprvSUNpPdMbtBPWI'
CHAT_ID = '6622395147'

# Konfiguracja strategii
RR_RATIO = 2.0  # Risk:Reward
SL_PIPS = 15    # stały SL w pipsach (np. 15 = 1.5 USD)

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.json
    signal = data.get("signal", "BRAK")
    symbol = data.get("symbol", "???")
    price = float(data.get("price", 0))

    # Oblicz TP i SL wg strategii
    if signal == "BUY":
        sl = round(price - (SL_PIPS / 10), 2)
        tp = round(price + (SL_PIPS / 10) * RR_RATIO, 2)
    elif signal == "SELL":
        sl = round(price + (SL_PIPS / 10), 2)
        tp = round(price - (SL_PIPS / 10) * RR_RATIO, 2)
    else:
        sl = tp = "?"

    message = (
        f"🔔 SYGNAŁ: {signal} na {symbol} @ {price}\n"
        f"🛑 SL: {sl}\n"
        f"🎯 TP: {tp}"
    )
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": message}
    requests.post(url, data=payload)
    return 'OK', 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
