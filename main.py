import os
import threading
from flask import Flask
import telebot

TOKEN = os.getenv("TOKEN")
bot = telebot.TeleBot(TOKEN)

app = Flask(__name__)

# =========================
# DATI SANZIONI
# =========================

VIOLATIONS = {
    "085-02": {
        "title": "Noleggio con conducente di veicolo non adibito a tale uso - 1a violazione",
        "article": "CdS art. 85 c. 4",
        "pmr": "Non ammesso",
        "reduced_30": "Non ammesso",
        "over_60": "Non ammesso",
        "edictal": "da € 1.812,00 a € 7.249,00",
        "accessories": [
            "Sospensione patente da 4 a 12 mesi",
            "Sequestro del veicolo ai fini della confisca"
        ],
        "verbal_text": (
            "Effettuava servizio di noleggio con conducente con veicolo non adibito a tale uso, "
            "in violazione dell’art. 85, comma 4, Codice della strada. "
            "Si procedeva altresì al sequestro del veicolo ai fini della confisca. "
            "Non è ammesso il pagamento in misura ridotta."
        ),
        "notes": [
            "Il verbale va inviato entro 10 giorni al Prefetto del luogo della violazione.",
            "Possibili violazioni concorrenti: CAP/CQC, art. 72, art. 79, 085-05.",
            "Non è ammesso il servizio NCC di autocarri per trasporto cose per conto terzi."
        ]
    },
    "085-04": {
        "title": "Noleggio con conducente di veicolo non adibito a tale uso - 2a violazione nel triennio",
        "article": "CdS art. 85 c. 4",
        "pmr": "Non ammesso",
        "reduced_30": "Non ammesso",
        "over_60": "Non ammesso",
        "edictal": "da € 1.812,00 a € 7.249,00",
        "accessories": [
            "Revoca patente",
            "Sequestro del veicolo per confisca"
        ],
        "verbal_text": (
            "Per la seconda volta, in un periodo di 3 anni, adibiva a noleggio con conducente il veicolo sopra indicato "
            "benché non destinato a tale uso. Risultava infatti, in base alle indicazioni del documento di circolazione, "
            "che il veicolo doveva essere adibito a diverso uso. Nella circostanza veniva accertato il trasporto di persone. "
            "Il veicolo è sottoposto a sequestro come da apposito verbale."
        ),
        "notes": [
            "Alla seconda violazione nel triennio si applica la revoca patente.",
            "L'organo accertatore comunica entro 5 giorni al Prefetto i presupposti della revoca."
        ]
    },
    "085-05": {
        "title": "NCC in violazione degli artt. 3 e 11 L. 21/1992 - 1a violazione nel quinquennio",
        "article": "CdS art. 85 c. 4-bis + L. 21/1992",
        "pmr": "€ 178,00",
        "reduced_30": "€ 124,60",
        "over_60": "€ 336,00",
        "edictal": "da € 178,00 a € 672,00",
        "accessories": [
            "Sospensione documento di circolazione per 1 mese"
        ],
        "verbal_text": (
            "Utilizzava l'autovettura adibita a servizio di noleggio con conducente, munito della relativa autorizzazione, "
            "senza ottemperare alle disposizioni dell'art. 3 o dell'art. 11 della L. 21/1992. "
            "Il documento di circolazione è ritirato e trasmesso all'UMC competente. "
            "Il conducente è autorizzato a condurre il veicolo per la via più breve fino al luogo indicato, "
            "con l'avvertenza che il veicolo sarà sottoposto a fermo amministrativo per la durata della sospensione."
        ),
        "notes": [
            "Se il conducente non è titolare dell’autorizzazione, la violazione va notificata al titolare.",
            "Non contestare come autonoma violazione il mero mancato rientro in rimessa dopo ogni servizio.",
            "Verificare con attenzione prenotazione, stazionamento, foglio di servizio, sede/rimessa."
        ]
    },
    "085-06": {
        "title": "NCC in violazione degli artt. 3 e 11 L. 21/1992 - 2a violazione nel quinquennio",
        "article": "CdS art. 85 c. 4-bis + L. 21/1992",
        "pmr": "€ 264,00",
        "reduced_30": "€ 184,80",
        "over_60": "€ 505,00",
        "edictal": "da € 264,00 a € 1.010,00",
        "accessories": [
            "Sospensione documento di circolazione da 1 a 2 mesi"
        ],
        "verbal_text": (
            "Utilizzava l'autovettura adibita a servizio di noleggio con conducente, munito della relativa autorizzazione, "
            "senza ottemperare alle disposizioni dell'art. 3 o dell'art. 11 della L. 21/1992. "
            "Il documento di circolazione è ritirato e trasmesso all'UMC competente."
        ),
        "notes": [
            "Seconda violazione nel quinquennio.",
            "Se il conducente non è titolare, risponde il titolare dell’autorizzazione."
        ]
    },
    "085-07": {
        "title": "NCC in violazione degli artt. 3 e 11 L. 21/1992 - 3a violazione nel quinquennio",
        "article": "CdS art. 85 c. 4-bis + L. 21/1992",
        "pmr": "€ 356,00",
        "reduced_30": "€ 249,20",
        "over_60": "€ 672,00",
        "edictal": "da € 356,00 a € 1.344,00",
        "accessories": [
            "Sospensione documento di circolazione da 2 a 4 mesi"
        ],
        "verbal_text": (
            "Utilizzava l'autovettura adibita a servizio di noleggio con conducente, munito della relativa autorizzazione, "
            "senza ottemperare alle disposizioni dell'art. 3 o dell'art. 11 della L. 21/1992."
        ),
        "notes": [
            "Terza violazione nel quinquennio."
        ]
    },
    "085-08": {
        "title": "NCC in violazione degli artt. 3 e 11 L. 21/1992 - 4a o successiva nel quinquennio",
        "article": "CdS art. 85 c. 4-bis + L. 21/1992",
        "pmr": "€ 528,00",
        "reduced_30": "€ 369,60",
        "over_60": "€ 1.010,00",
        "edictal": "da € 528,00 a € 2.020,00",
        "accessories": [
            "Sospensione documento di circolazione da 4 a 8 mesi"
        ],
        "verbal_text": (
            "Utilizzava l'autovettura adibita a servizio di noleggio con conducente, munito della relativa autorizzazione, "
            "senza ottemperare alle disposizioni dell'art. 3 o dell'art. 11 della L. 21/1992."
        ),
        "notes": [
            "Quarta o successiva violazione nel quinquennio."
        ]
    },
    "085-09": {
        "title": "Circolazione con NCC violando altre prescrizioni dell’autorizzazione",
        "article": "CdS art. 85 c. 4-ter",
        "pmr": "€ 86,00",
        "reduced_30": "€ 60,20",
        "over_60": "€ 169,00",
        "edictal": "da € 86,00 a € 338,00",
        "accessories": [
            "Non previste"
        ],
        "verbal_text": (
            "Utilizzava il veicolo adibito a servizio di noleggio con conducente senza ottemperare alle norme in vigore "
            "ovvero alle condizioni di cui all'autorizzazione. Veniva accertato che ..."
        ),
        "notes": [
            "Rientrano qui le prescrizioni diverse dagli artt. 3 e 11 L. 21/1992.",
            "Verificare regolamenti comunali/locali, ZTL, modalità di servizio, ruolo CCIAA."
        ]
    },
    "116-06": {
        "title": "Guida senza CAP o CQC",
        "article": "CdS art. 116 c. 16 e 18",
        "pmr": "€ 408,00",
        "reduced_30": "€ 285,60",
        "over_60": "€ 817,00",
        "edictal": "da € 408,00 a € 1.634,00",
        "accessories": [
            "Fermo veicolo per 60 giorni"
        ],
        "verbal_text": (
            "Circolava alla guida del predetto veicolo adibito a servizio di noleggio con conducente "
            "munito di patente ma non del prescritto certificato di abilitazione professionale / titolo professionale richiesto."
        ),
        "notes": [
            "Da valutare concorso con 085-02/04 o 085-05 e seguenti."
        ]
    }
}

