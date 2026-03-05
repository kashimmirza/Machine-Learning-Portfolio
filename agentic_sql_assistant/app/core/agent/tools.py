from typing import Optional, Type
from langchain_core.tools import BaseTool
from pydantic import BaseModel, Field
from app.services.sql_server import sql_server_service

class SQLQueryInput(BaseModel):
    query: str = Field(description="The T-SQL query to execute. Must be a SELECT statement.")

class SQLQueryTool(BaseTool):
    name: str = "execute_sql_query"
    description: str = "Executes a T-SQL SELECT query against the database and returns the results. Use this to answer questions about business data."
    args_schema: Type[BaseModel] = SQLQueryInput

    def _run(self, query: str) -> str:
        """Use the tool."""
        return str(sql_server_service.execute_query(query))
    
    async def _arun(self, query: str) -> str:
        """Use the tool asynchronously."""
        # For now, we wrap the sync call since SQL Alchemy/PyODBC might block.
        # In a high-perf scenario, use run_in_executor.
        return self._run(query)

class SQLSchemaTool(BaseTool):
    name: str = "get_database_schema"
    description: str = "Returns the schema involving table names and column names of the database. Call this FIRST to understand what data is available."
    
    def _run(self) -> str:
        return sql_server_service.get_schema()
    
    async def _arun(self) -> str:
        return self._run()

tools = [SQLQueryTool(), SQLSchemaTool()]
