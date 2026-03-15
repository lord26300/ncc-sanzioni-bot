import telebot
import os

TOKEN = os.getenv("TOKEN")

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message,
    "Benvenuto in NCC Sanzioni Bot.\n\n"
    "Comandi disponibili:\n"
    "/caso\n/checklist\n/norme\n/help")

@bot.message_handler(commands=['help'])
def help(message):
    bot.reply_to(message,
    "Scrivi /caso e descrivi la situazione.\n"
    "Il bot suggerirà articoli e verifiche.")

@bot.message_handler(commands=['checklist'])
def checklist(message):
    bot.reply_to(message,
    "Checklist controllo NCC:\n"
    "1. Trasporto verso terzi?\n"
    "2. Veicolo autorizzato NCC?\n"
    "3. Prenotazione documentabile?\n"
    "4. Conducente con KB/CQC?\n"
    "5. Patente idonea?")

@bot.message_handler(commands=['norme'])
def norme(message):
    bot.reply_to(message,
    "Normativa principale NCC:\n"
    "- L. 21/1992\n"
    "- CdS art. 85\n"
    "- CdS art. 116")

@bot.message_handler(commands=['caso'])
def caso(message):
    bot.reply_to(message,
    "Descrivi la situazione NCC.\n"
    "Esempio: veicolo privato trasporta clienti aeroporto-centro città.")

@bot.message_handler(func=lambda m: True)
def risposta(message):
    bot.reply_to(message,
    "Caso ricevuto.\n"
    "Verifica possibile violazione art. 85 CdS o art. 116 CdS.\n"
    "Risposta preliminare.")

bot.infinity_polling()
