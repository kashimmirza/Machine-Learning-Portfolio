<!-- @format -->

# NotebookLM Clone — Full Stack AI Research Assistant

A production-grade clone of Google NotebookLM built with:

- **Frontend**: React 18 + Vite + Zustand + TailwindCSS
- **Backend**: FastAPI + Python 3.11
- **Database**: PostgreSQL (metadata) + Pinecone (vector search)
- **AI**: OpenAI GPT-4o / Anthropic Claude API
- **Storage**: AWS S3 / Local filesystem
- **Auth**: JWT + OAuth2
- **Agentic**: LangChain + LangGraph multi-agent orchestration
- **Audio**: ElevenLabs TTS for Podcast generation

## Features

- 📚 Multi-source ingestion (PDF, URL, YouTube, Google Docs, text)
- 🧠 RAG (Retrieval-Augmented Generation) Q&A
- 🎙️ AI Podcast/Audio Overview generation
- 💬 Notebook-scoped chat with citations
- 📝 AI-generated study guides, briefing docs, FAQs, timelines
- 🔍 Semantic search across notebooks
- 👥 Sharing & collaboration
- 🗂️ Notebook organization

## Quick Start

```bash
# Clone and setup
cp .env.example .env
# Fill in your API keys

# Backend
cd backend
pip install -r requirements.txt
alembic upgrade head
uvicorn main:app --reload

# Frontend
cd frontend
npm install
npm run dev
```

## Architecture

```
┌─────────────────────────────────────────────────────┐
│                   React Frontend                     │
│  (Notebook UI, Chat, Source Manager, Audio Player)  │
└───────────────────────┬─────────────────────────────┘
                        │ REST + WebSocket
┌───────────────────────▼─────────────────────────────┐
│                  FastAPI Backend                     │
│   ┌──────────┐  ┌──────────┐  ┌──────────────────┐  │
│   │  Router  │  │  Agent   │  │  RAG Pipeline    │  │
│   │  Layer   │  │ Orchestr.│  │  (LangChain)     │  │
│   └──────────┘  └──────────┘  └──────────────────┘  │
└──────┬──────────────┬───────────────┬────────────────┘
       │              │               │
┌──────▼──┐    ┌──────▼──┐    ┌──────▼──┐
│PostgreSQL│    │Pinecone │    │  S3 /   │
│(metadata)│    │(vectors)│    │ Storage │
└──────────┘    └─────────┘    └─────────┘
```
