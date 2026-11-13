import os
import threading
import telebot
from flask import Flask

app = Flask(__name__)

TOKEN = os.environ.get("BOT_TOKEN")
if not TOKEN:
    TOKEN = "আপনার_BOT_TOKEN_এখানে_বসাবেন"

bot = telebot.TeleBot(TOKEN)

@app.route('/')
def home():
    return "Bot cholche!"

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "Hello! Ami sob somoy cholbo! Site Code pathan, jemon: 1809")

@bot.message_handler(func=lambda m: True)
def reply(message):
    text = message.text.strip()
    if text == "1809":
        reply_text = """📶 DHK_X1809 | DHK1809

📡 2G: DHK_X1809
📶 4G: DHK_L1809
🏷️ SHARE: Not Applicable

🏠 Md. Ahsanuddin, Ashulia Khejurbagan, Dhaka.
🏘️ Savar

📞 HO NUMBER:
01715362954

📍 LATLON:
23.88975, 90.32066

🔗 GOOGLE:
https://maps.google.com/?q=23.88975,90.32066

⚡ POWER:
REB Savar
📍 Md. Ahsanuddin, Ashulia Khejurbagan, Dhaka.
📞 01769401071"""
        bot.send_message(message.chat.id, reply_text)
    else:
        bot.send_message(message.chat.id, f"{text} search cholche...")

def run_bot():
    bot.polling(non_stop=True)

threading.Thread(target=run_bot, daemon=True).start()

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
