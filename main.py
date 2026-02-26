import streamlit as st
import io
import contextlib
import re  # New import for cleaning text
from langchain_code import get_few_shots_db_chain

st.title("natural language TO SQL LLM")

# Function to remove ANSI color codes
def clean_ansi_codes(text):
    ansi_escape = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')
    return ansi_escape.sub('', text)

question = st.text_input("Question:")

if question:
    chain = get_few_shots_db_chain()
    
    f = io.StringIO()
    with contextlib.redirect_stdout(f):
        response = chain.run(question) 
    
    captured_output = f.getvalue()

    sql_query = ""
    sql_result = ""

    lines = captured_output.split("\n")
    for line in lines:
        clean_line = clean_ansi_codes(line.strip()) # Clean the codes here
        if "SQLQuery:" in clean_line:
            sql_query = clean_line.split("SQLQuery:")[-1].strip()
        if "SQLResult:" in clean_line:
            # This captures [(Decimal('26'),)]
            raw_result = clean_line.split("SQLResult:")[-1].strip()
            
            # Use regex to find only the digits
            numeric_match = re.search(r"\d+", raw_result)
            if numeric_match:
                sql_result = numeric_match.group()

    st.subheader("SQL Query")
    if sql_query:
        st.code(sql_query, language="sql")

    st.subheader("SQL Result")
    if sql_result:
        # Displaying just the clean number
        st.header(sql_result) 
    else:
        st.write(response)