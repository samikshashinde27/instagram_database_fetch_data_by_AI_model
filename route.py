from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Any
import traceback

from ollama_model import generate_sql, execute_sql

app = FastAPI(
    title="Advanced MySQL NLQ API",
    description="Generate and execute MySQL SELECT queries using natural language",
    version="1.0.0"
)


class NLQRequest(BaseModel):
    user_input: str

class SQLResponse(BaseModel):
    sql_query: str
    rows: List[List[Any]]  


@app.post("/generate_sql", response_model=SQLResponse)
def generate_and_execute(request: NLQRequest):
    try:
        try:
            sql_query = generate_sql(request.user_input)
            rows = execute_sql(sql_query)
            rows_list = [list(row) for row in rows]
        except Exception as db_error:
            return SQLResponse(
                sql_query="",
                rows=[]
            )

        return SQLResponse(sql_query=sql_query, rows=rows_list)

    except Exception as e:
        traceback_str = traceback.format_exc()
        raise HTTPException(status_code=400, detail=f"{str(e)}\n{traceback_str}")

@app.get("/")
def root():
    return {"message": "Advanced MySQL NLQ API is running!"}


