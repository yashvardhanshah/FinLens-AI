<div align="center">

# 📊 FinLens AI — Stock Research Made Simple

### Understand any stock in plain English, in under 30 seconds.

[![Live Demo](https://img.shields.io/badge/🚀%20Live%20Demo-Streamlit-FF4B4B?style=for-the-badge)](https://finlensai.streamlit.app)
[![GitHub](https://img.shields.io/badge/GitHub-yashvardhanshah-black?style=for-the-badge&logo=github)](https://github.com/yashvardhanshah/FinLens-AI)
[![Python](https://img.shields.io/badge/Python-3.10+-blue?style=for-the-badge&logo=python)](https://python.org)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.58-FF4B4B?style=for-the-badge&logo=streamlit)](https://streamlit.io)
[![LangChain](https://img.shields.io/badge/LangChain-1.3-green?style=for-the-badge)](https://langchain.com)
[![License](https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge)](LICENSE)

*Type a company name. Get a full research report. No finance degree required.*

### 🔗 [https://finlensai.streamlit.app](https://finlensai.streamlit.app)

![Model](https://img.shields.io/badge/LLaMA%203.3-70B-purple?style=flat-square) ![Tools](https://img.shields.io/badge/3%20Live%20Data%20Sources-Connected-success?style=flat-square) ![Speed](https://img.shields.io/badge/Report%20Ready-Under%2030s-blue?style=flat-square)

</div>

---

## 📋 Table of Contents

- [Overview](#-overview)
- [Features](#-features)
- [Tech Stack](#-tech-stack)
- [How It Works](#-how-it-works)
- [Project Structure](#-project-structure)
- [Local Setup](#-local-setup)
- [Deployment](#-deployment-on-streamlit-cloud)
- [Pages](#-app-pages)
- [Disclaimer](#-disclaimer)
- [License](#-license)
- [Author](#-author)

---

## 🧠 Overview

**FinLens AI** is an agentic financial research tool that turns a company name and ticker into a structured, plain-English research report — in under 30 seconds.

Most people can't afford a Bloomberg terminal or a team of analysts. FinLens bridges that gap: it pulls live market data, scans the latest news, and reads through any PDF you upload (annual reports, 10-K filings, earnings transcripts), then synthesises everything into one clear, well-structured brief using a 70B-parameter LLM running on Groq.

The agent decides autonomously which tools to call and in what order — no rigid pipeline, no hardcoded logic. Every number in the output comes from a real live data call, never from the model's memory.

---

## ✨ Features

| Feature | Description |
|---|---|
| 📈 **Live Market Data** | Real-time price, market cap, P/E ratio, 52-week range, volume, dividend yield |
| 📰 **News Search** | Latest headlines from the past 72 hours, summarised with overall sentiment |
| 📂 **PDF Document Analysis** | Upload an annual report or 10-K — FinLens reads it and extracts the key insights |
| ✍️ **Plain-English Reports** | Every brief is written to be understood by anyone, not just finance professionals |
| ⚡ **Under 30 Seconds** | Groq's hardware accelerates inference so results feel near-instant |
| ⬇️ **Downloadable Briefs** | Save every report as a timestamped `.txt` file |
| 🔒 **Private by Design** | Uploaded documents are never stored or sent anywhere beyond the inference call |

---

## 🛠 Tech Stack

### Frontend
- **Streamlit** — Multi-page web app, file uploads, session state
- **Custom CSS** — Dark theme with Syne + Inter typography, animations, responsive layout

### AI / Agent
- **LangChain Classic** — ReAct agent, `AgentExecutor`, tool orchestration
- **LangChain Core** — `Tool`, `PromptTemplate`
- **Groq API (LLaMA 3.3 70B)** — LLM inference for report synthesis

### Data Sources
- **yfinance** — Live stock price and fundamentals (no API key required)
- **Tavily Search API** — Web search for recent news and market commentary

### Document Intelligence (RAG)
- **LangChain Community** — `PyPDFLoader`, `FAISS` vectorstore
- **LangChain HuggingFace** — `HuggingFaceEmbeddings`
- **Sentence Transformers (MiniLM-L6-v2)** — Local document embeddings at 384 dimensions
- **FAISS (CPU)** — In-process vector similarity search, no external database

---

## ⚙️ How It Works

```
User Input (company name + ticker + optional PDF)
        ↓
    [Optional] PDF uploaded
        → PyPDFLoader extracts text
        → RecursiveCharacterTextSplitter chunks it
        → MiniLM-L6-v2 embeds chunks
        → FAISS indexes vectors in memory
        ↓
    ReAct Agent initialised (LLaMA 3.3 70B via Groq)
        ↓
    Agent autonomously calls tools:
        → get_stock_data(ticker)     ← yfinance live data
        → search_news(query)         ← Tavily web search
        → search_document(question)  ← FAISS vector search (if PDF uploaded)
        ↓
    LLM synthesises all observations
        ↓
    Structured Research Brief output
        → Company Overview
        → Live Market Data (line-by-line metrics)
        → Latest News & Sentiment
        → Key Insights from Document (if uploaded)
        → Key Risks
        → Outlook
```

---

## 📁 Project Structure

```
FinLens-AI/
│
├── app.py                  # Main Streamlit app — all 4 pages and UI
│
├── agent/
│   ├── agent.py            # ReAct agent setup, prompt template, tool wiring
│   └── tools.py            # Tool functions: stock data, news search, doc search
│
├── rag/
│   └── rag_pipeline.py     # PDF loading, chunking, embedding, FAISS vectorstore
│
├── requirements.txt        # All Python dependencies (verified, conflict-free)
├── .env                    # API keys — never committed to git
├── .gitignore              # Excludes .env, __pycache__, faiss_index/
└── README.md
```

---

## 🚀 Local Setup

### Prerequisites
- Python 3.10+
- A Groq API key (free at [console.groq.com](https://console.groq.com))
- A Tavily API key (free tier at [app.tavily.com](https://app.tavily.com))

### 1. Clone the repo

```bash
git clone https://github.com/yashvardhanshah/FinLens-AI.git
cd FinLens-AI
```

### 2. Create and activate a virtual environment

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Mac / Linux
python -m venv venv
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

> ⚠️ Note: `sentence-transformers` pulls in PyTorch, so this install is heavier than average (~1–2GB). Give it a minute.

### 4. Add your API keys

Create a `.env` file in the project root:

```env
GROQ_API_KEY=your_groq_api_key_here
TAVILY_API_KEY=your_tavily_api_key_here
```

### 5. Run the app

```bash
streamlit run app.py
```

Open [http://localhost:8501](http://localhost:8501) in your browser.

---

## ☁️ Deployment on Streamlit Cloud

1. Fork this repo to your GitHub account
2. Go to [share.streamlit.io](https://share.streamlit.io) and sign in with GitHub
3. Click **New app** — select your fork, branch `main`, main file `app.py`
4. Click **Advanced settings → Secrets** and add:

```toml
GROQ_API_KEY = "your_groq_key_here"
TAVILY_API_KEY = "your_tavily_key_here"
```

5. Click **Deploy**

Build takes 3–5 minutes (PyTorch install). Once live, you'll get a permanent shareable URL.

---

## 📄 App Pages

| Page | Description |
|---|---|
| 🏠 **Home** | Landing page — what FinLens does, how it works, why to trust it |
| 🔍 **Get a Report** | The main tool — enter a company, upload a PDF, generate your report |
| ❓ **How It Works** | Step-by-step guide for non-technical users, FAQ |
| ℹ️ **About** | Mission, design principles, what the app stands for |

---

## ⚠️ Disclaimer

> **FinLens AI is an informational tool only and does not constitute financial advice.**
>
> Reports generated by this application are produced by an AI system using publicly available data. They are intended to help users understand and research companies — not to recommend buying or selling any security.
>
> Always consult a qualified financial advisor before making any investment decisions. Past performance and AI-generated analysis are not reliable indicators of future results.

---

## 📄 License

This project is licensed under the **MIT License** — free to use, fork, and build on.

```
MIT License — Copyright (c) 2026 Yashvardhan Shah
```

---

## 👤 Author

**Yashvardhan Shah**

[![GitHub](https://img.shields.io/badge/GitHub-yashvardhanshah-black?style=flat-square&logo=github)](https://github.com/yashvardhanshah)
[![Live App](https://img.shields.io/badge/Live%20App-finlensai.streamlit.app-FF4B4B?style=flat-square)](https://finlensai.streamlit.app)

---

<div align="center">

**⭐ Star this repo if you found it useful!**

*Built with Streamlit · Groq · LangChain · Tavily · FAISS*

</div>