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
            "Adibiva a noleggio con conducente il veicolo sopra indicato benché non destinato a tale uso "
            "(ovvero, solo per autovetture e motocarrozzette, benché privo della prescritta autorizzazione; "
            "ovvero, per tutti i veicoli, benché l'autorizzazione fosse sospesa o revocata). "
            "Risultava infatti, in base alle indicazioni del documento di circolazione, che il veicolo doveva "
            "essere adibito a diverso uso. Nella circostanza veniva accertato il trasporto di persone. "
            "Il veicolo è sottoposto a sequestro ai fini della confisca come da separato verbale."
        ),
        "notes": [
            "Il verbale va inviato entro 10 giorni al Prefetto del luogo della violazione.",
            "Non è ammesso il pagamento in misura ridotta, essendo prevista la confisca del veicolo.",
            "Possibili violazioni concorrenti: CAP/CQC, art. 72, art. 79, 085-05.",
            "Non è ammesso il servizio NCC di autocarri per trasporto cose per conto terzi."
        ],
        "fields_to_fill": [
            "uso risultante dalla carta di circolazione / DU",
            "generalità di almeno un passeggero trasportato",
            "eventuale provvedimento di sospensione/revoca autorizzazione",
            "generalità del custode",
            "luogo di custodia del veicolo"
        ],
        "short_ready_text": (
            "Violazione accertata: noleggio con conducente con veicolo non adibito a tale uso. "
            "Norma: art. 85, comma 4, CdS. "
            "Sanzione edittale: da € 1.812,00 a € 7.249,00. "
            "Pagamento in misura ridotta non ammesso. "
            "Accessorie: sospensione patente da 4 a 12 mesi e sequestro del veicolo ai fini della confisca. "
            "Verbale da trasmettere entro 10 giorni al Prefetto del luogo della violazione."
        )
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
            "benché non destinato a tale uso (ovvero, solo per autovetture e motocarrozzette, benché fosse privo di "
            "autorizzazione ovvero, per tutti i veicoli, benché l'autorizzazione fosse sospesa o revocata). "
            "Risultava infatti, in base alle indicazioni del documento di circolazione, che il veicolo doveva essere "
            "adibito a diverso uso. Nella circostanza veniva accertato il trasporto di persone. "
            "Il veicolo è sottoposto a sequestro come da apposito verbale."
        ),
        "notes": [
            "Alla seconda violazione nel triennio si applica la revoca patente.",
            "L'organo accertatore comunica entro 5 giorni al Prefetto i presupposti della revoca."
        ],
        "fields_to_fill": [
            "uso risultante dalla carta di circolazione / DU",
            "generalità di almeno un passeggero trasportato",
            "generalità del custode",
            "luogo di custodia del veicolo",
            "precedente violazione utile nel triennio"
        ],
        "short_ready_text": (
            "Violazione accertata: noleggio con conducente con veicolo non adibito a tale uso, seconda violazione nel triennio. "
            "Norma: art. 85, comma 4, CdS. "
            "Sanzione edittale: da € 1.812,00 a € 7.249,00. "
            "Pagamento in misura ridotta non ammesso. "
            "Accessorie: revoca patente e sequestro del veicolo per confisca. "
            "Comunicazione entro 5 giorni al Prefetto per i presupposti della revoca."
        )
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
            "Utilizzava l'autovettura (o il motoveicolo) sopra indicata, adibita a servizio di noleggio con conducente, "
            "munito della relativa autorizzazione, senza ottemperare alle disposizioni dell'art. 3 della L. 21/1992 "
            "ovvero alle disposizioni di cui all'art. 11 della L. 21/1992. "
            "Il documento di circolazione è ritirato e trasmesso all'UMC competente. "
            "Il conducente è autorizzato a condurre il veicolo per la via più breve fino al luogo indicato, "
            "con l'avvertenza che lo stesso sarà sottoposto a fermo amministrativo per tutta la durata della sospensione."
        ),
        "notes": [
            "Se il conducente non è titolare dell’autorizzazione, la violazione va notificata al titolare.",
            "Non contestare come autonoma violazione il mero mancato rientro in rimessa dopo ogni servizio.",
            "Verificare con attenzione prenotazione, stazionamento, foglio di servizio, sede/rimessa."
        ],
        "fields_to_fill": [
            "specificare se la violazione riguarda art. 3 o art. 11 L. 21/1992",
            "descrizione concreta del fatto accertato",
            "UMC competente",
            "luogo verso cui autorizzare la marcia per la via più breve",
            "titolare dell'autorizzazione se diverso dal conducente"
        ],
        "short_ready_text": (
            "Violazione accertata: utilizzo del veicolo NCC in violazione degli artt. 3 o 11 della L. 21/1992. "
            "Norma: art. 85, comma 4-bis, CdS. "
            "PMR € 178,00; riduzione 30% € 124,60; oltre 60 giorni € 336,00; "
            "edittale da € 178,00 a € 672,00. "
            "Accessoria: sospensione del documento di circolazione per 1 mese."
        )
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
            "Utilizzava l'autovettura (o il motoveicolo) sopra indicata, adibita a servizio di noleggio con conducente, "
            "munito della relativa autorizzazione, senza ottemperare alle disposizioni dell'art. 3 della L. 21/1992 "
            "ovvero alle disposizioni di cui all'art. 11 della L. 21/1992. "
            "Il documento di circolazione è ritirato e trasmesso all'UMC competente."
        ),
        "notes": [
            "Seconda violazione nel quinquennio.",
            "Se il conducente non è titolare, risponde il titolare dell’autorizzazione."
        ],
        "fields_to_fill": [
            "specificare se la violazione riguarda art. 3 o art. 11 L. 21/1992",
            "descrizione concreta del fatto accertato",
            "UMC competente",
            "precedente violazione utile nel quinquennio"
        ],
        "short_ready_text": (
            "Violazione accertata: utilizzo del veicolo NCC in violazione degli artt. 3 o 11 della L. 21/1992, "
            "seconda violazione nel quinquennio. "
            "Norma: art. 85, comma 4-bis, CdS. "
            "PMR € 264,00; riduzione 30% € 184,80; oltre 60 giorni € 505,00; "
            "edittale da € 264,00 a € 1.010,00. "
            "Accessoria: sospensione del documento di circolazione da 1 a 2 mesi."
        )
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
            "Utilizzava l'autovettura (o il motoveicolo) sopra indicata, adibita a servizio di noleggio con conducente, "
            "munito della relativa autorizzazione, senza ottemperare alle disposizioni dell'art. 3 della L. 21/1992 "
            "ovvero alle disposizioni di cui all'art. 11 della L. 21/1992."
        ),
        "notes": [
            "Terza violazione nel quinquennio."
        ],
        "fields_to_fill": [
            "specificare se la violazione riguarda art. 3 o art. 11 L. 21/1992",
            "descrizione concreta del fatto accertato",
            "precedenti violazioni utili nel quinquennio"
        ],
        "short_ready_text": (
            "Violazione accertata: utilizzo del veicolo NCC in violazione degli artt. 3 o 11 della L. 21/1992, "
            "terza violazione nel quinquennio. "
            "Norma: art. 85, comma 4-bis, CdS. "
            "PMR € 356,00; riduzione 30% € 249,20; oltre 60 giorni € 672,00; "
            "edittale da € 356,00 a € 1.344,00. "
            "Accessoria: sospensione del documento di circolazione da 2 a 4 mesi."
        )
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
            "Utilizzava l'autovettura (o il motoveicolo) sopra indicata, adibita a servizio di noleggio con conducente, "
            "munito della relativa autorizzazione, senza ottemperare alle disposizioni dell'art. 3 della L. 21/1992 "
            "ovvero alle disposizioni di cui all'art. 11 della L. 21/1992."
        ),
        "notes": [
            "Quarta o successiva violazione nel quinquennio."
        ],
        "fields_to_fill": [
            "specificare se la violazione riguarda art. 3 o art. 11 L. 21/1992",
            "descrizione concreta del fatto accertato",
            "progressione completa delle violazioni nel quinquennio"
        ],
        "short_ready_text": (
            "Violazione accertata: utilizzo del veicolo NCC in violazione degli artt. 3 o 11 della L. 21/1992, "
            "quarta o successiva nel quinquennio. "
            "Norma: art. 85, comma 4-bis, CdS. "
            "PMR € 528,00; riduzione 30% € 369,60; oltre 60 giorni € 1.010,00; "
            "edittale da € 528,00 a € 2.020,00. "
            "Accessoria: sospensione del documento di circolazione da 4 a 8 mesi."
        )
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
            "Utilizzava il veicolo sopra indicato, adibito a servizio di noleggio con conducente, "
            "senza ottemperare alle norme in vigore ovvero alle condizioni di cui all'autorizzazione. "
            "Veniva accertato che ..."
        ),
        "notes": [
            "Rientrano qui le prescrizioni diverse dagli artt. 3 e 11 L. 21/1992.",
            "Verificare regolamenti comunali/locali, ZTL, modalità di servizio, ruolo CCIAA."
        ],
        "fields_to_fill": [
            "specifica prescrizione autorizzativa violata",
            "descrizione concreta del fatto accertato",
            "eventuale regolamento locale applicabile"
        ],
        "short_ready_text": (
            "Violazione accertata: circolazione con NCC in violazione di altre prescrizioni dell'autorizzazione. "
            "Norma: art. 85, comma 4-ter, CdS. "
            "PMR € 86,00; riduzione 30% € 60,20; oltre 60 giorni € 169,00; "
            "edittale da € 86,00 a € 338,00. "
            "Sanzioni accessorie non previste."
        )
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
            "munito di patente ma non del prescritto certificato di abilitazione professionale / titolo "
            "professionale richiesto per il servizio svolto."
        ),
        "notes": [
            "Da valutare il concorso con le violazioni ex art. 85 CdS.",
            "Verificare se per il servizio concreto fosse richiesto KB / KA / CQC."
        ],
        "fields_to_fill": [
            "titolo professionale mancante (KB / KA / CQC)",
            "tipo di veicolo e servizio svolto",
            "eventuale affidante del veicolo"
        ],
        "short_ready_text": (
            "Violazione concorrente: guida del veicolo adibito al servizio senza il prescritto titolo professionale. "
            "Norma: art. 116, commi 16 e 18, CdS. "
            "PMR € 408,00; riduzione 30% € 285,60; oltre 60 giorni € 817,00; "
            "edittale da € 408,00 a € 1.634,00. "
            "Accessoria: fermo del veicolo per 60 giorni."
        )
    }
}

