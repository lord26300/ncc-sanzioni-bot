import os
import json
import threading
from flask import Flask
import telebot

TOKEN = os.getenv("TOKEN")
bot = telebot.TeleBot(TOKEN)

app = Flask(__name__)

ADMIN_ID = 242294061

# GIF/animazione di benvenuto
WELCOME_MEDIA_PATH = "welcome.mp4"
WELCOME_MEDIA_ENABLED = False

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

NCC_DB = {
    "norme": {
        "L21_3_11": {
            "norma": "L. 21/1992 artt. 3 e 11",
            "tema": "Prescrizioni autorizzazione/licenza NCC",
            "uso_operativo": "Verificare se la violazione ricade nelle prescrizioni tipiche del titolo NCC e nel corretto esercizio del servizio."
        },
        "CDS_85_4": {
            "norma": "CdS art. 85 c. 4",
            "tema": "Veicolo non adibito/autorizzato a NCC",
            "uso_operativo": "Ramo sanzionatorio quando il servizio è svolto con veicolo non autorizzato/adibito a tale uso."
        },
        "CDS_85_4BIS": {
            "norma": "CdS art. 85 c. 4-bis",
            "tema": "Violazione artt. 3 o 11 L. 21/1992",
            "uso_operativo": "Ramo per violazioni collegate alle prescrizioni della L. 21/1992, con progressione nel quinquennio."
        },
        "CDS_85_4TER": {
            "norma": "CdS art. 85 c. 4-ter",
            "tema": "Altre prescrizioni autorizzazione NCC",
            "uso_operativo": "Ramo per violazioni di prescrizioni diverse da artt. 3 e 11 L. 21/1992."
        },
        "CDS_116_14": {
            "norma": "CdS art. 116 c. 14",
            "tema": "Incauto affidamento",
            "uso_operativo": "Quando il soggetto che ha disponibilità del veicolo lo affida a persona priva dei titoli richiesti."
        },
        "CDS_116_15_17": {
            "norma": "CdS art. 116 c. 15 e 17",
            "tema": "Guida senza patente o patente non idonea",
            "uso_operativo": "Prima violazione amministrativa, recidiva biennale o reiterazione; può concorrere con il ramo NCC."
        },
        "CDS_116_15BIS": {
            "norma": "CdS art. 116 c. 15-bis",
            "tema": "Patente diversa in casi tipizzati",
            "uso_operativo": "Ipotesi specifica distinta dalla guida senza patente vera e propria."
        },
        "CDS_116_16_18": {
            "norma": "CdS art. 116 c. 16 e 18",
            "tema": "Guida senza CAP/KB/KA/CQC",
            "uso_operativo": "Per servizio pubblico/NCC senza titolo professionale richiesto."
        },
        "CDS_126_11": {
            "norma": "CdS art. 126 c. 11",
            "tema": "CAP/CQC scaduti",
            "uso_operativo": "Quando il titolo professionale esiste ma non è più valido."
        },
        "CDS_180": {
            "norma": "CdS art. 180",
            "tema": "Mancanza materiale del documento",
            "uso_operativo": "Solo quando il titolo esiste ma non è esibito nell’immediato."
        }
    },

    "voci": {
        "085-02": {
            "norma": "CdS art. 85 c. 4",
            "titolo": "Veicolo non adibito a tale uso – 1ª violazione",
            "quando_usarla": "Servizio NCC svolto con veicolo non regolarmente adibito/autorizzato a NCC.",
            "cluster": "mezzo_non_ncc"
        },
        "085-04": {
            "norma": "CdS art. 85 c. 4",
            "titolo": "Veicolo non adibito – 2ª violazione nel triennio",
            "quando_usarla": "Quando ricorre seconda violazione nel triennio sul ramo del veicolo non autorizzato.",
            "cluster": "mezzo_non_ncc"
        },
        "085-05": {
            "norma": "CdS art. 85 c. 4-bis + L. 21/1992",
            "titolo": "Violazione artt. 3 e 11 – 1ª nel quinquennio",
            "quando_usarla": "Quando il veicolo è NCC e la violazione riguarda artt. 3 o 11.",
            "cluster": "mezzo_ncc_art3_11"
        },
        "085-06": {
            "norma": "CdS art. 85 c. 4-bis + L. 21/1992",
            "titolo": "Violazione artt. 3 e 11 – 2ª nel quinquennio",
            "quando_usarla": "Come sopra, con progressione sanzionatoria.",
            "cluster": "mezzo_ncc_art3_11"
        },
        "085-07": {
            "norma": "CdS art. 85 c. 4-bis + L. 21/1992",
            "titolo": "Violazione artt. 3 e 11 – 3ª nel quinquennio",
            "quando_usarla": "Come sopra.",
            "cluster": "mezzo_ncc_art3_11"
        },
        "085-08": {
            "norma": "CdS art. 85 c. 4-bis + L. 21/1992",
            "titolo": "Violazione artt. 3 e 11 – 4ª o successiva",
            "quando_usarla": "Come sopra.",
            "cluster": "mezzo_ncc_art3_11"
        },
        "085-09": {
            "norma": "CdS art. 85 c. 4-ter",
            "titolo": "Altre prescrizioni dell’autorizzazione NCC",
            "quando_usarla": "Quando la violazione non ricade negli artt. 3 e 11 ma in altre prescrizioni dell’autorizzazione.",
            "cluster": "mezzo_ncc_altre_prescrizioni"
        },
        "116-01": {
            "norma": "CdS art. 116 c. 14",
            "titolo": "Incauto affidamento",
            "quando_usarla": "Veicolo affidato a soggetto privo dei titoli richiesti.",
            "cluster": "conducente"
        },
        "116-02": {
            "norma": "CdS art. 116 c. 15 e 17",
            "titolo": "Guida senza patente / prima violazione amministrativa",
            "quando_usarla": "Mai conseguita, revocata, non rinnovata per mancanza requisiti o categoria non rientrante nel 15-bis.",
            "cluster": "conducente"
        },
        "116-03": {
            "norma": "CdS art. 116 c. 15 e 17",
            "titolo": "Recidiva biennale nella violazione amministrativa",
            "quando_usarla": "Seconda violazione amministrativa nel biennio, senza presupposti della reiterazione penale.",
            "cluster": "conducente"
        },
        "116-04": {
            "norma": "CdS art. 116 c. 15 e 17",
            "titolo": "Reiterazione nella guida senza patente",
            "quando_usarla": "Quando ricorrono i presupposti di illecito penale richiamati dal prontuario.",
            "cluster": "conducente"
        },
        "116-05": {
            "norma": "CdS art. 116 c. 15-bis",
            "titolo": "Patente diversa ma rientrante nei casi tipizzati",
            "quando_usarla": "Ipotesi tassative di patente di categoria diversa.",
            "cluster": "conducente"
        },
        "116-06": {
            "norma": "CdS art. 116 c. 16 e 18",
            "titolo": "Guida senza CAP o CQC",
            "quando_usarla": "Servizio NCC senza KB/KA/CQC quando richiesti.",
            "cluster": "conducente"
        }
    },

    "casi_tipici": {
        "A_abusivo_totale_mezzo_proprio": {
            "descrizione": "Un privato usa il proprio veicolo per trasporto verso terzi assimilabile a NCC.",
            "possibili_esiti": ["085-02", "085-04", "116-02", "116-03", "116-04", "116-05", "116-06"],
            "note": [
                "Se manca il corretto inquadramento NCC del veicolo: valutare il ramo art. 85 c. 4.",
                "Se manca patente idonea: valutare art. 116 c. 15 / 15-bis secondo il caso.",
                "Se manca il titolo professionale richiesto: valutare 116-06.",
                "Possibile concorso di più violazioni."
            ]
        },
        "B_titolare_ncc_procaccia_clienti": {
            "descrizione": "Il mezzo è NCC ma il servizio va verificato rispetto alle prescrizioni della L. 21/1992 e dell’autorizzazione.",
            "possibili_esiti": ["085-05", "085-06", "085-07", "085-08", "085-09", "116-06"],
            "note": [
                "Se la violazione riguarda artt. 3 o 11 L. 21/1992: ramo 085-05 / 085-06 / 085-07 / 085-08.",
                "Se riguarda altre prescrizioni dell’autorizzazione: 085-09.",
                "Se il conducente non ha titolo professionale valido: può concorrere 116-06."
            ]
        },
        "C_impresa_agenzia_mezzo_aziendale": {
            "descrizione": "Impresa/agenzia che trasporta clienti con dipendente e mezzo aziendale.",
            "possibili_esiti": ["085-02", "085-04", "085-05", "085-09", "116-06"],
            "note": [
                "Prima domanda pratica: trasporto verso terzi / assimilabile a NCC oppure attività accessoria dell’impresa?",
                "Se il servizio è organizzato come trasporto a terzi, il rischio è la qualificazione come servizio NCC non autorizzato.",
                "Se il trasporto è realmente accessorio al servizio principale dell’impresa e riservato ai propri clienti, la qualificazione va verificata con attenzione."
            ]
        },
        "D_navetta_parcheggio_hotel": {
            "descrizione": "Navetta interna / parcheggio / hotel / struttura.",
            "possibili_esiti": ["085-02", "085-04"],
            "note": [
                "Va distinta la navetta interna/collegamento funzionale dal trasporto verso terzi autonomamente venduto.",
                "Se il trasporto è compreso nel servizio principale e dedicato ai soli clienti, il caso va valutato come attività accessoria e non automaticamente come NCC.",
                "Se invece il trasporto è offerto come servizio a terzi autonomo, aumenta il rischio di riconduzione al ramo NCC abusivo.",
                "Verificare copertura documentale e contrattuale."
            ]
        },
        "E_veicolo_ncc_conducente_non_legittimato": {
            "descrizione": "Il veicolo risulta NCC, ma il conducente non ha patente idonea o titolo professionale richiesto.",
            "possibili_esiti": ["116-01", "116-02", "116-03", "116-04", "116-05", "116-06"],
            "note": [
                "Il nucleo sanzionatorio principale è spesso sul ramo 116.",
                "Può aggiungersi l’incauto affidamento 116-01 a carico di chi ha affidato il veicolo."
            ]
        },
        "F_veicolo_non_ncc_ma_conducente_titolato": {
            "descrizione": "Il conducente ha titolo ma usa mezzo non autorizzato/adibito a NCC.",
            "possibili_esiti": ["085-02", "085-04", "116-02", "116-03", "116-04", "116-05", "116-06"],
            "note": [
                "Il fatto che il conducente abbia titolo non sana l’uso di un mezzo non autorizzato/adibito a NCC.",
                "Valutare prioritariamente il ramo art. 85 c. 4.",
                "Se inoltre mancano patente idonea o requisiti documentali, il ramo 116 può concorrere."
            ]
        }
    },

    "checklist_operativa": [
        "Capire se il trasporto è verso terzi / assimilabile a NCC oppure attività accessoria dell’impresa.",
        "Identificare il soggetto che svolge il trasporto: privato, titolare NCC, impresa/agenzia, gestore navetta/parcheggio.",
        "Verificare come viene acquisita la clientela: prenotazione preventiva, procacciamento diretto, servizio per clienti propri, navetta interna.",
        "Verificare se il servizio è riservato ai clienti della struttura o è offerto come trasporto a terzi.",
        "Verificare se il veicolo è regolarmente adibito/autorizzato a NCC.",
        "Verificare patente idonea del conducente.",
        "Verificare titolo professionale richiesto (KB/KA/CQC) o eventuale scadenza.",
        "Se il veicolo è NCC, distinguere: violazione artt. 3 o 11 L. 21/1992 / altre prescrizioni / progressione nel quinquennio.",
        "Valutare eventuale concorso con incauto affidamento nei confronti dell’avente disponibilità del veicolo."
    ],

    "matrice_rapida": {
        "Mezzo non autorizzato NCC": ["085-02", "085-04"],
        "Mezzo NCC + violazione artt. 3 o 11 L. 21/1992": ["085-05", "085-06", "085-07", "085-08"],
        "Mezzo NCC + altre prescrizioni autorizzazione": ["085-09"],
        "Conducente senza patente idonea": ["116-02", "116-03", "116-04", "116-05"],
        "Conducente senza KB/KA/CQC": ["116-06"],
        "Veicolo affidato a soggetto privo dei titoli richiesti": ["116-01"],
        "Titolo professionale esistente ma scaduto": ["CDS_126_11"],
        "Documento esistente ma non esibito": ["CDS_180"]
    },

    "documenti_controllo": [
        "Carta di circolazione / DU",
        "Autorizzazione NCC / titolo abilitativo",
        "Patente del conducente",
        "KB / KA / CQC se richiesti",
        "Iscrizione a ruolo / posizione del conducente",
        "Prenotazione documentabile",
        "Foglio di servizio",
        "Eventuale documentazione contrattuale / commerciale / fiscale",
        "Eventuali regolamenti locali / accesso porto / ZTL"
    ]
}

