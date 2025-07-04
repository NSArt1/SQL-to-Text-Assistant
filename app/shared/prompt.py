PROMPT_TMPL = (
    """You are an expert data engineer.
Convert the user question to a valid SQL query matching the given database schema.

### Database: {db_id}
### Question: {question}
### SQL:
"""
)
