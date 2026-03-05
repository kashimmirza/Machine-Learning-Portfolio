# Enterprise AI Chatbot

A secure, enterprise-grade AI chatbot prototype capable of answering natural language questions by querying an MS SQL database using Azure OpenAI.

## Features
- **Text-to-SQL Conversion**: Uses Azure OpenAI (GPT-4) to translate natural language into SQL.
- **Database Agnostic (Sort of)**: Designed for MS SQL, but currently runs in **Mock Mode** using SQLite if no connection string is provided.
- **Safety**: Only allows `SELECT` queries to be executed.
- **API First**: Built with FastAPI for easy integration with frontend apps (React, Teams Bot, etc.).

## Architecture

![Architecture](https://mermaid.ink/img/pako:eNplkMFOwzAMhl_F8gmQOnBocNq4IQGJE0hwe3GapY01aRzHlbF3Z2lXQOzF_v3_F9uP5FoZ5Cg-G2u_MAb2eS-dwo9G2-fH8_1TfHq8jXcn_3j0j4_390_x4yLevdyHq3D1L76K10_hOnwOV7FfxTLePobLcA3vF3G4Cpfhc_gUPi2P4TLGL_8aLmP8fB0uY_wYf9x_hsvYP_89XIb34Spcx-swvscy3N58_gIAAP__j7l2cQ)

(Architecture diagram placeholder)

- **Main App**: `backend.app.main:app`
- **Services**:
  - `llm_service`: Handles Azure OpenAI communication.
  - `db_service`: Handles Database connections and schema reflection.

## Setup & Running

1. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Configure Environment**:
   Rename or create `.env` file.
   - For **Mock Mode** (No real Azure/SQL needed), just run it! The defaults handle everything.
   - For **Real Mode**:
     ```env
     AZURE_OPENAI_API_KEY=your_real_key
     AZURE_OPENAI_ENDPOINT=https://your-resource.openai.azure.com/
     SQL_SERVER_CONNECTION_STRING=mssql+pyodbc://user:password@server/db?driver=ODBC+Driver+17+for+SQL+Server
     ```

3. **Run the Server**:
   ```bash
   uvicorn backend.app.main:app --reload
   ```

4. **Test the API**:
   Open [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
   
   **Try these questions (Mock Data)**:
   - "Identify the total sales."
   - "Show me all employees in the Sales department."
   - "Who has the highest salary?"

## Structure
```
backend/
  app/
    api/       # Routes
    core/      # Config & Settings
    services/  # Business Logic (DB, LLM)
    main.py    # Entry point
```