# =========================
# STATO CONVERSAZIONI
# =========================

user_states = {}

# user_states[chat_id] = {
#   "mode": "case_flow",
#   "answers": {},
#   "step": "vehicle_type"
# }

# =========================
# FUNZIONI UTILI
# =========================

def start_case(chat_id):
    user_states[chat_id] = {
        "mode": "case_flow",
        "answers": {},
        "step": "vehicle_authorized"
    }

def clear_case(chat_id):
    if chat_id in user_states:
        del user_states[chat_id]

def is_in_case(chat_id):
    return chat_id in user_states and user_states[chat_id].get("mode") == "case_flow"

def get_state(chat_id):
    return user_states.get(chat_id)

def set_answer(chat_id, key, value):
    user_states[chat_id]["answers"][key] = value

def next_step(chat_id, step):
    user_states[chat_id]["step"] = step

def format_violation(code):
    v = VIOLATIONS[code]
    lines = []
    lines.append("ESITO FINALE")
    lines.append(v["title"])
    lines.append("")
    lines.append("RIFERIMENTO")
    lines.append(v["article"])
    lines.append("")
    lines.append("VOCE OPERATIVA")
    lines.append(code)
    lines.append("")
    lines.append("IMPORTI")
    lines.append(f"- Pagamento in misura ridotta: {v['pmr']}")
    lines.append(f"- Riduzione 30% entro 5 gg: {v['reduced_30']}")
    lines.append(f"- Pagamento oltre 60 gg: {v['over_60']}")
    lines.append(f"- Limiti edittali: {v['edictal']}")
    lines.append("")
    lines.append("SANZIONI ACCESSORIE")
    for a in v["accessories"]:
        lines.append(f"- {a}")
    lines.append("")
    lines.append("DICITURA VERBALE")
    lines.append(v["verbal_text"])
    lines.append("")
    lines.append("NOTE OPERATIVE")
    for n in v["notes"]:
        lines.append(f"- {n}")
    lines.append("")
    lines.append("AVVERTENZA")
    lines.append("Verificare sempre normativa vigente, prontuario del comando, disciplina locale e dati concreti del caso.")
    return "\n".join(lines)

