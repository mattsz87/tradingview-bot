from flask import Flask, request
import requests

app = Flask(__name__)

# === KONFIGURACJA ===
BOT_TOKEN = '7739855211:AAHXtqN3BO4GQPtFg9xprvSUNpPdMbtBPWI'
CHAT_ID = '6622395147'
RR_RATIO = 2.0      # Risk:Reward ratio (np. 2 = 1:2)
SL_PIPS = 15        # Stały SL w pipsach (np. 15 = 1.5 USD)

# === GŁÓWNY WEBHOOK ===
@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.json
    signal = data.get("signal", "BRAK")
    symbol = data.get("symbol", "???")
    price = float(data.get("price", 0))

    # Wylicz SL i TP
    if signal == "BUY":
        sl = round(price - (SL_PIPS / 10), 2)
        tp = round(price + (SL_PIPS / 10) * RR_RATIO, 2)
    elif signal == "SELL":
        sl = round(price + (SL_PIPS / 10), 2)
        tp = round(price - (SL_PIPS / 10) * RR_RATIO, 2)
    else:
        sl = tp = "?"

    # Wiadomość do Telegrama
    message = (
        f"🔔 SYGNAŁ: {signal} na {symbol} @ {price}\n"
        f"🛑 SL: {sl}\n"
        f"🎯 TP: {tp}"
    )

    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": message}

    try:
        response = requests.post(url, data=payload)
        return 'OK', 200
    except Exception as e:
        return f'Error: {e}', 500

# === URUCHOMIENIE ===
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
