# FinLens-AI — Financial Research Intelligence Agent
<div align="center">

# FinLens AI
### Financial Research Intelligence Agent

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10%2B-blue?style=for-the-badge&logo=python&logoColor=white" />
  <img src="https://img.shields.io/badge/LangChain-Agentic-purple?style=for-the-badge" />
  <img src="https://img.shields.io/badge/RAG-FAISS-orange?style=for-the-badge" />
  <img src="https://img.shields.io/badge/Streamlit-Deployed-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white" />
  <img src="https://img.shields.io/badge/License-MIT-green?style=for-the-badge" />
</p>

<p align="center">
  <b>An agentic AI system that autonomously retrieves live financial data, searches market news, and performs RAG over annual reports to generate structured analyst-style research briefs.</b>
</p>

---

</div>

## 📌 Overview

FinLens AI is a production-oriented financial research agent that combines **Large Language Models**, **Retrieval-Augmented Generation (RAG)**, and **Agentic tool-calling** to automate equity research workflows. Enter a company name or ticker — FinLens autonomously gathers live data, retrieves relevant document context, and synthesizes a structured analyst brief in seconds.

> Built to demonstrate the full modern AI stack: LLM reasoning · RAG over financial documents · Agentic multi-step tool use · Real-time data integration.

---

## ⚡ Features

- **Live Financial Data** — Fetches real-time price, fundamentals, and key metrics via yfinance
- **Market News Search** — Agentic web search for latest news and analyst sentiment
- **Document RAG** — Upload any annual report or 10-K PDF; FAISS vector store enables semantic retrieval
- **LLM Synthesis** — Groq-powered LLM generates structured research briefs: Summary · Financials · Key Risks · Sentiment · Outlook
- **Agentic Pipeline** — LangChain agent autonomously decides which tools to call and in what order
- **Clean UI** — Streamlit frontend with report-style output

---

## 🏗️ Architecture

```
User Input (Ticker / Company Name)
         ↓
   LangChain Agent
    ↙     ↓      ↘
Live Data  Web Search  Document RAG
(yfinance) (Tavily)    (FAISS + PDF)
         ↓
   LLM Synthesis (Groq)
         ↓
Structured Research Brief
─────────────────────────
Summary · Financials · Risks · Sentiment · Outlook
```

---

## 🛠️ Tech Stack

| Layer | Technology |
|-------|-----------|
| LLM | Groq (LLaMA 3) |
| Agent Framework | LangChain |
| Vector Store | FAISS |
| Embeddings | HuggingFace |
| Financial Data | yfinance |
| Web Search | Tavily API |
| Frontend | Streamlit |
| Language | Python 3.10+ |

---

## ⚙️ Setup

```bash
# Clone the repository
git clone https://github.com/yashvardhanshah/FinLens-AI.git
cd FinLens-AI

# Install dependencies
pip install -r requirements.txt

# Add API keys to .env
GROQ_API_KEY=your_key
TAVILY_API_KEY=your_key

# Run
streamlit run app.py
```

---

## 📄 License

MIT License · Copyright (c) 2026 Yash Vardhan Shah

---

<div align="center">

**Built by [Yash Vardhan Shah](https://github.com/yashvardhanshah)**

⭐ Star this repo if you found it useful

</div>