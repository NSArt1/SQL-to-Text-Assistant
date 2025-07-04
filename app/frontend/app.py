import streamlit as st, requests, pandas as pd

st.set_page_config(page_title=" NL→SQL Generator")
API_URL = st.secrets.get("api_url", "http://backend:8000")

st.title(" NL → SQL Generator")

if "history" not in st.session_state:
    st.session_state.history = []

col1, col2 = st.columns([2, 1])
with col1:
    question = st.text_input("Ask a question…", placeholder="Total sales by month in 2024")
with col2:
    db_id = st.text_input("DB", value="demo_db")

if st.button("Generate SQL") and question:
    with st.spinner("LLM generating…"):
        res = requests.post(f"{API_URL}/generate_sql", json={"question": question, "db_id": db_id}, timeout=120)
    sql = res.json().get("sql", "-- error --")
    st.code(sql, language="sql")
    st.session_state.history.append((question, sql))

if st.session_state.get("history"):
    st.markdown("### History")
    for q, s in st.session_state.history[::-1]:
        st.markdown(f"**Q:** {q}")
        st.code(s, language="sql")

st.divider()
st.markdown("### Run SQL")
manual_sql = st.text_area("SQL to run", height=100)
if st.button("Execute"):
    with st.spinner("Running…"):
        res = requests.post(f"{API_URL}/execute_sql", json={"sql": manual_sql}, timeout=120)
    rows = res.json().get("rows", [])
    if rows:
        df = pd.DataFrame(rows)
        st.dataframe(df)
    else:
        st.info("No rows returned.")