ARTICOLI_DB = {
    "art85": {
        "titolo": "CdS art. 85",
        "testo": (
            "Art. 85 CdS – Servizio di noleggio con conducente.\n\n"
            "Uso operativo nel bot:\n"
            "- comma 4: veicolo non adibito / non autorizzato a NCC\n"
            "- comma 4-bis: violazioni degli artt. 3 e 11 della L. 21/1992\n"
            "- comma 4-ter: altre prescrizioni dell’autorizzazione NCC\n\n"
            "Per il dettaglio sanzionatorio il bot usa le voci:\n"
            "085-02, 085-04, 085-05, 085-06, 085-07, 085-08, 085-09."
        ),
        "link": "https://www.normattiva.it/"
    },
    "art116": {
        "titolo": "CdS art. 116",
        "testo": (
            "Art. 116 CdS – Requisiti per la guida dei veicoli.\n\n"
            "Uso operativo nel bot:\n"
            "- comma 14: incauto affidamento\n"
            "- commi 15 e 17: guida senza patente / recidiva / reiterazione\n"
            "- comma 15-bis: patente diversa in casi tipizzati\n"
            "- commi 16 e 18: guida senza CAP / KB / KA / CQC\n\n"
            "Per il dettaglio operativo il bot usa le voci:\n"
            "116-01, 116-02, 116-03, 116-04, 116-05, 116-06."
        ),
        "link": "https://www.normattiva.it/"
    },
    "art3l21": {
        "titolo": "L. 21/1992 art. 3",
        "testo": (
            "Legge 21/1992 – art. 3.\n\n"
            "Uso operativo nel bot:\n"
            "- la richiesta del servizio deve essere avanzata presso la sede o la rimessa, "
            "anche mediante strumenti tecnologici;\n"
            "- lo stazionamento dei mezzi deve avvenire all’interno delle rimesse;\n"
            "- sede operativa e almeno una rimessa devono essere nel territorio consentito.\n\n"
            "Se il mezzo è regolarmente NCC ma viola queste prescrizioni, il bot orienta verso il ramo 085-05 / 085-06 / 085-07 / 085-08."
        ),
        "link": "https://www.normattiva.it/"
    },
    "art11l21": {
        "titolo": "L. 21/1992 art. 11",
        "testo": (
            "Legge 21/1992 – art. 11.\n\n"
            "Uso operativo nel bot:\n"
            "- divieto di sosta in posteggio di stazionamento su suolo pubblico nei comuni dove è esercitato il servizio taxi;\n"
            "- nei casi consentiti, verifica dell’area di sosta autorizzata;\n"
            "- controllo su prenotazione / foglio di servizio / modalità operative del servizio.\n\n"
            "Se il mezzo è NCC e la violazione ricade su queste prescrizioni, il bot orienta verso il ramo 085-05 / 085-06 / 085-07 / 085-08."
        ),
        "link": "https://www.normattiva.it/"
    }
}

