import os
import threading
from flask import Flask
import telebot

TOKEN = os.getenv("TOKEN")
bot = telebot.TeleBot(TOKEN)

app = Flask(__name__)

# Tiene traccia degli utenti che hanno scritto /caso
waiting_for_case = set()

@app.route("/")
def home():
    return "NCC Sanzioni Bot attivo", 200


def analizza_caso(testo: str) -> str:
    t = testo.lower()

    norme = []
    codici = []
    verifiche = []
    esito = "Caso da approfondire."

    # parole chiave utili
    mezzo_non_ncc = any(x in t for x in [
        "veicolo privato", "mezzo privato", "non ncc", "senza autorizzazione",
        "abusivo", "proprio veicolo"
    ])

    prenotazione_mancante = any(x in t for x in [
        "senza prenotazione", "no prenotazione", "manca prenotazione"
    ])

    stazione_aeroporto = any(x in t for x in [
        "stazione", "aeroporto", "porto", "terminal"
    ])

    kb_mancante = any(x in t for x in [
        "senza kb", "senza ka", "senza cqc", "manca kb", "manca ka", "manca cqc"
    ])

    patente_mancante = any(x in t for x in [
        "senza patente", "patente non idonea", "patente scaduta",
        "mai conseguita", "patente revocata"
    ])

    navetta = any(x in t for x in [
        "navetta", "parcheggio", "transfer", "trasferimento interno"
    ])

    clienti_terzi = any(x in t for x in [
        "clienti", "turisti", "a pagamento", "trasporto verso terzi"
    ])

    veicolo_ncc = any(x in t for x in [
        "veicolo ncc", "mezzo ncc", "autorizzato ncc", "con autorizzazione ncc"
    ])

    affidamento = any(x in t for x in [
        "affidato", "dato in uso", "consegnato il veicolo", "incauto affidamento"
    ])

    # Regole principali
    if mezzo_non_ncc and clienti_terzi:
        esito = "Possibile svolgimento di servizio assimilabile a NCC con veicolo non autorizzato."
        norme.append("CdS art. 85 c. 4")
        codici.append("085-02")
        verifiche.extend([
            "accertare se il trasporto è verso terzi",
            "verificare autorizzazione NCC del veicolo",
            "controllare eventuali precedenti nel triennio"
        ])

    if veicolo_ncc and prenotazione_mancante:
        esito = "Possibile violazione delle prescrizioni del servizio NCC."
        norme.append("L. 21/1992 artt. 3 e 11")
        norme.append("CdS art. 85 c. 4-bis")
        codici.append("085-05 / 085-06 / 085-07 / 085-08")
        verifiche.extend([
            "verificare documentazione della prenotazione",
            "accertare progressione nel quinquennio",
            "distinguere se la violazione riguarda artt. 3 o 11"
        ])

    if veicolo_ncc and not prenotazione_mancante and stazione_aeroporto:
        verifiche.append("verificare se vi è procacciamento diretto della clientela")
        verifiche.append("verificare se il servizio rispetta le prescrizioni dell'autorizzazione")

    if kb_mancante:
        esito = "Possibile violazione relativa al titolo professionale richiesto al conducente."
        norme.append("CdS art. 116 c. 16 e 18")
        codici.append("116-06")
        verifiche.extend([
            "verificare se per il servizio svolto è richiesto KB/KA/CQC",
            "controllare validità del titolo professionale"
        ])

    if patente_mancante:
        esito = "Possibile violazione relativa alla patente del conducente."
        norme.append("CdS art. 116 c. 15 e 17")
        codici.append("116-02 / 116-03 / 116-04")
        verifiche.extend([
            "accertare se si tratta di prima violazione o recidiva",
            "verificare la tipologia di patente posseduta"
        ])

    if affidamento and (kb_mancante or patente_mancante):
        norme.append("CdS art. 116 c. 14")
        codici.append("116-01")
        verifiche.append("valutare incauto affidamento a carico dell'affidante")

    if navetta:
        esito = "Caso da distinguere tra attività accessoria e trasporto verso terzi."
        verifiche.extend([
            "verificare se il servizio è riservato ai clienti della struttura",
            "controllare documentazione commerciale e contrattuale",
            "accertare se il trasporto è autonomamente offerto a terzi"
        ])

    if not norme:
        norme.append("Verifica L. 21/1992")
        norme.append("Verifica CdS art. 85")
        norme.append("Verifica CdS art. 116")
        verifiche.append("descrivere meglio veicolo, prenotazione, clienti e titoli del conducente")

    # rimuove duplicati mantenendo ordine
    def unici(lista):
        viste = set()
        out = []
        for item in lista:
            if item not in viste:
                viste.add(item)
                out.append(item)
        return out

    norme = unici(norme)
    codici = unici(codici)
    verifiche = unici(verifiche)

    risposta = []
    risposta.append("Esito preliminare")
    risposta.append(esito)
    risposta.append("")
    risposta.append("Possibili riferimenti normativi")
    for n in norme:
        risposta.append(f"- {n}")
    risposta.append("")
    risposta.append("Possibili codici sanzione")
    for c in codici:
        risposta.append(f"- {c}")
    risposta.append("")
    risposta.append("Verifiche ulteriori")
    for v in verifiche:
        risposta.append(f"- {v}")
    risposta.append("")
    risposta.append("Avvertenza")
    risposta.append("Risposta operativa preliminare da verificare su normativa vigente, prontuario e disciplina locale.")

    return "\n".join(risposta)


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
        "Usa /caso e poi descrivi la situazione.\n\n"
        "Esempio:\n"
        "veicolo privato trasporta clienti a pagamento senza autorizzazione ncc\n\n"
        "Il bot fornirà un inquadramento preliminare con norme, codici sanzione e verifiche."
    )


