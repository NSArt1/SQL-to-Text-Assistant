import os, logging
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import httpx, pandas as pd

from .db import run_query

logger = logging.getLogger("uvicorn.error")

class GenRequest(BaseModel):
    question: str
    db_id: str = "demo_db"

class SqlResponse(BaseModel):
    sql: str

class ExecRequest(BaseModel):
    sql: str

class ExecResponse(BaseModel):
    rows: list

VLLM_ENDPOINT = os.getenv("VLLM_ENDPOINT", "http://vllm:8000/v1/completions")
PROMPT_TMPL = (
    "You are an expert data engineer. Convert the user question to a valid,\n"
    "executable SQL query that matches the given database schema.\n"
    "### Database: {db_id}\n"
    "### Question: {question}\n"
    "### SQL:"
)

app = FastAPI(title="NL→SQL API", version="1.0")

@app.post("/generate_sql", response_model=SqlResponse)
async def generate_sql(req: GenRequest):
    payload = {
        "model": "codellama-7b-dpo",
        "prompt": PROMPT_TMPL.format(**req.dict()),
        "max_tokens": 256,
        "temperature": 0.0,
    }
    async with httpx.AsyncClient(timeout=120) as client:
        r = await client.post(VLLM_ENDPOINT, json=payload)
    if r.status_code != 200:
        logger.error(r.text)
        raise HTTPException(status_code=500, detail="LLM inference failed")
    sql_text = r.json()["choices"][0]["text"].strip()
    return {"sql": sql_text}

@app.post("/execute_sql", response_model=ExecResponse)
async def execute_sql(req: ExecRequest):
    try:
        df = run_query(req.sql)
    except Exception as e:
        logger.exception("SQL execution error")
        raise HTTPException(status_code=400, detail=str(e))
    # Convert DF rows to list of dicts
    return {"rows": df.to_dict(orient="records")}