# =========================
# ACCESSO / AUTORIZZAZIONI
# =========================

access_data = {
    "authorized_users": {ADMIN_ID},
    "pending_users": {},
    "rejected_users": set()
}

def save_access_data():
    return

def is_admin(user_id):
    return user_id == ADMIN_ID

def is_authorized(user_id):
    return user_id in access_data["authorized_users"]

def is_pending(user_id):
    return str(user_id) in access_data["pending_users"]

def add_pending(user):
    uid = str(user.id)
    if uid not in access_data["pending_users"]:
        access_data["pending_users"][uid] = {
            "id": user.id,
            "first_name": user.first_name or "",
            "username": user.username or "",
        }
        save_access_data()

def approve_user(user_id):
    uid_str = str(user_id)
    if uid_str in access_data["pending_users"]:
        del access_data["pending_users"][uid_str]
    access_data["authorized_users"].add(user_id)
    access_data["rejected_users"].discard(user_id)
    save_access_data()

def reject_user(user_id):
    uid_str = str(user_id)
    if uid_str in access_data["pending_users"]:
        del access_data["pending_users"][uid_str]
    access_data["rejected_users"].add(user_id)
    access_data["authorized_users"].discard(user_id)
    save_access_data()

def revoke_user(user_id):
    if user_id == ADMIN_ID:
        return False
    access_data["authorized_users"].discard(user_id)
    save_access_data()
    return True

