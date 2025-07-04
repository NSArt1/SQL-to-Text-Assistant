import os, psycopg2, pandas as pd

def _conn():
    return psycopg2.connect(
        host=os.getenv("DB_HOST", "db"),
        port=os.getenv("DB_PORT", "5432"),
        dbname=os.getenv("DB_NAME", "demo_db"),
        user=os.getenv("DB_USER", "demo"),
        password=os.getenv("DB_PASSWORD", "demo"),
    )

def run_query(sql: str) -> pd.DataFrame:
    with _conn() as conn:
        return pd.read_sql_query(sql, conn)
