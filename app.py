import streamlit as st
import google.generativeai as genai
from dotenv import load_dotenv
import os

# Load API key from .env file
load_dotenv()
api_key = os.getenv("google_api_key")

if not api_key:
    st.error("API key not found. Please add your API key to a .env file.")
else:
    # Configure Google Generative AI
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-pro')

    # Setting web app page name and layout
    st.set_page_config(page_title='Text-To-SQL APP', layout='wide')

    # Setting column size
    col1, col2 = st.columns((0.12, 1.7))

    # Adding images and text
    col1.image('text.jpeg', use_column_width=True)
    col2.markdown("# :rainbow[SMARTSQL GENIE]")
    st.write("#### :blue[This is a SQL Query Generator Web App Using Google Gemini!]")

    # User input
    st.markdown("## Enter your prompt:")
    query_input = st.text_area("Prompt", height=150)

    # Buttons
    col3, col4 = st.columns((1, 0.5))
    with col3:
        submit = st.button("Generate SQL Query")
    with col4:
        clear = st.button("Clear")

    # Supportive information for generating content
    supportive_info1 = (
        "Based on the prompt text, create a SQL query, and make sure to exclude '' in the beginning and end."
    )
    supportive_info2 = (
        "Based on the SQL query code, create an example input dataframe before the SQL query code is applied "
        "and the output dataframe after the SQL query is applied."
    )
    supportive_info3 = (
        "Explain the SQL query in detail without any example output."
    )

    # Initialize variables for storing results
    sql_query = ""
    example_output = ""
    explanation = ""

    if submit:
        if not query_input.strip():
            st.warning("Please enter a prompt before submitting.")
        else:
            with st.spinner("Generating..."):
                try:
                    # Generate SQL Query
                    response = model.generate_content([supportive_info1, query_input])
                    sql_query = response.text

                    # Generate Example Output
                    response2 = model.generate_content([supportive_info2, sql_query])
                    example_output = response2.text

                    # Generate Explanation
                    response3 = model.generate_content([supportive_info3, sql_query])
                    explanation = response3.text

                except Exception as e:
                    st.error(f"An error occurred: {e}")

    # Display results
    if sql_query:
        st.markdown("## Results")
        st.write("### 1. The Generated SQL Query Code:")
        st.code(sql_query, language='sql')

        st.write("### 2. Example Input and Output DataFrames:")
        st.write(example_output)

        st.write("### 3. Explanation of the SQL Query Code Generated:")
        st.write(explanation)

        # Download button for SQL query
        st.download_button(
            label="Download SQL Query",
            data=sql_query,
            file_name="generated_query.sql",
            mime="text/plain"
        )

    if clear:
        st.experimental_rerun()  # Clear all inputs and outputs