@bot.message_handler(commands=['checklist'])
def checklist(message):
    bot.reply_to(
        message,
        "Checklist controllo NCC:\n"
        "1. Trasporto verso terzi o attività accessoria?\n"
        "2. Veicolo autorizzato NCC?\n"
        "3. Prenotazione documentabile?\n"
        "4. Conducente con KB/KA/CQC?\n"
        "5. Patente idonea?\n"
        "6. Veicolo affidato da altro soggetto?\n"
        "7. Clienti propri o terzi?\n"
        "8. Stazione, aeroporto, porto o terminal?\n"
        "9. Precedenti utili per progressione sanzionatoria?"
    )


@bot.message_handler(commands=['norme'])
def norme(message):
    bot.reply_to(
        message,
        "Normativa principale NCC:\n"
        "- L. 21/1992 artt. 3 e 11\n"
        "- CdS art. 85 c. 4\n"
        "- CdS art. 85 c. 4-bis\n"
        "- CdS art. 85 c. 4-ter\n"
        "- CdS art. 116 c. 14\n"
        "- CdS art. 116 c. 15 e 17\n"
        "- CdS art. 116 c. 16 e 18"
    )


@bot.message_handler(commands=['caso'])
def caso(message):
    waiting_for_case.add(message.chat.id)
    bot.reply_to(
        message,
        "Descrivi il caso NCC in un solo messaggio.\n\n"
        "Esempio:\n"
        "veicolo privato trasporta clienti a pagamento senza autorizzazione ncc e senza kb"
    )


@bot.message_handler(func=lambda m: True)
def risposta_generica(message):
    if message.chat.id in waiting_for_case:
        waiting_for_case.remove(message.chat.id)
        risposta = analizza_caso(message.text)
        bot.reply_to(message, risposta)
    else:
        bot.reply_to(
            message,
            "Per analizzare una situazione usa /caso"
        )


def run_bot():
    bot.remove_webhook()
    bot.infinity_polling(timeout=30, long_polling_timeout=30)


if __name__ == "__main__":
    threading.Thread(target=run_bot, daemon=True).start()
    port = int(os.getenv("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
