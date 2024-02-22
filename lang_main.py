import re
import os
import joblib
import pandas as pd
import google.generativeai as genai
from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
from langchain.vectorstores import FAISS
from langchain.prompts import SemanticSimilarityExampleSelector
from langchain.schema import SystemMessage, HumanMessage, AIMessage
from sqlalchemy import create_engine
from utilities import data_dict, mysql_prompt, generic_prompts, few_shots
from dotenv import load_dotenv
load_dotenv()

database_name = 'apple_store'
data_table = 'apple_data'
discount_table = 'discounts'
mysql_conn_str = f"mysql+mysqlconnector://root:root@localhost/{database_name}"

history_df = pd.DataFrame(columns = ["HumanMessage", "AIMessage"])

def load_embeddings():
    vectorstore = joblib.load('data/vectorstore.joblib')
    return vectorstore

def get_chat_history(history_df):
    try:
        chat_history = {'HumanMessage': history_df['HumanMessage'].iloc[0],
         'AIMessage': history_df['AIMessage'].iloc[0]}
        history = f"""Based on the conversation below, answer the current question.
        Convsersation history : 
        Question : {chat_history["HumanMessage"]}
        AI Response : {chat_history["AIMessage"]}
        """
    except:
        history = ""
    return history

def save_chat_history(chat_history_dict, history_df):
    cur_his_df = pd.DataFrame(chat_history_dict)
    history_df = pd.concat([cur_his_df, history_df], axis=0, ignore_index=True)
    return history_df

def get_sql_result(sql_query):
    engine = create_engine(mysql_conn_str, echo=False)
    con= engine.connect()
    df_result = pd.read_sql(sql_query, con)
    con.close()
    return df_result

def clean_response_query(response):
    import re
    text = response.replace('`','').replace('sql', '').replace('\\n','').replace('SQLQuery:', '')
    text = re.sub(r'\s+', ' ', text)
    return text

def refresh_chat_history(history_df):
    if len(history_df)>5:
        history_df = history_df[:5]
    return history_df

def generate_llm_response(prompt, history_df):

    llm = ChatGoogleGenerativeAI(model = "gemini-pro", temperature=0.3)

    vectorstore = load_embeddings()
    exampleSelector = SemanticSimilarityExampleSelector(vectorstore = vectorstore, k=2)
    response, chat_history = "", dict()
    chat_history = get_chat_history(history_df)
    msg = [
        SystemMessage(content = mysql_prompt),
        HumanMessage(content = exampleSelector.select_examples({"Question": prompt})[0]['Question']),
        AIMessage(content = exampleSelector.select_examples({"SQLQuery": prompt})[0]['SQLQuery'])
        ]

    msg.append(SystemMessage(content = chat_history))
    msg.append(HumanMessage(content= prompt))

    response = llm.invoke(str(msg)).content

    clean_query = clean_response_query(response)

    res_data = get_sql_result(clean_query)

    chat_history_dict = {'HumanMessage': [prompt], 'AIMessage': [clean_query]}
    history_df = save_chat_history(chat_history_dict, history_df)

    history_df = refresh_chat_history(history_df)

    return response.replace('`','').replace('sql',''), res_data, history_df