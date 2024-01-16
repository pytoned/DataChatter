import streamlit as st
#import json
import streamlit.components.v1 as components
import pandas as pd
import pygwalker as pyg
from langchain_experimental.agents.agent_toolkits import create_pandas_dataframe_agent
from langchain_openai import ChatOpenAI
from langchain.agents.agent_types import AgentType


# def load_api_key(secrets_file="secrets.json"):
#     with open(secrets_file) as f:
#         secrets = json.load(f)
#     return secrets["OPENAI_API_KEY"]

#OPENAI_API_KEY = load_api_key()

def main():
    
    st.set_page_config(page_title="Visualize and chat with your Excel/CSV files 📈", page_icon=":bar_chart:", layout="wide")
    st.header("Visualize and chat with your Excel/CSV files 🔎 📈")

    user_file = st.file_uploader("Upload your Excel/CSV file ❣️", type=["csv", "xlsx"])
    
    df = None
    
    with st.sidebar:
        OPENAI_API_KEY = st.text_input("OpenAI API Key", type="password")
        "[Get an OpenAI API key](https://platform.openai.com/account/api-keys)"
    
    if user_file is not None:
        file_name = user_file.name
        
        def process_df():
            if file_name.endswith('.csv'):
                return pd.read_csv(user_file)
            elif file_name.endswith('.xlsx'):
                return pd.read_excel(user_file)
    
        df = process_df()

    if df is not None:        
        def generate_response(input_text):
            agent = create_pandas_dataframe_agent(
                llm=ChatOpenAI(temperature=0, model="gpt-4", api_key=OPENAI_API_KEY),
                df=df,
                verbose=True,
                agent_type=AgentType.OPENAI_FUNCTIONS
                )
            
            response = agent.invoke(input_text)
            if 'output' in response:
                st.info(response['output'], icon='🤖')
            else:
                st.error("No output received from the LLM.. 🤦")

        
        with st.form("my_form"):
            user_question = st.text_area("Enter question about your data:", "How many rows are there in total?")
            submitted = st.form_submit_button("Ask")
            if not OPENAI_API_KEY:
                st.info("Please enter your OpenAI API to ask questions about your data..")
            elif submitted:
                generate_response(user_question)

        # Generate the HTML using PyGWalker
        pyg_html = pyg.to_html(df=df, dark='media')
        
        # Embed the HTML into the streamlit app
        components.html(pyg_html, height=1000, scrolling=True)
    

if __name__ == "__main__":
    main()
