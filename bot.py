import os
import threading
import re
import pandas as pd
from flask import Flask
import telebot

TOKEN = os.environ.get("BOT_TOKEN")
bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

df = pd.read_excel("All_Sites_Full_Details.xlsx", sheet_name="All Sites", dtype=str).fillna("")

POWER_BY_SITE = {
    "X0094": "REB Ashulia", "X3878": "REB Ashulia", "X3372": "REB Ashulia", "X4211": "REB Ashulia", "Z5140": "REB Ashulia",
    "X2589": "REB Ashulia", "X2688": "REB Ashulia", "W2517": "REB Ashulia", "R0918": "REB Ashulia", "X3261": "REB Ashulia",
    "R8097": "REB Ashulia", "R2691": "REB Ashulia", "X0194": "REB Ashulia", "X4436": "REB Ashulia",
    "X0095": "REB Sadullahpur", "R6803": "REB Sadullahpur",
    "X5139": "REB Dhurgapur",
    "X1955": "REB Zirabo", "R6905": "REB Zirabo", "X0093": "REB Zirabo", "Y7650": "REB Zirabo", "R7610": "REB Zirabo",
    "X4179": "REB Zirabo", "Z7629": "REB Zirabo", "X2588": "REB Zirabo", "X2080": "REB Zirabo", "R7418": "REB Zirabo",
    "X4864": "REB Zirabo", "X4311": "REB Zirabo", "X3247": "REB Zirabo", "X3843": "REB Zirabo", "Y8072": "REB Zirabo",
    "Y7655": "REB Zirabo", "Y8062": "REB Zirabo", "X2090": "REB Zirabo", "R3395": "REB Zirabo", "R2516": "REB Zirabo", "R6024": "REB Zirabo",
    "Y7631": "REB Kathgora", "R4861": "REB Kathgora", "Y6778": "REB Kathgora", "Y3949": "REB Kathgora", "Y7628": "REB Kathgora", "R6940": "REB Kathgora",
    "G3704": "REB Jamgora", "X2237": "REB Jamgora", "X2587": "REB Jamgora", "R4869": "REB Jamgora", "Y7577": "REB Jamgora",
    "X0727": "REB Jamgora", "M2342": "REB Jamgora", "X3098": "REB Jamgora", "X1800": "REB Jamgora", "G3668": "REB Jamgora",
    "X2586": "REB Jamgora", "R8067": "REB Jamgora", "B4549": "REB Jamgora", "R7611": "REB Jamgora", "X0967": "REB Jamgora",
    "R8092": "REB Jamgora", "X3500": "REB Jamgora", "X4291": "REB Jamgora", "P6764": "REB Jamgora",
    "X3529": "REB Palash Bari / Kaichabari", "X4404": "REB Palash Bari / Kaichabari", "Y8117": "REB Palash Bari / Kaichabari",
    "R4892": "REB Palash Bari / Kaichabari", "R1189": "REB Palash Bari / Kaichabari", "X0471": "REB Palash Bari / Kaichabari",
    "W4162": "REB Palash Bari / Kaichabari", "X3724": "REB Palash Bari / Kaichabari", "X2585": "REB Palash Bari / Kaichabari",
    "X3447": "REB Palash Bari / Kaichabari", "Y4914": "REB Palash Bari / Kaichabari", "X4195": "REB Palash Bari / Kaichabari",
    "R4342": "REB Bogabari, Bipel, Unique", "X1773": "REB Bogabari, Bipel, Unique", "X3506": "REB Bogabari, Bipel, Unique",
    "X4112": "REB Bogabari, Bipel, Unique", "X4275": "REB Bogabari, Bipel, Unique", "X0049": "REB Bogabari, Bipel, Unique",
    "X0111": "REB Zirani, Kobirpur, Dhamsona", "B6113": "REB Zirani, Kobirpur, Dhamsona", "X1908": "REB Zirani, Kobirpur, Dhamsona",
    "X3296": "REB Zirani, Kobirpur, Dhamsona", "R8061": "REB Zirani, Kobirpur, Dhamsona", "R3651": "REB Zirani, Kobirpur, Dhamsona",
    "W4160": "REB Zirani, Kobirpur, Dhamsona", "R0875": "REB Zirani, Kobirpur, Dhamsona", "R6445": "REB Zirani, Kobirpur, Dhamsona",
    "R3971": "REB Zirani, Kobirpur, Dhamsona",
    "X5517": "REB Simulia Bazar", "X1939": "REB Simulia Bazar", "X2138": "REB Simulia Bazar", "R6885": "REB Simulia Bazar",
    "X2518": "REB Sreepur, Bolibodro", "X0134": "REB Sreepur, Bolibodro", "R2705": "REB Sreepur, Bolibodro",
    "X0726": "REB Sreepur, Bolibodro", "R4938": "REB Sreepur, Bolibodro", "P6775": "REB Sreepur, Bolibodro", "R3791": "REB Sreepur, Bolibodro",
    "X2294": "REB Vadil", "X0354": "REB Vadil", "R4366": "REB Vadil", "G1472": "REB Vadil", "R6782": "REB Vadil", "R4871": "REB Vadil", "W3665": "REB Vadil",
    "R8479": "REB Tajpur"
}

