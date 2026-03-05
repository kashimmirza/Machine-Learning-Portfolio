from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
from backend.app.services.db_service import db_service
from backend.app.services.llm_service import llm_service
import logging

logger = logging.getLogger(__name__)

router = APIRouter()

class QueryRequest(BaseModel):
    question: str

class QueryResponse(BaseModel):
    question: str
    generated_sql: str
    results: List[Dict[str, Any]]
    error: Optional[str] = None

# Mock Security Dependency
def get_current_user(x_api_key: str = "default-user"):
    # In a real app, validate token/key here.
    return x_api_key

@router.post("/query", response_model=QueryResponse)
async def ask_question(request: QueryRequest, user: str = Depends(get_current_user)):
    """
    Process a natural language question, convert to SQL, and return results.
    """
    try:
        # 1. Get Schema Context
        schema_summary = db_service.get_schema_summary()
        
        # 2. Generate SQL
        generated_sql = llm_service.generate_sql(request.question, schema_summary)
        logger.info(f"Generated SQL: {generated_sql}")
        
        # 3. Execute SQL (Safety checks are inside db_service)
        results = db_service.execute_query(generated_sql)
        
        return QueryResponse(
            question=request.question,
            generated_sql=generated_sql,
            results=results
        )
        
    except ValueError as ve:
        # User/safety error (e.g. non-SELECT query)
        logger.warning(f"Query Safety Violation: {ve}")
        return QueryResponse(
            question=request.question,
            generated_sql="BLOCKED",
            results=[],
            error=str(ve)
        )
    except Exception as e:
        logger.error(f"Internal Error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/health")
def health_check():
    return {"status": "ok", "db_mock_mode": db_service.is_mock}