# =========================
# STATO CONVERSAZIONI
# =========================

user_states = {}

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
    if v.get("fields_to_fill"):
        lines.append("")
        lines.append("DATI DA COMPLETARE")
        for f in v["fields_to_fill"]:
            lines.append(f"- {f}")
    if v.get("short_ready_text"):
        lines.append("")
        lines.append("VERBALE SINTETICO PRONTO")
        lines.append(v["short_ready_text"])
    if v.get("notes"):
        lines.append("")
        lines.append("NOTE OPERATIVE")
        for n in v["notes"]:
            lines.append(f"- {n}")
    lines.append("")
    lines.append("AVVERTENZA")
    lines.append("Verificare sempre normativa vigente, prontuario del comando, disciplina locale e dati concreti del caso.")
    return "\n".join(lines)

def format_compact_violation(code):
    v = VIOLATIONS[code]
    lines = []
    lines.append(f"{code} | {v['article']} | {v['title']}")
    lines.append(f"- PMR: {v['pmr']}")
    lines.append(f"- Riduzione 30%: {v['reduced_30']}")
    lines.append(f"- Oltre 60 gg: {v['over_60']}")
    lines.append(f"- Limiti edittali: {v['edictal']}")
    lines.append("- Sanzioni accessorie:")
    for a in v["accessories"]:
        lines.append(f"  • {a}")
    lines.append("- Dicitura verbale:")
    lines.append(f"  {v['verbal_text']}")
    if v.get("fields_to_fill"):
        lines.append("- Dati da completare:")
        for f in v["fields_to_fill"]:
            lines.append(f"  • {f}")
    if v.get("short_ready_text"):
        lines.append("- Verbale sintetico pronto:")
        lines.append(f"  {v['short_ready_text']}")
    return "\n".join(lines)

