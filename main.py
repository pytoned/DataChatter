
import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import pygwalker as pyg
from langchain_experimental.agents.agent_toolkits import create_pandas_dataframe_agent
#from langchain_openai import OpenAI
from langchain_openai import ChatOpenAI
from langchain.agents.agent_types import AgentType
#from dotenv import load_dotenv
#from langchain.agents import load_tools
#import plotly.express as px


def main():
    
    #load_dotenv()
        
    st.set_page_config(page_title="Visualize and chat with your Excel/CSV files 📈", page_icon=":bar_chart:", layout="wide")
    st.header("Visualize and chat with your Excel/CSV files 🔎 📈")

    with st.sidebar:
        OPENAI_API_KEY = st.text_input("OpenAI API Key", type="password")
        "[Get an OpenAI API key](https://platform.openai.com/account/api-keys)"


    user_file = st.file_uploader("Upload your Excel/CSV file ❣️", type=["csv", "xlsx"])
    
    df = None
    
    if user_file is not None:
        file_name = user_file.name
        
        def process_df():
            if file_name.endswith('.csv'):
                return pd.read_csv(user_file)
            elif file_name.endswith('.xlsx'):
                return pd.read_excel(user_file)
    
        df = process_df()

    if df is not None:
        
        #llm = OpenAI(temperature=0, max_tokens=1000, OPENAI_API_KEY=OPENAI_API_KEY)
        # agent = create_pandas_dataframe_agent(
        #     ChatOpenAI(temperature=0, model="gpt-4"),
        #     df,
        #     verbose=True,
        #     agent_type=AgentType.OPENAI_FUNCTIONS,
        #     )
        
        def generate_response(input_text):
            #llm = OpenAI(temperature=0, max_tokens=1000, OPENAI_API_KEY=OPENAI_API_KEY)
            agent = create_pandas_dataframe_agent(
                llm=ChatOpenAI(temperature=0, model="gpt-4"),
                df=df,
                verbose=True,
                agent_type=AgentType.OPENAI_FUNCTIONS
                )
            st.info(agent.invoke(input_text))
        
        with st.form("my_form"):
            user_question = st.text_area("Enter question:", "Ask a question about your Excel/CSV file?")
            submitted = st.form_submit_button("Submit")
            if not OPENAI_API_KEY:
                st.info("Please add your OpenAI API key to continue.")
            elif submitted:
                generate_response(user_question)
        
        #user_question = st.text_input("Ask a question about your CSV file")
    
        # if user_question:
        #     response = agent.invoke(user_question)
        #     st.write(response)
        
        # Generate the HTML using PyGWalker
        pyg_html = pyg.walk(df, return_html=True)
        
        # Embed the HTML into the streamlit app
        components.html(pyg_html, height=1000, scrolling=True)
    


if __name__ == "__main__":
    main()
