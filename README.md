# PL-SB1U

Multi-agent assistent for produktledere hos **SpareBank 1 Utvikling (SB1U)**.

## Oversikt

`pl-sb1u` er et multi-agent system bygget med [LangGraph](https://github.com/langchain-ai/langgraph) og OpenAI. Systemet gjør det enkelt for en produktleder å få hjelp med daglige oppgaver: backlog-håndtering, produktanalyse, interessentkommunikasjon og markedsundersøkelser – alt i én samlet chat-assistent.

### Agenter

| Agent | Ansvar |
|---|---|
| 🎯 **Orchestrator** | Analyserer brukerens forespørsel og ruter den til riktig spesialistagent |
| 🗒️ **Backlog-agent** | User stories, akseptansekriterier, MoSCoW-/WSJF-prioritering, sprintplanlegging |
| 📊 **Analytics-agent** | KPIer, OKRer, sprintmetrikker, velocity, NPS, ROI-beregning |
| 💬 **Kommunikasjons-agent** | Statusrapporter, release notes, møtereferater, roadmap-kommunikasjon |
| 🔍 **Research-agent** | Konkurrentanalyse, trendanalyse norsk fintech, SWOT, teknologivurderinger |

### Arkitektur

```
Bruker → Orchestrator → [Backlog | Analytics | Communication | Research] → Svar
```

LangGraph-grafen bruker en betinget kant fra Orchestrator til én av de fire spesialistagentene basert på innholdet i forespørselen.

## Oppsett

### Krav

- Python 3.11+
- OpenAI API-nøkkel

### Installasjon

```bash
# Klon og installer
pip install -e .

# Kopier og fyll ut miljøvariabler
cp .env.example .env
# Rediger .env og legg inn OPENAI_API_KEY
```

### Kjøring

**Interaktiv modus (REPL):**
```bash
pl-sb1u
```

**Enkelt spørsmål:**
```bash
pl-sb1u "Skriv en user story for innlogging med BankID"
pl-sb1u "Hva er velocity-trenden vår de siste 6 sprintene?"
pl-sb1u "Skriv release notes for mobilbank versjon 4.2"
pl-sb1u "Sammenlign SB1U mobilbank med DNB sin app"
```

### Eksempelspørsmål

```
# Backlog
"Skriv en user story for å sette opp AvtaleGiro"
"Prioriter disse backlog-itemene med WSJF: [liste]"
"Hva bør Definition of Done inneholde for en betalingsfunksjon?"

# Analytics
"Hjelp meg å sette opp OKRer for neste kvartal"
"Hvordan tolker jeg et burndown-diagram som flater ut?"
"Hvilke KPIer bør vi følge for mobilbank?"

# Kommunikasjon
"Skriv statusrapport for sprint 23 til produktstyret"
"Lag agenda for neste PI Planning"
"Oppsummer disse møtenotatene og identifiser action items"

# Research
"Gjør en SWOT-analyse av SB1U sin mobilbankapp"
"Hvilke open banking-trender påvirker oss i 2025?"
"Sammenlign Vipps Mobilepay med SB1U sin betalingsløsning"
```

## Utvikling

```bash
# Installer med dev-avhengigheter
pip install -e ".[dev]"

# Kjør tester
pytest

# Kjør spesifikke testfiler
pytest tests/test_orchestrator.py -v
```

## Konfigurasjon

Se `.env.example` for tilgjengelige innstillinger:

| Variabel | Standard | Beskrivelse |
|---|---|---|
| `OPENAI_API_KEY` | (påkrevd) | OpenAI API-nøkkel |
| `OPENAI_MODEL` | `gpt-4o` | Modellnavn |
| `TEMPERATURE` | `0.1` | Kreativitet (0 = deterministisk) |
| `LANGUAGE` | `no` | Svarspråk (`no` / `en`) |
| `TEAM_NAME` | `SpareBank 1 Utvikling` | Teamnavn brukt i kontekst |
