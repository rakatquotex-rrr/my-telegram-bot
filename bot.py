import os
import threading
import telebot
from flask import Flask

TOKEN = os.environ.get("BOT_TOKEN")
bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

@app.route('/')
def home():
    return "Bot is Alive!"

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "Hello! Ami sob somoy cholbo! Site Code pathan, jemon: 1809")

@bot.message_handler(func=lambda m: True)
def handle_all(message):
    code = message.text.strip()
    if code == "1809":
        bot.reply_to(message, "1809 | DHK_W1809 | DHK1809\nSavar Bazar\nBanglalink Site - Found!")
    else:
        bot.reply_to(message, f"{code} search cholche...\nSite Code: {code}")

def run_bot():
    bot.infinity_polling()

if __name__ == "__main__":
    threading.Thread(target=run_bot).start()
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
