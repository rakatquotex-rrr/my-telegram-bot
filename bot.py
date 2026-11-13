import os
import threading
import re
import pandas as pd
from flask import Flask
import telebot

TOKEN = os.environ.get("BOT_TOKEN")
bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

# Excel load
df = pd.read_excel("All_Sites_Full_Details.xlsx", sheet_name="All Sites", dtype=str).fillna("")

def find_site(text):
    text = text.strip().upper()
    # 1809 -> DHK1809 বানানো
    num = re.sub(r'[^0-9]', '', text)
    if not num:
        return None
    # Generic ID দিয়ে খোঁজা
    for _, row in df.iterrows():
        generic = str(row.get("Generic ID", "")).upper()
        if num in generic or generic.endswith(num):
            return row
    return None

def format_reply(row):
    generic = row.get("Generic ID", "")
    g2 = row.get("2G Site ID", "")
    g4 = row.get("4G Site ID", "")
    share = row.get("Share Site ID", "") or "Not Applicable"
    addr = row.get("Address", "")
    thana = row.get("Thana", "")
    ho = row.get("House Owner Number", "") or "Not Available"
    latlon = row.get("Lat Long (cleaned)", "")
    gmap = row.get("Direct Google Location", "")
    return f"""📶 {g2} | {generic}

📡 2G: {g2}
📶 4G: {g4}
🏷️ SHARE: {share}

🏠 {addr}
🏘️ {thana}

📞 HO NUMBER:
{ho}

📍 LATLON:
{latlon}

🔗 GOOGLE:
{gmap}"""

@app.route('/')
def home():
    return "Bot is Live!"

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "Hello! Site Code pathan, jemon: 1809 / DHK1809")

@bot.message_handler(func=lambda m: True)
def reply(message):
    row = find_site(message.text)
    if row is not None:
        bot.send_message(message.chat.id, format_reply(row))
    else:
        bot.send_message(message.chat.id, f"{message.text} - Site pai nai! Thik code den, jemon: 1809")

def run_bot():
    bot.polling(non_stop=True)

if __name__ == "__main__":
    threading.Thread(target=run_bot, daemon=True).start()
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