POWER_NUMBERS = {
    "REB Ashulia": "01769401070",
    "REB Sadullahpur": "01769401954",
    "REB Dhurgapur": "01704108972",
    "REB Zirabo": "01769401953",
    "REB Kathgora": "01769401065",
    "REB Jamgora": "01769401071",
    "REB Palash Bari / Kaichabari": "01769401064",
    "REB Bogabari, Bipel, Unique": "01769407540",
    "REB Zirani, Kobirpur, Dhamsona": "01769401069",
    "REB Simulia Bazar": "01769401080",
    "REB Sreepur, Bolibodro": "01769401952",
    "REB Vadil": "01714105944",
    "REB Tajpur": "01769401182",
    "DESCO Uttarkhan, Kaskura": "01324435983",
    "DESCO Dakkhinkhan, Kaow": "01324435982",
    "DESCO Khilkhet, Namapara": "01324435976",
    "DESCO Faidabad, Azompur": "01324435977",
    "DESCO Uttara West": "01321117855",
    "DESCO Uttara East": "01321117854",
    "DESCO Turag": "0248956788",
    "DPDC Khelgaon": "01730320315",
    "DPDC Moghbazar": "01730320306",
    "DPDC Banasree": "01766675039"
}

POWER_BY_AREA = {
    "REB Ashulia": ["ASHULIA", "KHEJURBAGAN"],
    "REB Sadullahpur": ["SADULLAHPUR", "SADULLAPUR"],
    "REB Dhurgapur": ["DHURGAPUR", "DURGAPUR", "INSEPTA", "PUKURPAR"],
    "REB Zirabo": ["ZIRABO"],
    "REB Kathgora": ["KATHGORA"],
    "REB Jamgora": ["JAMGORA", "SHAJAN MARKET", "SAJAN MARKET", "KOBORASTAN"],
    "REB Palash Bari / Kaichabari": ["PALASH", "KAICHABARI"],
    "REB Bogabari, Bipel, Unique": ["BOGABARI", "BIPEL", "UNIQUE"],
    "REB Zirani, Kobirpur, Dhamsona": ["ZIRANI", "KOBIRPUR", "KABIRPUR", "DHAMSONA"],
    "REB Simulia Bazar": ["SIMULIA"],
    "REB Sreepur, Bolibodro": ["SREEPUR", "SRIPUR", "BOLIBODRO"],
    "REB Vadil": ["VADIL", "BAIDIL"],
    "REB Tajpur": ["TAJPUR"],
    "DESCO Uttarkhan, Kaskura": ["UTTARKHAN", "KASKURA"],
    "DESCO Dakkhinkhan, Kaow": ["DAKKHINKHAN", "KAOW"],
    "DESCO Khilkhet, Namapara": ["KHILKHET", "NAMAPARA"],
    "DESCO Faidabad, Azompur": ["FAIDABAD", "AZOMPUR", "AZAMPUR"],
    "DESCO Uttara West": ["UTTARA WEST", "UTTARA WEAST"],
    "DESCO Uttara East": ["UTTARA EAST"],
    "DESCO Turag": ["TURAG"],
    "DPDC Khelgaon": ["KHELGAON", "KHILGAON"],
    "DPDC Moghbazar": ["MOGHBAZAR"],
    "DPDC Banasree": ["BANASREE"]
}