def send_welcome_media(chat_id):
    if not WELCOME_MEDIA_ENABLED:
        return
    if not os.path.exists(WELCOME_MEDIA_PATH):
        return
    try:
        with open(WELCOME_MEDIA_PATH, "rb") as media_file:
            bot.send_animation(chat_id, media_file)
    except Exception:
        pass

def request_access_text():
    return (
        "Benvenuto in NCC Sanzioni Bot.\n\n"
        "Questo assistente supporta l’analisi preliminare delle possibili violazioni in materia NCC, con indicazione di:\n"
        "- riferimento normativo\n"
        "- voce operativa\n"
        "- importi\n"
        "- sanzioni accessorie\n"
        "- dicitura verbale\n"
        "- verifiche finali\n\n"
        "Uso interno-operativo.\n"
        "Le risultanze vanno sempre verificate su normativa vigente, prontuario e disposizioni di servizio.\n\n"
        "Il tuo accesso è in attesa di approvazione amministratore."
    )

def authorized_start_text(user_id):
    return (
        f"Benvenuto in NCC Sanzioni Bot.\n\n"
        f"Accesso autorizzato.\n"
        f"Il tuo user id è: {user_id}\n\n"
        "Comandi disponibili:\n"
        "/caso - descrivi liberamente il fatto\n"
        "/checklist - controlli operativi\n"
        "/documenti - documenti da controllare\n"
        "/norme - riferimenti principali\n"
        "/art85 - leggi art. 85 CdS\n"
        "/art116 - leggi art. 116 CdS\n"
        "/art3l21 - leggi art. 3 L. 21/1992\n"
        "/art11l21 - leggi art. 11 L. 21/1992\n"
        "/reset - annulla caso in corso"
    )

def notify_admin_new_request(user):
    username_line = f"@{user.username}" if user.username else "-"
    text = (
        "Richiesta accesso al bot\n\n"
        f"Nome: {user.first_name or '-'}\n"
        f"Username: {username_line}\n"
        f"ID: {user.id}\n\n"
        f"Per approvare:\n/approva {user.id}\n\n"
        f"Per rifiutare:\n/rifiuta {user.id}"
    )
    bot.send_message(ADMIN_ID, text)

def ensure_authorized(message):
    uid = message.from_user.id
    if is_admin(uid) or is_authorized(uid):
        return True

    send_welcome_media(message.chat.id)

    if is_pending(uid):
        bot.reply_to(
            message,
            "Accesso non ancora autorizzato.\nLa tua richiesta è già stata inviata all'amministratore."
        )
        return False

    add_pending(message.from_user)
    notify_admin_new_request(message.from_user)
    bot.reply_to(message, request_access_text())
    return False

# =========================
# STATO CONVERSAZIONI
# =========================

user_states = {}

# mode:
# - free_case: attesa descrizione libera
# - clarification: attesa risposta a domanda integrativa

# =========================
# FUNZIONI FORMATO
# =========================

def clear_case(chat_id):
    if chat_id in user_states:
        del user_states[chat_id]

def get_state(chat_id):
    return user_states.get(chat_id)

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

    lines.append(article_shortcuts_from_result(main_code, concurrent_codes))
    
    lines.append("")
    lines.append("AVVERTENZA")
    lines.append("Verificare sempre normativa vigente, prontuario del comando, disciplina locale e dati concreti del caso.")
    
    return "\n".join(lines)

def format_norme_from_db():
    lines = ["RIFERIMENTI NORMATIVI NCC\n"]
    for item in NCC_DB["norme"].values():
        lines.append(f"- {item['norma']}")
        lines.append(f"  Tema: {item['tema']}")
        lines.append(f"  Uso operativo: {item['uso_operativo']}")
        lines.append("")
    return "\n".join(lines).strip()

def format_documenti_from_db():
    lines = ["DOCUMENTI / ELEMENTI DA CONTROLLARE\n"]
    for item in NCC_DB["documenti_controllo"]:
        lines.append(f"- {item}")
    return "\n".join(lines)

def format_checklist_from_db():
    lines = ["CHECKLIST OPERATIVA NCC\n"]
    for i, item in enumerate(NCC_DB["checklist_operativa"], start=1):
        lines.append(f"{i}. {item}")
    return "\n".join(lines)

def match_case_from_text(text):
    t = text.lower()

    # casi tipici di primo orientamento
    if any(x in t for x in ["veicolo privato", "auto privata", "mezzo privato", "senza autorizzazione ncc", "abusivo"]):
        return "A_abusivo_totale_mezzo_proprio"

    if any(x in t for x in ["ncc", "prenotazione", "foglio di servizio", "rimessa", "staziona", "sosta"]):
        return "B_titolare_ncc_procaccia_clienti"

    if any(x in t for x in ["agenzia", "impresa", "mezzo aziendale", "dipendente"]):
        return "C_impresa_agenzia_mezzo_aziendale"

    if any(x in t for x in ["navetta", "hotel", "albergo", "parcheggio", "parking", "struttura ricettiva"]):
        return "D_navetta_parcheggio_hotel"

    if any(x in t for x in ["senza kb", "senza cqc", "manca kb", "manca cqc", "senza patente", "patente non idonea"]):
        return "E_veicolo_ncc_conducente_non_legittimato"

    if any(x in t for x in ["con kb", "titolo presente", "conducente titolato"]) and any(x in t for x in ["veicolo privato", "non ncc"]):
        return "F_veicolo_non_ncc_ma_conducente_titolato"

    return None

def format_case_hint(case_key):
    case_data = NCC_DB["casi_tipici"][case_key]
    lines = []
    lines.append("INQUADRAMENTO OPERATIVO PRELIMINARE")
    lines.append(case_data["descrizione"])
    lines.append("")
    lines.append("POSSIBILI ESITI")
    for code in case_data["possibili_esiti"]:
        if code in VIOLATIONS:
            lines.append(f"- {code} | {VIOLATIONS[code]['article']} | {VIOLATIONS[code]['title']}")
        elif code in NCC_DB["norme"]:
            lines.append(f"- {code} | {NCC_DB['norme'][code]['norma']} | {NCC_DB['norme'][code]['tema']}")
        else:
            lines.append(f"- {code}")
    lines.append("")
    lines.append("NOTE")
    for n in case_data["note"]:
        lines.append(f"- {n}")
    return "\n".join(lines)

