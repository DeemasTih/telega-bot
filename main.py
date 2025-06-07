from telegram.ext import Updater, CommandHandler
import yfinance as yf
from flask import Flask
from threading import Thread

TOKEN = "ТВОЙ_ТОКЕН_БОТА"
TICKERS = ["NVDA", "PLTR", "BTDR", "CIFR", "BABA", "HOOK", "QURE", "TATT", "ARVN"]

app = Flask('')
@app.route('/')
def home():
    return "бот работает"

def run():
    app.run(host='0.0.0.0', port=8080)

Thread(target=run).start()

def start(update, context):
    update.message.reply_text("👋 Привет! Команды: /help, /check <тикер>, /price <тикер>, /list")

def help_command(update, context):
    update.message.reply_text(
        "/check <тикер> — рекомендация BUY/SELL/HOLD\n"
        "/price <тикер> — текущая цена и средняя\n"
        "/list — список тикеров"
    )

def check(update, context):
    try:
        ticker = context.args[0].upper()
        data = yf.Ticker(ticker).history(period="5d")["Close"]
        last = data.iloc[-1]
        avg = data.mean()
        if last < avg * 0.95:
            text = f"🟢 BUY {ticker}: {last:.2f} < средняя {avg:.2f}"
        elif last > avg * 1.1:
            text = f"🔴 SELL {ticker}: {last:.2f} > средняя {avg:.2f}"
        else:
            text = f"🟡 HOLD {ticker}: {last:.2f} ≈ средняя {avg:.2f}"
        update.message.reply_text(text)
    except Exception as e:
        update.message.reply_text(f"⚠️ Ошибка: {e}")

def price(update, context):
    try:
        ticker = context.args[0].upper()
        data = yf.Ticker(ticker).history(period="5d")["Close"]
        last = data.iloc[-1]
        avg = data.mean()
        update.message.reply_text(f"{ticker} цена: {last:.2f}, средняя: {avg:.2f}")
    except Exception as e:
        update.message.reply_text(f"⚠️ Ошибка: {e}")

def list_tickers(update, context):
    update.message.reply_text("📊 Тикеры:\n" + ", ".join(TICKERS))

updater = Updater(TOKEN, use_context=True)
dp = updater.dispatcher
dp.add_handler(CommandHandler("start", start))
dp.add_handler(CommandHandler("help", help_command))
dp.add_handler(CommandHandler("check", check))
dp.add_handler(CommandHandler("price", price))
dp.add_handler(CommandHandler("list", list_tickers))

updater.start_polling()
