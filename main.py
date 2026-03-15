import os
import threading
from flask import Flask
import telebot

TOKEN = os.getenv("TOKEN")
bot = telebot.TeleBot(TOKEN)

app = Flask(__name__)

@app.route("/")
def home():
    return "NCC Sanzioni Bot attivo", 200

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(
        message,
        "Benvenuto in NCC Sanzioni Bot.\n\n"
        "Comandi disponibili:\n"
        "/caso\n/checklist\n/norme\n/help"
    )

@bot.message_handler(commands=['help'])
def help_command(message):
    bot.reply_to(
        message,
        "Scrivi /caso e descrivi la situazione.\n"
        "Il bot suggerirà articoli e verifiche."
    )

@bot.message_handler(commands=['checklist'])
def checklist(message):
    bot.reply_to(
        message,
        "Checklist controllo NCC:\n"
        "1. Trasporto verso terzi?\n"
        "2. Veicolo autorizzato NCC?\n"
        "3. Prenotazione documentabile?\n"
        "4. Conducente con KB/CQC?\n"
        "5. Patente idonea?"
    )

@bot.message_handler(commands=['norme'])
def norme(message):
    bot.reply_to(
        message,
        "Normativa principale NCC:\n"
        "- L. 21/1992\n"
        "- CdS art. 85\n"
        "- CdS art. 116"
    )

@bot.message_handler(commands=['caso'])
def caso(message):
    bot.reply_to(
        message,
        "Descrivi la situazione NCC.\n"
        "Esempio: veicolo privato trasporta clienti aeroporto-centro città."
    )

@bot.message_handler(func=lambda m: True)
def risposta(message):
    bot.reply_to(
        message,
        "Caso ricevuto.\n"
        "Verifica possibile violazione art. 85 CdS o art. 116 CdS.\n"
        "Risposta preliminare."
    )

def run_bot():
    bot.infinity_polling(timeout=30, long_polling_timeout=30)

if __name__ == "__main__":
    threading.Thread(target=run_bot, daemon=True).start()
    port = int(os.getenv("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