ARTICOLI_DB = {
    "art85": {
        "titolo": "CdS art. 85",
        "testo": (
            "Art. 85 CdS – Servizio di noleggio con conducente.\n\n"
            "Uso operativo nel bot:\n"
            "- comma 4: veicolo non adibito / non autorizzato a NCC\n"
            "- comma 4-bis: violazioni degli artt. 3 e 11 della L. 21/1992\n"
            "- comma 4-ter: altre prescrizioni dell’autorizzazione NCC\n\n"
            "Per il dettaglio sanzionatorio il bot usa le voci:\n"
            "085-02, 085-04, 085-05, 085-06, 085-07, 085-08, 085-09."
        ),
        "link": "https://www.normattiva.it/"
    },
    "art116": {
        "titolo": "CdS art. 116",
        "testo": (
            "Art. 116 CdS – Requisiti per la guida dei veicoli.\n\n"
            "Uso operativo nel bot:\n"
            "- comma 14: incauto affidamento\n"
            "- commi 15 e 17: guida senza patente / recidiva / reiterazione\n"
            "- comma 15-bis: patente diversa in casi tipizzati\n"
            "- commi 16 e 18: guida senza CAP / KB / KA / CQC\n\n"
            "Per il dettaglio operativo il bot usa le voci:\n"
            "116-01, 116-02, 116-03, 116-04, 116-05, 116-06."
        ),
        "link": "https://www.normattiva.it/"
    },
    "art3l21": {
        "titolo": "L. 21/1992 art. 3",
        "testo": (
            "Legge 21/1992 – art. 3.\n\n"
            "Uso operativo nel bot:\n"
            "- la richiesta del servizio deve essere avanzata presso la sede o la rimessa, "
            "anche mediante strumenti tecnologici;\n"
            "- lo stazionamento dei mezzi deve avvenire all’interno delle rimesse;\n"
            "- sede operativa e almeno una rimessa devono essere nel territorio consentito.\n\n"
            "Se il mezzo è regolarmente NCC ma viola queste prescrizioni, il bot orienta verso il ramo 085-05 / 085-06 / 085-07 / 085-08."
        ),
        "link": "https://www.normattiva.it/"
    },
    "art11l21": {
        "titolo": "L. 21/1992 art. 11",
        "testo": (
            "Legge 21/1992 – art. 11.\n\n"
            "Uso operativo nel bot:\n"
            "- divieto di sosta in posteggio di stazionamento su suolo pubblico nei comuni dove è esercitato il servizio taxi;\n"
            "- nei casi consentiti, verifica dell’area di sosta autorizzata;\n"
            "- controllo su prenotazione / foglio di servizio / modalità operative del servizio.\n\n"
            "Se il mezzo è NCC e la violazione ricade su queste prescrizioni, il bot orienta verso il ramo 085-05 / 085-06 / 085-07 / 085-08."
        ),
        "link": "https://www.normattiva.it/"
    }
}

# =========================
# ANALISI TESTO LIBERO
# =========================

