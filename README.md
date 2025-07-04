# NL2SQL Generator

This repository delivers a **ready‑to‑run** system that converts natural‑language
questions to SQL and executes them on a Postgres database.  
The model is a DPO‑fine‑tuned **CodeLlama‑7B** served with **vLLM**, wrapped by a
**FastAPI** backend and a **Streamlit** front‑end.

## 1 Quick Start

```bash
git clone https://github.com/your-org/nl2sql-generator && cd nl2sql-generator
docker compose -f docker/docker-compose.yml up -d --build
# Wait until http://localhost:8501 is up
open http://localhost:8501
```

## 2 Services

| Service   | Port | Description                                |
| --------- | ---- | ------------------------------------------ |
| Streamlit | 8501 | Web UI                                     |
| FastAPI   | 8000 | `/generate_sql` + `/execute_sql` endpoints |
| vLLM      | 8001 | OpenAI‑compatible LLM server               |
| Postgres  | 5432 | Demo DB (customers / sales)                |

## 3 Training

Minimal DPO script is in **model/train_dpo.py** and works on `data/nl_sql_pairs.jsonl`.
Run:

```bash
python model/train_dpo.py \
    --model_name_or_path codellama/CodeLlama-7b-hf \
    --dataset_path data/nl_sql_pairs.jsonl \
    --output_dir model/CodeLlama-7b-dpo
```