def format_multiple(main_code, concurrent_codes=None, extra_notes=None):
    if concurrent_codes is None:
        concurrent_codes = []
    if extra_notes is None:
        extra_notes = []

    main_text = format_violation(main_code)

    lines = [main_text]

    if concurrent_codes:
        lines.append("")
        lines.append("VIOLAZIONI CONCORRENTI POSSIBILI")
        for code in concurrent_codes:
            v = VIOLATIONS[code]
            lines.append(f"- {code} | {v['article']} | {v['title']}")

    if extra_notes:
        lines.append("")
        lines.append("ULTERIORI VERIFICHE")
        for note in extra_notes:
            lines.append(f"- {note}")

    return "\n".join(lines)

# =========================
# MOTORE DECISIONALE
# =========================

def decide_violation(answers):
    vehicle_authorized = answers.get("vehicle_authorized")        # si/no
    service_to_third = answers.get("service_to_third")            # si/no/dubbio
    violation_type = answers.get("violation_type")                # art3_11 / other_auth / none
    recurrence = answers.get("recurrence")                        # first / second_3y / 1_5y / 2_5y / 3_5y / 4plus_5y
    kb = answers.get("kb")                                        # si/no
    public_waiting = answers.get("public_waiting")                # si/no
    taxi_commune = answers.get("taxi_commune")                    # si/no
    booking = answers.get("booking")                              # si/no
    courtesy = answers.get("courtesy")                            # si/no
    separate_payment = answers.get("separate_payment")            # si/no

    concurrent = []
    notes = []

    if kb == "no":
        concurrent.append("116-06")

    # filtro di prudenza: attività accessoria / cortesia
    if courtesy == "si" and separate_payment == "no":
        return None, concurrent, [
            "Il caso può rientrare in trasporto di cortesia / attività accessoria.",
            "Verificare che non vi sia corrispettivo autonomo o utenza indifferenziata.",
            "Verificare che il trasporto sia riservato a clienti propri e accessorio all’attività principale."
        ]

    # mezzo non autorizzato NCC
    if vehicle_authorized == "no" and service_to_third == "si":
        if recurrence == "second_3y":
            return "085-04", concurrent, notes
        return "085-02", concurrent, notes

    # mezzo autorizzato NCC + violazione artt. 3 o 11
    if vehicle_authorized == "si" and violation_type == "art3_11":
        if recurrence == "2_5y":
            return "085-06", concurrent, notes
        elif recurrence == "3_5y":
            return "085-07", concurrent, notes
        elif recurrence == "4plus_5y":
            return "085-08", concurrent, notes
        else:
            return "085-05", concurrent, notes

    # mezzo autorizzato NCC + altre prescrizioni
    if vehicle_authorized == "si" and violation_type == "other_auth":
        return "085-09", concurrent, notes

    # stazionamento pubblico senza prenotazione: suggerimento art. 3/11
    if vehicle_authorized == "si" and public_waiting == "si" and taxi_commune == "si" and booking == "no":
        notes.extend([
            "Possibile violazione art. 11 L. 21/1992 per stazionamento fuori rimessa.",
            "Verificare se il veicolo era in attesa di utenza indifferenziata o già in servizio su prenotazione."
        ])
        return "085-05", concurrent, notes

    return None, concurrent, [
        "Caso non chiudibile automaticamente.",
        "Servono ulteriori elementi su autorizzazione, prenotazione, natura del servizio e progressione."
    ]