def detect_from_text(text):
    t = text.lower()

    data = {
        "vehicle_authorized": None,   # si/no
        "service_to_third": None,     # si/no/dubbio
        "service_context": None,      # a/b/c
        "violation_type": None,       # art3_11 / other_auth / none
        "recurrence": None,           # first / second_3y / 1_5y / 2_5y / 3_5y / 4plus_5y
        "kb": None,                   # si/no
        "public_waiting": None,       # si/no
        "taxi_commune": None,         # si/no
        "booking": None,              # si/no
        "separate_payment": None      # si/no
    }

    # autorizzazione veicolo
    if any(x in t for x in [
        "veicolo privato", "auto privata", "non autorizzato", "senza autorizzazione ncc",
        "abusivo", "non ncc", "mezzo privato"
    ]):
        data["vehicle_authorized"] = "no"

    if any(x in t for x in [
        "veicolo ncc", "autorizzato ncc", "con autorizzazione ncc", "ncc regolare"
    ]):
        data["vehicle_authorized"] = "si"

    # servizio verso clienti
    if any(x in t for x in [
        "clienti", "passeggeri", "turisti", "a pagamento", "trasporta persone",
        "accompagna clienti", "servizio ncc", "utenza"
    ]):
        data["service_to_third"] = "si"

    # contesto
    if any(x in t for x in ["hotel", "albergo", "parcheggio", "parking", "struttura ricettiva", "navetta"]):
        data["service_context"] = "b"
    elif any(x in t for x in ["taxi", "ncc", "autobus autorizzato", "bus autorizzato"]):
        data["service_context"] = "a"

    # tipo violazione
    if any(x in t for x in [
        "senza prenotazione", "manca prenotazione", "no prenotazione",
        "foglio di servizio", "staziona", "sosta su area pubblica", "attesa clienti",
        "rimessa", "fuori rimessa"
    ]):
        data["violation_type"] = "art3_11"

    if any(x in t for x in [
        "ztl", "regolamento comunale", "altra prescrizione", "condizioni autorizzazione",
        "prescrizione autorizzativa"
    ]):
        data["violation_type"] = "other_auth"

    # recidiva
    if any(x in t for x in ["seconda nel triennio", "2a nel triennio", "recidiva triennio"]):
        data["recurrence"] = "second_3y"
    elif any(x in t for x in ["seconda nel quinquennio", "2a nel quinquennio"]):
        data["recurrence"] = "2_5y"
    elif any(x in t for x in ["terza nel quinquennio", "3a nel quinquennio"]):
        data["recurrence"] = "3_5y"
    elif any(x in t for x in ["quarta nel quinquennio", "quarta o successiva", "4a nel quinquennio"]):
        data["recurrence"] = "4plus_5y"
    elif any(x in t for x in ["prima violazione", "1a violazione", "prima nel quinquennio"]):
        data["recurrence"] = "first"

    # kb/cqc
    if any(x in t for x in ["senza kb", "manca kb", "senza cqc", "manca cqc", "senza ka", "manca ka"]):
        data["kb"] = "no"
    elif any(x in t for x in ["con kb", "kb presente", "cqc presente", "titolo presente"]):
        data["kb"] = "si"

    # sosta/attesa
    if any(x in t for x in ["staziona", "in attesa", "sosta", "fermo in attesa", "attesa clienti"]):
        data["public_waiting"] = "si"

    # comune taxi
    if any(x in t for x in ["comune con taxi", "dove c'è taxi", "porto di civitavecchia", "roma", "milano"]):
        data["taxi_commune"] = "si"

    # prenotazione
    if any(x in t for x in ["senza prenotazione", "no prenotazione", "manca prenotazione"]):
        data["booking"] = "no"
    elif any(x in t for x in ["prenotazione presente", "con prenotazione", "foglio di servizio presente", "contratto presente"]):
        data["booking"] = "si"

    # corrispettivo separato
    if any(x in t for x in ["pagamento separato", "prezzo separato", "corrispettivo separato", "pagano il trasporto"]):
        data["separate_payment"] = "si"
    elif any(x in t for x in ["gratuito", "senza corrispettivo", "compreso nel servizio", "cortesia"]):
        data["separate_payment"] = "no"

    return data

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

    if service_context == "b" and separate_payment == "no":
        return None, concurrent, [
            "Il caso può rientrare in navetta / trasporto accessorio collegato ad attività propria.",
            "Verificare che il servizio sia riservato a clienti propri della struttura o attività.",
            "Verificare che non vi sia corrispettivo separato specifico per il trasporto.",
            "Verificare che non si tratti in concreto di servizio aperto a utenza indifferenziata."
        ]

    if vehicle_authorized == "no" and service_to_third == "si":
        if recurrence == "second_3y":
            return "085-04", concurrent, notes
        return "085-02", concurrent, notes

    if vehicle_authorized == "si" and violation_type == "art3_11":
        if recurrence == "2_5y":
            return "085-06", concurrent, notes
        elif recurrence == "3_5y":
            return "085-07", concurrent, notes
        elif recurrence == "4plus_5y":
            return "085-08", concurrent, notes
        else:
            return "085-05", concurrent, notes

    if vehicle_authorized == "si" and violation_type == "other_auth":
        return "085-09", concurrent, notes

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

def missing_questions(answers):
    questions = []

    if answers.get("vehicle_authorized") is None:
        questions.append({
            "key": "vehicle_authorized",
            "text": "Il veicolo è autorizzato/adibito a NCC?\nRispondi: si / no"
        })

    if answers.get("service_to_third") is None:
        questions.append({
            "key": "service_to_third",
            "text": "Il conducente sta trasportando o mettendosi a disposizione di clienti/passeggeri?\nRispondi: si / no / dubbio"
        })

    if answers.get("service_context") is None:
        questions.append({
            "key": "service_context",
            "text": "Il servizio sembra essere:\na = NCC/taxi/autobus autorizzato\nb = navetta o trasporto collegato a hotel/parcheggio/struttura\nc = non chiaro\nRispondi: a / b / c"
        })

    if answers.get("separate_payment") is None:
        questions.append({
            "key": "separate_payment",
            "text": "Il trasporto ha un prezzo/corrispettivo separato?\nRispondi: si / no"
        })

    # se mezzo non ncc e servizio verso clienti, serve recidiva minima
    if answers.get("vehicle_authorized") == "no" and answers.get("service_to_third") == "si" and answers.get("recurrence") is None:
        questions.append({
            "key": "recurrence",
            "text": "Si tratta di prima violazione o seconda nel triennio?\nRispondi: first / second_3y"
        })

    # se mezzo ncc, serve tipo violazione
    if answers.get("vehicle_authorized") == "si" and answers.get("violation_type") is None:
        questions.append({
            "key": "violation_type",
            "text": "La violazione riguarda:\nart3_11 = artt. 3 o 11 L. 21/1992\nother_auth = altre prescrizioni autorizzative\nnone = non chiaro\nRispondi: art3_11 / other_auth / none"
        })

    # se art3_11 serve recidiva quinquennio
    if answers.get("vehicle_authorized") == "si" and answers.get("violation_type") == "art3_11" and answers.get("recurrence") is None:
        questions.append({
            "key": "recurrence",
            "text": "Indica la progressione nel quinquennio:\nfirst / 2_5y / 3_5y / 4plus_5y"
        })

    if answers.get("kb") is None:
        questions.append({
            "key": "kb",
            "text": "Il conducente ha il titolo professionale richiesto (KB/KA/CQC se dovuto)?\nRispondi: si / no"
        })

    if answers.get("public_waiting") is None:
        questions.append({
            "key": "public_waiting",
            "text": "Il veicolo era in sosta/stazionamento su area pubblica in attesa?\nRispondi: si / no"
        })

    if answers.get("taxi_commune") is None:
        questions.append({
            "key": "taxi_commune",
            "text": "Il fatto avviene in un comune dove è esercitato il servizio taxi?\nRispondi: si / no"
        })

    if answers.get("booking") is None:
        questions.append({
            "key": "booking",
            "text": "Esiste prenotazione documentabile / foglio di servizio / contratto?\nRispondi: si / no"
        })

    return questions

