from typing import List, Dict, Any, Union
from sqlalchemy import create_engine, text
from app.core.config import settings

class SQLServerService:
    def __init__(self):
        # Construct connection string for ODBC
        # Driver={ODBC Driver 17 for SQL Server};Server=myServerAddress;Database=myDataBase;Uid=myUsername;Pwd=myPassword;
        # SQLAlchemy format: mssql+pyodbc://user:password@dsn_name?driver=ODBC+Driver+17+for+SQL+Server
        
        # NOTE: For on-prem SQL Server, ensure the docker container or host has network access.
        connection_url = (
            f"mssql+pyodbc://{settings.SQL_SERVER_USER}:{settings.SQL_SERVER_PASSWORD}@"
            f"{settings.SQL_SERVER_HOST}/{settings.SQL_SERVER_DB}?"
            f"driver={settings.SQL_SERVER_DRIVER.replace(' ', '+')}&TrustServerCertificate=yes"
        )
        
        self.engine = create_engine(connection_url, pool_pre_ping=True)

    def execute_query(self, query: str) -> Union[List[Dict[str, Any]], str]:
        """
        Executes a read-only SQL query and returns the results as a list of dictionaries.
        Basic safety check: Ensure query starts with SELECT.
        """
        if not query.strip().upper().startswith("SELECT"):
            return "Safety Alert: Only SELECT queries are allowed."

        try:
            with self.engine.connect() as connection:
                result = connection.execute(text(query))
                keys = result.keys()
                return [dict(zip(keys, row)) for row in result.fetchall()]
        except Exception as e:
            return f"Error executing query: {str(e)}"
    
    def get_schema(self) -> str:
        """
        Retrieves table definitions to help the LLM understand the DB structure.
        """
        inspector_query = """
        SELECT TABLE_NAME, COLUMN_NAME, DATA_TYPE 
        FROM INFORMATION_SCHEMA.COLUMNS
        """
        try:
            # Reusing the execute method to fetch metadata
            columns = self.execute_query(inspector_query)
            if isinstance(columns, str): # Error happened
                return columns
                
            # Organize by table
            schema = {}
            for col in columns:
                table = col['TABLE_NAME']
                if table not in schema:
                    schema[table] = []
                schema[table].append(f"{col['COLUMN_NAME']} ({col['DATA_TYPE']})")
            
            # Format as string
            schema_str = ""
            for table, cols in schema.items():
                schema_str += f"Table: {table}\nColumns: {', '.join(cols)}\n\n"
                
            return schema_str
        except Exception as e:
            return f"Error fetching schema: {str(e)}"

sql_server_service = SQLServerService()
