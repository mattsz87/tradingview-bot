from flask import Flask, request
import requests
from datetime import datetime

app = Flask(__name__)

BOT_TOKEN = '7739855211:AAHXtqN3BO4GQPtFg9xprvSUNpPdMbtBPWI'
CHAT_ID = '6622395147'

# Konfiguracja RR i mapa SL per instrument
RR_RATIO = 1.5  # Mniej TP-outów, wyższa skuteczność
SL_PIPS_MAP = {
    "EURUSD": 15,
    "GBPUSD": 20,
    "GBPJPY": 25,
    "XAUUSD": 25,
    "NAS100": 30,
    "ETHUSD": 40,
    "BTCUSD": 50
}

@app.route('/webhook', methods=['POST'])
def webhook():
    import json
    data = json.loads(request.data)
    print(f"[{datetime.now()}] Odebrano sygnał: {data}")

    signal = data.get("signal", "BRAK").upper()
    symbol = data.get("symbol", "???").upper()
    price = float(data.get("price", 0))

    # Dopasuj SL_PIPS na podstawie symbolu
    SL_PIPS = SL_PIPS_MAP.get(symbol, 20)  # default 20

    # pip_value zależnie od instrumentu
    pip_value = 0.1  # domyślnie
    if "USD" in symbol and "JPY" not in symbol and "XAU" not in symbol and "NAS" not in symbol:
        pip_value = 0.0001
    elif "JPY" in symbol:
        pip_value = 0.01
    elif "ETH" in symbol or "BTC" in symbol:
        pip_value = 1
    elif "NAS" in symbol or "US30" in symbol:
        pip_value = 1.0
    elif "XAU" in symbol:
        pip_value = 0.1

    # Oblicz SL i TP
    if signal == "BUY":
        sl = round(price - (SL_PIPS * pip_value), 5)
        tp = round(price + (SL_PIPS * pip_value * RR_RATIO), 5)
    elif signal == "SELL":
        sl = round(price + (SL_PIPS * pip_value), 5)
        tp = round(price - (SL_PIPS * pip_value * RR_RATIO), 5)
    else:
        sl = tp = "?"

    message = (
        f"🔔 SYGNAŁ: {signal} na {symbol} @ {price}\n"
        f"🛑 SL: {sl}\n"
        f"🎯 TP: {tp}"
    )

    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": message}

    try:
        response = requests.post(url, data=payload)
        print(f"[{datetime.now()}] Telegram response: {response.status_code}")
    except Exception as e:
        print(f"[{datetime.now()}] Błąd przy wysyłaniu do Telegrama: {e}")

    return 'OK', 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