def parse_answer_for_key(key, text):
    t = text.strip().lower()

    if key in ["vehicle_authorized", "kb", "public_waiting", "taxi_commune", "booking", "separate_payment"]:
        if t in {"si", "no"}:
            return t

    if key == "service_to_third":
        if t in {"si", "no", "dubbio"}:
            return t

    if key == "service_context":
        if t in {"a", "b", "c"}:
            return t

    if key == "violation_type":
        if t in {"art3_11", "other_auth", "none"}:
            return t

    if key == "recurrence":
        if t in {"first", "second_3y", "2_5y", "3_5y", "4plus_5y"}:
            return t

    return None

def begin_case_flow(chat_id):
    user_states[chat_id] = {
        "mode": "free_case",
        "free_text": "",
        "answers": {},
        "pending_question": None
    }

def process_case_description(chat_id, text):
    state = user_states[chat_id]
    state["free_text"] = text

    detected = detect_from_text(text)
    state["answers"].update({k: v for k, v in detected.items() if v is not None})

    case_key = match_case_from_text(text)
    main_code, concurrent, notes = decide_violation(state["answers"])
    questions = missing_questions(state["answers"])

    # Se il bot ha una base interna sufficiente e nessun dato manca
    if main_code and len(questions) == 0:
        result = format_multiple(main_code, concurrent, notes)

        if need_external_source_notice(state["answers"]):
            result += (
                "\n\nAVVISO OPERATORE\n"
                "Il caso è stato analizzato principalmente con il database interno del bot, "
                "ma alcuni profili restano da verificare su fonti esterne / normativa aggiornata."
            )

        clear_case(chat_id)
        return result

    # Se esiste un caso tipico riconosciuto, mostra un orientamento e poi chiede il primo dato mancante
    if case_key and questions:
        q = questions[0]
        state["mode"] = "clarification"
        state["pending_question"] = q
        return (
            f"{format_case_hint(case_key)}\n\n"
            "Per chiudere correttamente il caso mi serve questo chiarimento:\n\n"
            f"{q['text']}"
        )

    # Se ha già un’ipotesi ma mancano pochi dati
    if main_code and len(questions) <= 3:
        q = questions[0]
        state["mode"] = "clarification"
        state["pending_question"] = q
        return (
            "Esito preliminare probabile individuato con il database interno.\n"
            "Per chiudere il caso mi serve ancora questo dato:\n\n"
            f"{q['text']}"
        )

    # Se non ha dati sufficienti, lo dice e inizia a chiedere ciò che manca
    if questions:
        q = questions[0]
        state["mode"] = "clarification"
        state["pending_question"] = q
        return (
            "Il bot non ha ancora dati sufficienti per una qualificazione affidabile.\n"
            "Ti faccio una domanda mirata:\n\n"
            f"{q['text']}"
        )

    # Se non riesce a chiudere neppure così
    result = (
        "Non è stato possibile chiudere automaticamente il caso con il solo database interno del bot.\n\n"
        "VERIFICHE NECESSARIE\n" +
        "\n".join([f"- {n}" for n in notes])
    )

    if need_external_source_notice(state["answers"]):
        result += (
            "\n\nAVVISO OPERATORE\n"
            "Per completare il caso potrebbe essere necessario verificare fonti esterne o aggiornamenti normativi "
            "non presenti nel database interno."
        )

    clear_case(chat_id)
    return result

def process_clarification(chat_id, text):
    state = user_states[chat_id]
    q = state.get("pending_question")

    if not q:
        clear_case(chat_id)
        return "Procedura annullata. Usa /caso per ricominciare."

    value = parse_answer_for_key(q["key"], text)
    if value is None:
        return f"Risposta non valida.\n\n{q['text']}"

    state["answers"][q["key"]] = value

    main_code, concurrent, notes = decide_violation(state["answers"])
    questions = missing_questions(state["answers"])

    questions = [item for item in questions if item["key"] != q["key"]]

    if main_code and len(questions) == 0:
        result = format_multiple(main_code, concurrent, notes)

        if need_external_source_notice(state["answers"]):
            result += (
                "\n\nAVVISO OPERATORE\n"
                "Il caso è stato chiuso con il database interno del bot, "
                "ma alcuni aspetti vanno comunque verificati su normativa vigente / fonti esterne."
            )

        clear_case(chat_id)
        return result

    if questions:
        next_q = questions[0]
        state["pending_question"] = next_q
        return f"Mi serve ancora questo chiarimento:\n\n{next_q['text']}"

    if main_code:
        result = format_multiple(main_code, concurrent, notes)
        clear_case(chat_id)
        return result

    clear_case(chat_id)
    return (
        "Non è stato possibile individuare automaticamente una voce sanzionatoria definitiva.\n\n"
        "VERIFICHE NECESSARIE\n" +
        "\n".join([f"- {n}" for n in notes]) +
        "\n\nAVVISO OPERATORE\n"
        "Il database interno non basta da solo a chiudere il caso."
    )

# =========================
# FLASK
# =========================

@app.route("/")
def home():
    return "NCC Sanzioni Bot attivo", 200

# =========================
# COMANDI ADMIN
# =========================

@bot.message_handler(commands=['approva'])
def approve_command(message):
    if not is_admin(message.from_user.id):
        return
    parts = message.text.strip().split()
    if len(parts) != 2 or not parts[1].isdigit():
        bot.reply_to(message, "Uso corretto: /approva ID")
        return
    user_id = int(parts[1])
    approve_user(user_id)
    bot.reply_to(message, f"Utente {user_id} autorizzato.")
    try:
        bot.send_message(user_id, "Accesso autorizzato dall'amministratore.\n\nOra puoi usare il bot.\nScrivi /start")
    except Exception:
        pass

@bot.message_handler(commands=['rifiuta'])
def reject_command(message):
    if not is_admin(message.from_user.id):
        return
    parts = message.text.strip().split()
    if len(parts) != 2 or not parts[1].isdigit():
        bot.reply_to(message, "Uso corretto: /rifiuta ID")
        return
    user_id = int(parts[1])
    reject_user(user_id)
    bot.reply_to(message, f"Utente {user_id} rifiutato.")
    try:
        bot.send_message(user_id, "La tua richiesta di accesso al bot non è stata approvata.")
    except Exception:
        pass