# =========================
# DOMANDE GUIDATE
# =========================

def ask_step(chat_id):
    state = get_state(chat_id)
    step = state["step"]

    if step == "vehicle_authorized":
        bot.send_message(
            chat_id,
            "1) Il veicolo è autorizzato/adibito a NCC?\n"
            "Rispondi con una delle seguenti parole:\n"
            "si / no"
        )

    elif step == "service_to_third":
        bot.send_message(
            chat_id,
            "2) Il trasporto è verso terzi / a pagamento / per utenza esterna?\n"
            "Rispondi:\n"
            "si / no / dubbio"
        )

    elif step == "courtesy":
        bot.send_message(
            chat_id,
            "3) Si tratta di trasporto di cortesia / attività accessoria per clienti propri?\n"
            "Rispondi:\n"
            "si / no"
        )

    elif step == "separate_payment":
        bot.send_message(
            chat_id,
            "4) Esiste un corrispettivo separato specifico per il trasporto?\n"
            "Rispondi:\n"
            "si / no"
        )

    elif step == "violation_type":
        bot.send_message(
            chat_id,
            "5) Se il veicolo è NCC, la violazione riguarda:\n"
            "art3_11 = artt. 3 o 11 L. 21/1992\n"
            "other_auth = altre prescrizioni dell'autorizzazione\n"
            "none = non chiaro / non applicabile"
        )

    elif step == "public_waiting":
        bot.send_message(
            chat_id,
            "6) Il veicolo stazionava/sostava su area pubblica in attesa?\n"
            "Rispondi:\n"
            "si / no"
        )

    elif step == "taxi_commune":
        bot.send_message(
            chat_id,
            "7) Il fatto è avvenuto in un comune dove è esercitato il servizio taxi?\n"
            "Rispondi:\n"
            "si / no"
        )

    elif step == "booking":
        bot.send_message(
            chat_id,
            "8) Esiste prenotazione documentabile / foglio di servizio / contratto?\n"
            "Rispondi:\n"
            "si / no"
        )

    elif step == "recurrence":
        bot.send_message(
            chat_id,
            "9) Indica la progressione della violazione.\n"
            "Rispondi con UNA di queste:\n"
            "first = prima violazione\n"
            "second_3y = seconda nel triennio (per 085-04)\n"
            "1_5y = prima nel quinquennio\n"
            "2_5y = seconda nel quinquennio\n"
            "3_5y = terza nel quinquennio\n"
            "4plus_5y = quarta o successiva nel quinquennio"
        )

    elif step == "kb":
        bot.send_message(
            chat_id,
            "10) Il conducente ha il titolo professionale richiesto (KB/KA/CQC se dovuto)?\n"
            "Rispondi:\n"
            "si / no"
        )

    elif step == "finalize":
        answers = state["answers"]
        main_code, concurrent, notes = decide_violation(answers)

        if main_code:
            result = format_multiple(main_code, concurrent, notes)
        else:
            lines = []
            lines.append("ESITO")
            lines.append("Non è stato possibile individuare automaticamente una voce sanzionatoria definitiva.")
            lines.append("")
            if concurrent:
                lines.append("VIOLAZIONI CONCORRENTI POSSIBILI")
                for code in concurrent:
                    v = VIOLATIONS[code]
                    lines.append(f"- {code} | {v['article']} | {v['title']}")
                lines.append("")
            lines.append("VERIFICHE NECESSARIE")
            for n in notes:
                lines.append(f"- {n}")
            lines.append("")
            lines.append("AVVERTENZA")
            lines.append("Il caso richiede approfondimento su normativa vigente, prontuario e circostanze concrete.")
            result = "\n".join(lines)

        bot.send_message(chat_id, result)
        clear_case(chat_id)

