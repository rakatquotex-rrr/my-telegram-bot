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
    "X0094":"REB Ashulia", "X3878":"REB Ashulia", "X3372":"REB Ashulia", "X4211":"REB Ashulia", "Z5140":"REB Ashulia",
    "X2589":"REB Ashulia", "X2688":"REB Ashulia", "W2517":"REB Ashulia", "R0918":"REB Ashulia", "X3261":"REB Ashulia",
    "R8097":"REB Ashulia", "R2691":"REB Ashulia", "X0194":"REB Ashulia", "X4436":"REB Ashulia",
    "X0095":"REB Sadullahpur", "R6803":"REB Sadullahpur",
    "X5139":"REB Dhurgapur",
    "X1955":"REB Zirabo", "R6905":"REB Zirabo", "X0093":"REB Zirabo", "Y7650":"REB Zirabo", "R7610":"REB Zirabo",
    "X4179":"REB Zirabo", "Z7629":"REB Zirabo", "X2588":"REB Zirabo", "X2080":"REB Zirabo", "R7418":"REB Zirabo",
    "X4864":"REB Zirabo", "X4311":"REB Zirabo", "X3247":"REB Zirabo", "X3843":"REB Zirabo", "Y8072":"REB Zirabo",
    "Y7655":"REB Zirabo", "Y8062":"REB Zirabo", "X2090":"REB Zirabo", "R3395":"REB Zirabo", "R2516":"REB Zirabo", "R6024":"REB Zirabo",
    "Y7631":"REB Kathgora", "R4861":"REB Kathgora", "Y6778":"REB Kathgora", "Y3949":"REB Kathgora", "Y7628":"REB Kathgora", "R6940":"REB Kathgora",
    "G3704":"REB Jamgora", "X2237":"REB Jamgora", "X2587":"REB Jamgora", "R4869":"REB Jamgora", "Y7577":"REB Jamgora",
    "X0727":"REB Jamgora", "M2342":"REB Jamgora", "X3098":"REB Jamgora", "X1800":"REB Jamgora", "G3668":"REB Jamgora",
    "X2586":"REB Jamgora", "R8067":"REB Jamgora", "B4549":"REB Jamgora", "R7611":"REB Jamgora", "X0967":"REB Jamgora",
    "R8092":"REB Jamgora", "X3500":"REB Jamgora", "X4291":"REB Jamgora", "P6764":"REB Jamgora",
    "X3529":"REB Palash Bari / Kaichabari", "X4404":"REB Palash Bari / Kaichabari", "Y8117":"REB Palash Bari / Kaichabari",
    "R4892":"REB Palash Bari / Kaichabari", "R1189":"REB Palash Bari / Kaichabari", "X0471":"REB Palash Bari / Kaichabari",
    "W4162":"REB Palash Bari / Kaichabari", "X3724":"REB Palash Bari / Kaichabari", "X2585":"REB Palash Bari / Kaichabari",
    "X3447":"REB Palash Bari / Kaichabari", "Y4914":"REB Palash Bari / Kaichabari", "X4195":"REB Palash Bari / Kaichabari",
    "R4342":"REB Bogabari, Bipel, Unique", "X1773":"REB Bogabari, Bipel, Unique", "X3506":"REB Bogabari, Bipel, Unique",
    "X4112":"REB Bogabari, Bipel, Unique", "X4275":"REB Bogabari, Bipel, Unique", "X0049":"REB Bogabari, Bipel, Unique",
    "X0111":"REB Zirani, Kobirpur, Dhamsona", "B6113":"REB Zirani, Kobirpur, Dhamsona", "X1908":"REB Zirani, Kobirpur, Dhamsona",
    "X3296":"REB Zirani, Kobirpur, Dhamsona", "R8061":"REB Zirani, Kobirpur, Dhamsona", "R3651":"REB Zirani, Kobirpur, Dhamsona",
    "W4160":"REB Zirani, Kobirpur, Dhamsona", "R0875":"REB Zirani, Kobirpur, Dhamsona", "R6445":"REB Zirani, Kobirpur, Dhamsona",
    "R3971":"REB Zirani, Kobirpur, Dhamsona",
    "X5517":"REB Simulia Bazar", "X1939":"REB Simulia Bazar", "X2138":"REB Simulia Bazar", "R6885":"REB Simulia Bazar",
    "X2518":"REB Sreepur, Bolibodro", "X0134":"REB Sreepur, Bolibodro", "R2705":"REB Sreepur, Bolibodro",
    "X0726":"REB Sreepur, Bolibodro", "R4938":"REB Sreepur, Bolibodro", "P6775":"REB Sreepur, Bolibodro", "R3791":"REB Sreepur, Bolibodro",
    "X2294":"REB Vadil", "X0354":"REB Vadil", "R4366":"REB Vadil", "G1472":"REB Vadil", "R6782":"REB Vadil", "R4871":"REB Vadil", "W3665":"REB Vadil",
    "R8479":"REB Tajpur",
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
    "DPDC Banasree": "01766675039",
}

POWER_BY_AREA = [
    (["ASHULIA", "KHEJURBAGAN"], "REB Ashulia"),
    (["SADULLAHPUR", "SADULLAPUR"], "REB Sadullahpur"),
    (["DHURGAPUR", "DURGAPUR", "INSEPTA", "PUKURPAR"], "REB Dhurgapur"),
    (["ZIRABO"], "REB Zirabo"),
    (["KATHGORA"], "REB Kathgora"),
    (["JAMGORA", "SHAJAN MARKET", "SAJAN MARKET", "KOBORASTAN"], "REB Jamgora"),
    (["PALASH", "KAICHABARI"], "REB Palash Bari / Kaichabari"),
    (["BOGABARI", "BIPEL", "UNIQUE"], "REB Bogabari, Bipel, Unique"),
    (["ZIRANI", "KOBIRPUR", "KABIRPUR", "DHAMSONA"], "REB Zirani, Kobirpur, Dhamsona"),
    (["SIMULIA"], "REB Simulia Bazar"),
    (["SREEPUR", "SRIPUR", "BOLIBODRO"], "REB Sreepur, Bolibodro"),
    (["VADIL", "BAIDIL"], "REB Vadil"),
    (["TAJPUR"], "REB Tajpur"),
    (["UTTARKHAN", "KASKURA"], "DESCO Uttarkhan, Kaskura"),
    (["DAKKHINKHAN", "KAOW"], "DESCO Dakkhinkhan, Kaow"),
    (["KHILKHET", "NAMAPARA"], "DESCO Khilkhet, Namapara"),
    (["FAIDABAD", "AZOMPUR", "AZAMPUR"], "DESCO Faidabad, Azompur"),
    (["UTTARA WEST", "UTTARA WEAST"], "DESCO Uttara West"),
    (["UTTARA EAST"], "DESCO Uttara East"),
    (["TURAG"], "DESCO Turag"),
    (["KHELGAON", "KHILGAON"],
