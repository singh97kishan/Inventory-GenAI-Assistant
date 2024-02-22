from lang_main import generate_llm_response
import streamlit as st
import pandas as pd
from sqlalchemy import create_engine
from utilities import generic_prompts

st.set_page_config(page_title = 'Apple GenAI Assist.')

st.title("Inventory GenAI Assistant :robot_face:")

history_df = pd.DataFrame(columns = ["HumanMessage", "AIMessage"])

chat_tokeep= []

def clear_chat_history():
    """
    To append the chat messages in streamlit session state to a variable and clear the chat window
    """
    for message in st.session_state.messages:
        chat = dict()
        chat[message['role']] = message['content']
        chat_tokeep.append(chat)
        #st.write(chat)
    st.session_state.messages = [{"role": "assistant", "content": "How may I assist you today?"}]
    global history_df
    history_df = pd.DataFrame(columns = ["HumanMessage", "AIMessage"])

schema = """TABLE NAME: apple_data \n product_id - int\n product_category - nvarchar \n product_name - nvarchar \n price - double \n stock_quantity - int\n
            TABLE_NAME: discounts \n product_id - int \n discount_perc - double
            """
schema_lis = schema.split("\n")

with st.sidebar:
    expander = st.expander("Chat History")
    expander_content = expander.empty()
    expander_content.write("No Chat history found")
    st.markdown(
    """
    *For more information, visit this [Github Repo](https://github.com/singh97kishan/Apple-SCM-LLM).*
    """
    )
    schema_expander = st.expander("Schema")
    for i in schema_lis:
        schema_expander.write(i)
    if st.button('Clear Chat Window'):
       clear_chat_history()
       expander.write(chat_tokeep)
       

# ----------------------------------------------------------------------------------------------------------#

if "messages" not in st.session_state.keys():
    st.session_state.messages = [{"role": "assistant", "content": "How may I assist you today?"}]

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        if isinstance(message["content"], pd.DataFrame):
            with st.expander("Generated SQL Query"):
                st.code(message["sqlquery"], language='sql')
            st.dataframe(message["content"])
        else:
            st.write(message["content"])

def get_response(prompt, history_df):
    """
    Function to get the LLM response from generate_llm_reponse function from lang_main.py file
    """
    try:
        if prompt in generic_prompts:
            full_response = "Hi, how can I help you today?"
            clean_query = ""
        else:
            clean_query, full_response, history_df = generate_llm_response(prompt, history_df)
    except:
        clean_query = ""
        full_response = "Couldn't process the request, please ask relevant questions only"
    return clean_query, full_response, history_df



if prompt := st.chat_input("Ask your questions here"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

if st.session_state.messages[-1]["role"] != "assistant":
    with st.chat_message("assistant"):
        with st.spinner("Please allow me a moment to check.."):
            sqlquery, full_response, history_df = get_response(prompt, history_df)
            if isinstance(full_response, pd.DataFrame):
                final_response = pd.DataFrame(full_response)
                with st.expander("Generated SQL Query"):
                    st.code(sqlquery, language='sql')
                st.dataframe(final_response)
            else:
                final_response = full_response
                st.markdown(final_response)

    message = {"role": "assistant", "content": final_response, "sqlquery": sqlquery}
    st.session_state.messages.append(message)