# =========================
# GESTIONE INPUT STEP BY STEP
# =========================

def handle_case_input(message):
    chat_id = message.chat.id
    text = message.text.strip().lower()
    state = get_state(chat_id)
    step = state["step"]

    allowed_yes_no = {"si", "no"}
    allowed_yes_no_doubt = {"si", "no", "dubbio"}

    if step == "vehicle_authorized":
        if text in allowed_yes_no:
            set_answer(chat_id, "vehicle_authorized", text)
            next_step(chat_id, "service_to_third")
            ask_step(chat_id)
        else:
            bot.reply_to(message, "Rispondi solo con: si / no")

    elif step == "service_to_third":
        if text in allowed_yes_no_doubt:
            set_answer(chat_id, "service_to_third", text)
            next_step(chat_id, "courtesy")
            ask_step(chat_id)
        else:
            bot.reply_to(message, "Rispondi solo con: si / no / dubbio")

    elif step == "courtesy":
        if text in allowed_yes_no:
            set_answer(chat_id, "courtesy", text)
            next_step(chat_id, "separate_payment")
            ask_step(chat_id)
        else:
            bot.reply_to(message, "Rispondi solo con: si / no")

    elif step == "separate_payment":
        if text in allowed_yes_no:
            set_answer(chat_id, "separate_payment", text)
            next_step(chat_id, "violation_type")
            ask_step(chat_id)
        else:
            bot.reply_to(message, "Rispondi solo con: si / no")

    elif step == "violation_type":
        if text in {"art3_11", "other_auth", "none"}:
            set_answer(chat_id, "violation_type", text)
            next_step(chat_id, "public_waiting")
            ask_step(chat_id)
        else:
            bot.reply_to(message, "Rispondi solo con: art3_11 / other_auth / none")

    elif step == "public_waiting":
        if text in allowed_yes_no:
            set_answer(chat_id, "public_waiting", text)
            next_step(chat_id, "taxi_commune")
            ask_step(chat_id)
        else:
            bot.reply_to(message, "Rispondi solo con: si / no")

    elif step == "taxi_commune":
        if text in allowed_yes_no:
            set_answer(chat_id, "taxi_commune", text)
            next_step(chat_id, "booking")
            ask_step(chat_id)
        else:
            bot.reply_to(message, "Rispondi solo con: si / no")

    elif step == "booking":
        if text in allowed_yes_no:
            set_answer(chat_id, "booking", text)
            next_step(chat_id, "recurrence")
            ask_step(chat_id)
        else:
            bot.reply_to(message, "Rispondi solo con: si / no")

    elif step == "recurrence":
        if text in {"first", "second_3y", "1_5y", "2_5y", "3_5y", "4plus_5y"}:
            set_answer(chat_id, "recurrence", text)
            next_step(chat_id, "kb")
            ask_step(chat_id)
        else:
            bot.reply_to(
                message,
                "Rispondi solo con una delle opzioni:\n"
                "first / second_3y / 1_5y / 2_5y / 3_5y / 4plus_5y"
            )

    elif step == "kb":
        if text in allowed_yes_no:
            set_answer(chat_id, "kb", text)
            next_step(chat_id, "finalize")
            ask_step(chat_id)
        else:
            bot.reply_to(message, "Rispondi solo con: si / no")