@bot.message_handler(commands=['pendenti'])
def pending_command(message):
    if not is_admin(message.from_user.id):
        return
    if not access_data["pending_users"]:
        bot.reply_to(message, "Nessuna richiesta pendente.")
        return
    lines = ["Richieste pendenti:"]
    for uid, data in access_data["pending_users"].items():
        username = f"@{data['username']}" if data.get("username") else "-"
        lines.append(f"- ID {uid} | {data.get('first_name', '-')} | {username}")
    bot.reply_to(message, "\n".join(lines))

@bot.message_handler(commands=['autorizzati'])
def authorized_command(message):
    if not is_admin(message.from_user.id):
        return
    lines = ["Utenti autorizzati:"]
    for uid in sorted(access_data["authorized_users"]):
        suffix = " (admin)" if uid == ADMIN_ID else ""
        lines.append(f"- {uid}{suffix}")
    bot.reply_to(message, "\n".join(lines))

@bot.message_handler(commands=['revoca'])
def revoke_command(message):
    if not is_admin(message.from_user.id):
        return
    parts = message.text.strip().split()
    if len(parts) != 2 or not parts[1].isdigit():
        bot.reply_to(message, "Uso corretto: /revoca ID")
        return
    user_id = int(parts[1])
    ok = revoke_user(user_id)
    if not ok:
        bot.reply_to(message, "Non puoi revocare l'accesso all'admin.")
        return
    bot.reply_to(message, f"Accesso revocato all'utente {user_id}.")
    try:
        bot.send_message(user_id, "Il tuo accesso al bot è stato revocato.")
    except Exception:
        pass

# =========================
# COMANDI BOT
# =========================

@bot.message_handler(commands=['start'])
def start_command(message):
    uid = message.from_user.id
    send_welcome_media(message.chat.id)

    if not is_admin(uid) and not is_authorized(uid):
        if not is_pending(uid):
            add_pending(message.from_user)
            notify_admin_new_request(message.from_user)
        bot.reply_to(message, request_access_text())
        return

    bot.reply_to(message, authorized_start_text(uid))

@bot.message_handler(commands=['help'])
def help_command(message):
    if not ensure_authorized(message):
        return
    bot.reply_to(
        message,
        "Comandi disponibili:\n\n"
        "/caso = descrivi liberamente la situazione; il bot analizza il testo, usa il database interno e, se manca qualcosa, ti fa domande mirate.\n\n"
        "/checklist = elenco controlli operativi sul posto.\n\n"
        "/documenti = documenti ed elementi che il conducente / servizio NCC deve esibire o consentire di verificare.\n\n"
        "/norme = riferimenti normativi principali NCC.\n\n"
        "/art85 = leggi il richiamo operativo dell'art. 85 CdS\n"
        "/art116 = leggi il richiamo operativo dell'art. 116 CdS\n"
        "/art3l21 = leggi il richiamo operativo dell'art. 3 L. 21/1992\n"
        "/art11l21 = leggi il richiamo operativo dell'art. 11 L. 21/1992\n\n"
        "/reset = annulla il caso in corso."
    )

@bot.message_handler(commands=['norme'])
def norme_command(message):
    if not ensure_authorized(message):
        return
    bot.reply_to(message, format_norme_from_db())

@bot.message_handler(commands=['documenti'])
def documenti_command(message):
    if not ensure_authorized(message):
        return
    bot.reply_to(message, format_documenti_from_db())

@bot.message_handler(commands=['art85'])
def art85_command(message):
    if not ensure_authorized(message):
        return
    bot.reply_to(message, format_articolo("art85"))

@bot.message_handler(commands=['art116'])
def art116_command(message):
    if not ensure_authorized(message):
        return
    bot.reply_to(message, format_articolo("art116"))

@bot.message_handler(commands=['art3l21'])
def art3l21_command(message):
    if not ensure_authorized(message):
        return
    bot.reply_to(message, format_articolo("art3l21"))

@bot.message_handler(commands=['art11l21'])
def art11l21_command(message):
    if not ensure_authorized(message):
        return
    bot.reply_to(message, format_articolo("art11l21"))

@bot.message_handler(commands=['checklist'])
def checklist_command(message):
    if not ensure_authorized(message):
        return
    bot.reply_to(message, format_checklist_from_db())

@bot.message_handler(commands=['reset'])
def reset_command(message):
    if not ensure_authorized(message):
        return
    clear_case(message.chat.id)
    bot.reply_to(message, "Procedura annullata.")

@bot.message_handler(commands=['caso'])
def caso_command(message):
    if not ensure_authorized(message):
        return
    begin_case_flow(message.chat.id)
    bot.reply_to(
        message,
        "Descrivi liberamente la situazione in un solo messaggio.\n\n"
        "Esempio:\n"
        "veicolo privato prende due turisti al porto, li accompagna a Roma, pagamento concordato, conducente senza KB"
    )

# =========================
# MESSAGGI GENERICI
# =========================

@bot.message_handler(func=lambda m: True)
def all_messages(message):
    if not ensure_authorized(message):
        return

    chat_id = message.chat.id
    state = get_state(chat_id)

    if not state:
        bot.reply_to(message, "Usa /caso per descrivere il fatto oppure /checklist per i controlli operativi.")
        return

    mode = state.get("mode")

    if mode == "free_case":
        response = process_case_description(chat_id, message.text.strip())
        bot.reply_to(message, response)
        return

    if mode == "clarification":
        response = process_clarification(chat_id, message.text.strip())
        bot.reply_to(message, response)
        return

    bot.reply_to(message, "Usa /caso per descrivere il fatto oppure /reset per annullare la procedura.")

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
