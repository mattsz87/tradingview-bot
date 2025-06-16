from flask import Flask, request
import telegram

app = Flask(__name__)

BOT_TOKEN = '7739855211:AAHXtqN3BO4GQPtFg9xprvSUNpPdMbtBPWI'
CHAT_ID = 6622395147

bot = telegram.Bot(token=BOT_TOKEN)

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.json
    signal = data.get("signal", "BRAK")
    symbol = data.get("symbol", "???")
    price = data.get("price", "???")

    message = f"🔔 SYGNAŁ: {signal} na {symbol} @ {price}"
    bot.send_message(chat_id=CHAT_ID, text=message)
    return 'OK', 200

if __name__ == '__main__':
    app.run()