# =========================
# FLASK
# =========================

@app.route("/")
def home():
    return "NCC Sanzioni Bot attivo", 200


# =========================
# COMANDI BOT
# =========================

@bot.message_handler(commands=['start'])
def start_command(message):
    bot.reply_to(
        message,
        "Benvenuto in NCC Sanzioni Bot.\n\n"
        "Comandi disponibili:\n"
        "/caso - avvia analisi guidata\n"
        "/help - guida\n"
        "/norme - riferimenti principali\n"
        "/reset - annulla caso in corso"
    )

@bot.message_handler(commands=['help'])
def help_command(message):
    bot.reply_to(
        message,
        "Usa /caso per avviare l’analisi guidata.\n\n"
        "Il bot ti farà domande per arrivare a:\n"
        "- voce operativa\n"
        "- articolo\n"
        "- importi\n"
        "- sanzioni accessorie\n"
        "- dicitura verbale\n\n"
        "Usa /reset per annullare una procedura in corso."
    )

@bot.message_handler(commands=['norme'])
def norme_command(message):
    bot.reply_to(
        message,
        "Riferimenti principali NCC:\n"
        "- L. 21/1992 artt. 3 e 11\n"
        "- CdS art. 85 c. 4\n"
        "- CdS art. 85 c. 4-bis\n"
        "- CdS art. 85 c. 4-ter\n"
        "- CdS art. 116 c. 16 e 18\n\n"
        "Nota: non proporre automaticamente come illecito il mero mancato rientro in rimessa dopo ogni servizio."
    )

@bot.message_handler(commands=['reset'])
def reset_command(message):
    clear_case(message.chat.id)
    bot.reply_to(message, "Procedura annullata.")

@bot.message_handler(commands=['caso'])
def caso_command(message):
    start_case(message.chat.id)
    bot.reply_to(
        message,
        "Avvio analisi guidata del caso NCC.\n"
        "Rispondi alle domande con una sola delle opzioni indicate."
    )
    ask_step(message.chat.id)


# =========================
# MESSAGGI GENERICI
# =========================

@bot.message_handler(func=lambda m: True)
def all_messages(message):
    chat_id = message.chat.id

    if is_in_case(chat_id):
        handle_case_input(message)
    else:
        bot.reply_to(
            message,
            "Usa /caso per avviare l’analisi guidata."
        )


# =========================
# AVVIO BOT
# =========================

def run_bot():
    bot.remove_webhook()
    bot.infinity_polling(timeout=30, long_polling_timeout=30)

if __name__ == "__main__":
    threading.Thread(target=run_bot, daemon=True).start()
    port = int(os.getenv("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
