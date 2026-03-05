# Agentic Medical System - Backend

This backend is built with the "7 Layers of a Production-Grade Agentic AI System" architecture.

## Setup

1. **Environment Variables**
   Copy `.env.example` to `.env` and fill in the required values:
   ```bash
   cp .env.example .env
   ```
   *Note: You need an OpenAI API Key.*

2. **Run with Docker**
   The easiest way to run the entire stack (App, DB, Prometheus, Grafana) is via Docker Compose:
   ```bash
   docker-compose up --build
   ```

3. **Access Services**
   - **API**: [http://localhost:8000](http://localhost:8000)
   - **Docs (Swagger)**: [http://localhost:8000/docs](http://localhost:8000/docs)
   - **Prometheus**: [http://localhost:9090](http://localhost:9090)
   - **Grafana**: [http://localhost:3000](http://localhost:3000) (Login: admin/admin)

## Architecture Layers

1. **Modular Codebase**: Organized in `app/`.
2. **Data Persistence**: Postgres + pgvector (`app/models/`, `app/services/database.py`).
3. **Security**: JWT Auth, Rate Limiting (`app/core/limiter.py`), Sanitization.
4. **Service Layer**: Resilient LLM Service (`app/services/llm.py`).
5. **Multi-Agentic**: LangGraph Agent (`app/core/langgraph/`).
6. **API Gateway**: FastAPI Routers (`app/api/`).
7. **Observability**: Prometheus + Grafana.
