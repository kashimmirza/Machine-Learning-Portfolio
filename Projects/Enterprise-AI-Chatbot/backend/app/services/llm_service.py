from openai import AzureOpenAI
from backend.app.core.config import settings
import logging

logger = logging.getLogger(__name__)

class LLMService:
    def __init__(self):
        self.mock_mode = settings.AZURE_OPENAI_API_KEY == "mock-key"
        if not self.mock_mode:
            self.client = AzureOpenAI(
                api_key=settings.AZURE_OPENAI_API_KEY,
                api_version=settings.API_VERSION,
                azure_endpoint=settings.AZURE_OPENAI_ENDPOINT
            )
    
    def generate_sql(self, question: str, schema_info: str) -> str:
        """
        Generates a SQL query based on the user question and schema.
        """
        if self.mock_mode:
            logger.warning("Running in MOCK mode. Returning dummy SQL.")
            # Simple keyword matching for demo purposes when no API key is present
            if "total sales" in question.lower():
                return "SELECT SUM(Amount) FROM Sales"
            elif "employee" in question.lower():
                return "SELECT * FROM Employees"
            return "SELECT * FROM Employees -- Default Mock Query"

        system_prompt = f"""You are an expert MS SQL Server developer.
Your goal is to answer user questions by generating accurate SQL queries.
You must:
1. Use the provided schema to construct the query.
2. Return ONLY the SQL query. Do not include markdown formatting (like ```sql), explanations, or notes.
3. Ensure the query is Read-Only (SELECT only).
4. Use standard T-SQL syntax suitable for Azure SQL / MS SQL Server.

Schema:
{schema_info}
"""

        try:
            response = self.client.chat.completions.create(
                model=settings.AZURE_OPENAI_DEPLOYMENT_NAME,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": question}
                ],
                temperature=0,
                max_tokens=500
            )
            
            sql_query = response.choices[0].message.content.strip()
            
            # Basic cleanup if the model outputs markdown code blocks despite instructions
            sql_query = sql_query.replace("```sql", "").replace("```", "").strip()
            
            return sql_query
        except Exception as e:
            logger.error(f"Error calling Azure OpenAI: {e}")
            raise

llm_service = LLMService()