def format_multiple(main_code, concurrent_codes=None, extra_notes=None):
    if concurrent_codes is None:
        concurrent_codes = []
    if extra_notes is None:
        extra_notes = []

    v = VIOLATIONS[main_code]

    lines = []
    lines.append("ESITO FINALE")
    lines.append(v["title"])
    lines.append("")
    lines.append("RIFERIMENTO")
    lines.append(v["article"])
    lines.append("")
    lines.append("VOCE OPERATIVA")
    lines.append(main_code)
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

    if v.get("fields_to_fill"):
        lines.append("")
        lines.append("DATI DA COMPLETARE")
        for f in v["fields_to_fill"]:
            lines.append(f"- {f}")

    if v.get("short_ready_text"):
        lines.append("")
        lines.append("VERBALE SINTETICO PRONTO")
        lines.append(v["short_ready_text"])

    if v.get("notes"):
        lines.append("")
        lines.append("NOTE OPERATIVE")
        for n in v["notes"]:
            lines.append(f"- {n}")

    if concurrent_codes:
        lines.append("")
        lines.append("VIOLAZIONI CONCORRENTI POSSIBILI")
        for code in concurrent_codes:
            lines.append("")
            lines.append(format_compact_violation(code))

    if extra_notes:
        lines.append("")
        lines.append("ULTERIORI VERIFICHE")
        for note in extra_notes:
            lines.append(f"- {note}")

    lines.append("")
    lines.append("AVVERTENZA")
    lines.append("Verificare sempre normativa vigente, prontuario del comando, disciplina locale e dati concreti del caso.")

    return "\n".join(lines)

