from sqlalchemy import create_engine, text, inspect
from backend.app.core.config import settings
import logging

logger = logging.getLogger(__name__)

class DatabaseService:
    def __init__(self):
        self.engine = create_engine(settings.SQL_SERVER_CONNECTION_STRING)
        self.is_mock = "sqlite" in settings.SQL_SERVER_CONNECTION_STRING

    def get_schema_summary(self) -> str:
        """
        Returns a summary of the database schema for the LLM.
        If using a mock DB/SQLite, valid tables will be created first if they don't exist.
        """
        if self.is_mock:
            self._ensure_mock_data()
        
        inspector = inspect(self.engine)
        schema_info = []
        
        for table_name in inspector.get_table_names():
            columns = inspector.get_columns(table_name)
            col_desc = ", ".join([f"{col['name']} ({col['type']})" for col in columns])
            schema_info.append(f"Table: {table_name}\nColumns: {col_desc}")
            
        return "\n\n".join(schema_info)

    def execute_query(self, query: str):
        """
        Executes a Read-Only SQL query.
        """
        # Basic safety check (should be enhanced)
        if not query.lower().strip().startswith("select"):
             raise ValueError("Only SELECT queries are allowed.")

        with self.engine.connect() as connection:
            result = connection.execute(text(query))
            keys = result.keys()
            return [dict(zip(keys, row)) for row in result.fetchall()]

    def _ensure_mock_data(self):
        """Creates mock tables for demonstration purposes."""
        with self.engine.connect() as conn:
            # Check if likely already populated
            if inspect(self.engine).has_table("Employees"):
                return

            conn.execute(text("CREATE TABLE Employees (Id INTEGER PRIMARY KEY, Name TEXT, Department TEXT, Salary INTEGER)"))
            conn.execute(text("INSERT INTO Employees (Id, Name, Department, Salary) VALUES (1, 'Alice', 'Sales', 50000)"))
            conn.execute(text("INSERT INTO Employees (Id, Name, Department, Salary) VALUES (2, 'Bob', 'Engineering', 80000)"))
            conn.execute(text("INSERT INTO Employees (Id, Name, Department, Salary) VALUES (3, 'Charlie', 'Sales', 55000)"))
            
            conn.execute(text("CREATE TABLE Sales (Id INTEGER PRIMARY KEY, Region TEXT, Amount INTEGER, EmployeeId INTEGER)"))
            conn.execute(text("INSERT INTO Sales (Id, Region, Amount, EmployeeId) VALUES (1, 'North', 12000, 1)"))
            conn.execute(text("INSERT INTO Sales (Id, Region, Amount, EmployeeId) VALUES (2, 'South', 15000, 3)"))
            conn.commit()
            logger.info("Mock data created.")

db_service = DatabaseService()