def get_power_office(row):
    addr = str(row.get("Address", "")) + " " + str(row.get("Thana", ""))
    addr = addr.upper()
    for office, keywords in POWER_BY_AREA.items():
        for kw in keywords:
            if kw in addr:
                return office
    all_ids = str(row.get("Generic ID", "")) + " " + str(row.get("2G Site ID", "")) + " " + str(row.get("4G Site ID", "")) + " " + str(row.get("Share Site ID", ""))
    all_ids = all_ids.upper()
    for sid, office in POWER_BY_SITE.items():
        if sid in all_ids:
            return office
    return "DESCO Hotline"

def find_site(text):
    text = text.strip().upper()
    num = re.sub(r"[^0-9]", "", text)
    clean = re.sub(r"[^A-Z0-9]", "", text)
    for _, row in df.iterrows():
        generic = str(row.get("Generic ID", "")).upper()
        g2 = str(row.get("2G Site ID", "")).upper()
        g4 = str(row.get("4G Site ID", "")).upper()
        if clean and (clean in generic or clean in g2 or clean in g4):
            return row
        if num and (num in generic or generic.endswith(num)):
            return row
    return None

def format_reply(row):
    generic = row.get("Generic ID", "")
    g2 = row.get("2G Site ID", "")
    g4 = row.get("4G Site ID", "")
    share = row.get("Share Site ID", "") or "Not Applicable"
    addr = row.get("Address", "")
    thana = row.get("Thana", "")
    ho_name = addr.split(",")[0].strip() if addr else "Not Available"
    ho_num = str(row.get("House Owner Number", "")).strip() or "Not Available"
    latlon = row.get("Lat Long (cleaned)", "")
    gmap = row.get("Direct Google Location", "")
    office = get_power_office(row)
    power_num = POWER_NUMBERS.get(office, "16120")
    return f"""🗼 {g2} | {generic}

📡 2G: {g2}
📶 4G: {g4}
🏷️ SHARE ID: {share}

🏠 {addr}
🏘️ {thana}

📍 LAT LONG:
`{latlon}`

👤 HOUSE OWNER NAME:
{ho_name}
📞 HOUSE OWNER NUMBER:
{ho_num}
`{ho_num}`

🔗 GOOGLE LINK:
{gmap}

⚡ POWER AUTHORITY OFFICE:
{office}
📞 CONTACT NUMBER:
{power_num}
`{power_num}`"""

@app.route("/")
def home():
    return "Bot is Live!"

@bot.message_handler(commands=["start"])
def start(message):
    bot.send_message(message.chat.id, "Hello! Site Code pathan, jemon: 1809 / X0094")

@bot.message_handler(func=lambda m: True)
def reply(message):
    row = find_site(message.text)
    if row is not None:
        bot.send_message(message.chat.id, format_reply(row), parse_mode="Markdown", disable_web_page_preview=True)
    else:
        bot.send_message(message.chat.id, f"{message.text} - Site pai nai!")

def run_bot():
    bot.polling(non_stop=True)

if __name__ == "__main__":
    threading.Thread(target=run_bot, daemon=True).start()
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