# =========================
# MOTORE DECISIONALE
# =========================

def decide_violation(answers):
    vehicle_authorized = answers.get("vehicle_authorized")
    service_to_third = answers.get("service_to_third")
    service_context = answers.get("service_context")
    violation_type = answers.get("violation_type")
    recurrence = answers.get("recurrence")
    kb = answers.get("kb")
    public_waiting = answers.get("public_waiting")
    taxi_commune = answers.get("taxi_commune")
    booking = answers.get("booking")
    separate_payment = answers.get("separate_payment")

    concurrent = []
    notes = []

    if kb == "no":
        concurrent.append("116-06")

    # trasporto accessorio / navetta / parking / struttura
    if service_context == "b" and separate_payment == "no":
        return None, concurrent, [
            "Il caso può rientrare in navetta / trasporto accessorio collegato ad attività propria.",
            "Verificare che il servizio sia riservato a clienti propri della struttura o attività.",
            "Verificare che non vi sia corrispettivo separato specifico per il trasporto.",
            "Verificare che non si tratti in concreto di servizio aperto a utenza indifferenziata."
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

    # stazionamento pubblico senza prenotazione
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
            "1) Il veicolo è autorizzato/adibito a NCC?\n\n"
            "Rispondi:\n"
            "si / no"
        )

    elif step == "service_to_third":
        bot.send_message(
            chat_id,
            "2) Il conducente sta trasportando o mettendosi a disposizione di clienti/passeggeri come servizio NCC o simile?\n\n"
            "Rispondi:\n"
            "si = trasporto clienti/passeggeri\n"
            "no = non sta facendo servizio verso clienti\n"
            "dubbio = situazione non ancora chiara"
        )

    elif step == "service_context":
        bot.send_message(
            chat_id,
            "3) Il servizio in esame rientra in quale situazione?\n\n"
            "Rispondi con UNA sola lettera:\n"
            "a = servizio dichiarato come NCC / taxi / autobus autorizzato\n"
            "b = navetta o trasporto collegato a hotel, parcheggio, struttura o attività propria\n"
            "c = non chiaro / da verificare"
        )

    elif step == "separate_payment":
        bot.send_message(
            chat_id,
            "4) Il trasporto ha un prezzo specifico separato?\n\n"
            "Rispondi:\n"
            "si = il cliente paga proprio il trasporto\n"
            "no = il trasporto non ha un prezzo separato / è compreso / è accessorio"
        )

    elif step == "violation_type":
        bot.send_message(
            chat_id,
            "5) Se il veicolo è NCC, la violazione riguarda:\n\n"
            "art3_11 = artt. 3 o 11 L. 21/1992\n"
            "other_auth = altre prescrizioni dell'autorizzazione\n"
            "none = non chiaro / non applicabile"
        )

    elif step == "public_waiting":
        bot.send_message(
            chat_id,
            "6) Il veicolo stazionava/sostava su area pubblica in attesa?\n\n"
            "Rispondi:\n"
            "si / no"
        )

    elif step == "taxi_commune":
        bot.send_message(
            chat_id,
            "7) Il fatto è avvenuto in un comune dove è esercitato il servizio taxi?\n\n"
            "Rispondi:\n"
            "si / no"
        )

    elif step == "booking":
        bot.send_message(
            chat_id,
            "8) Esiste prenotazione documentabile / foglio di servizio / contratto?\n\n"
            "Rispondi:\n"
            "si / no"
        )

    elif step == "recurrence":
        bot.send_message(
            chat_id,
            "9) Indica la progressione della violazione.\n\n"
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
            "10) Il conducente ha il titolo professionale richiesto (KB/KA/CQC se dovuto)?\n\n"
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
                    lines.append("")
                    lines.append(format_compact_violation(code))
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
            next_step(chat_id, "service_context")
            ask_step(chat_id)
        else:
            bot.reply_to(message, "Rispondi solo con: si / no / dubbio")

    elif step == "service_context":
        if text in {"a", "b", "c"}:
            set_answer(chat_id, "service_context", text)
            next_step(chat_id, "separate_payment")
            ask_step(chat_id)
        else:
            bot.reply_to(message, "Rispondi solo con: a / b / c")

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
