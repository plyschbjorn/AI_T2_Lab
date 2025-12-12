# 🤖 The T2 Lab – Terminator RAG Chatbot

En **Retrieval-Augmented Generation (RAG)**-chatbot som svarar på frågor om Data Engineering — med en konsekvent **Terminator T-800‑persona**.

Projektet är gjort som en kurslabb och fokuserar på att kombinera **faktabaserad retrieval** med **kontrollerad stil via prompt‑engineering**.

---

## 🧠 Vad gör applikationen?

- Läser in YouTube-transkript via .md-filer
- Skapar embeddings och lagrar dem i **LanceDB**
- Hämtar relevant kontext vid fråga (RAG)
- Genererar svar med **Gemini**
- Levererar svaren i **Terminator T‑800‑stil** via Streamlit

> *Affirmative. Knowledge delivery initiated.*

---

## 🏗️ Arkitektur

```
User
 ↓
Streamlit frontend
 ↓
Azure Function / FastAPI
 ↓
RAG-agent (PydanticAI)
 ↓
LanceDB (vector search)
 ↓
Gemini LLM
```

---

## 🚀 Kom igång

### Förutsättningar
- Python 3.10+
- `uv`
- Google Gemini API‑nyckel
- Azure Function API‑nyckel

### Miljövariabler (.env)
```
GOOGLE_API_KEY=...
FUNCTION_APP_API=...
```

### Installation
```bash
git clone https://github.com/plyschbjorn/AI_T2_Lab.git
cd AI_T2_Lab
uv sync
```

---

## 🧠 Ingestion

Bygger vektordatabasen från markdown‑filer i `data/`:

```bash
python ingestion.py
```

---

## 🧪 Köra lokalt

```bash
uvicorn api:app --reload
streamlit run frontend/app.py
```

Frontend körs på `http://localhost:8501`.

---

## ☁️ Azure Function

- FastAPI exponeras via `function_app.py`
- Frontend anropar Azure Function‑URL
- API‑nyckel används via `FUNCTION_APP_API`

---

## 📁 Projektstruktur

```
.
├── backend/        RAG‑logik, prompt & modeller
├── data/           Transkript (markdown)
├── frontend/       Streamlit‑UI + Terminator‑tema
├── api.py          FastAPI‑app
├── ingestion.py    Skapar LanceDB
└── function_app.py Azure Functions entrypoint
```

---

## 📝 Notering

- Terminator‑personan styr **endast stil**, inte fakta
- Allt innehåll är hämtat via RAG för att undvika hallucinationer
- Projektet är en lab för en kurs i AI

---

*Talk to the hand ✋ – I’ll be back.*