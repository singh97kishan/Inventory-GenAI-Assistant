from lang_main import generate_llm_response
import streamlit as st
import pandas as pd
from sqlalchemy import create_engine
from utilities import generic_prompts

history_df = pd.DataFrame(columns = ["HumanMessage", "AIMessage"])

def clear_chat_history():
    st.session_state.messages = [{"role": "assistant", "content": "How may I assist you today?"}]
    global history_df
    history_df = pd.DataFrame(columns = ["HumanMessage", "AIMessage"])

st.set_page_config(page_title = 'Apple GenAI Assist.')

st.title("Inventory GenAI Assistant :robot_face:")

if "messages" not in st.session_state.keys():
    st.session_state.messages = [{"role": "assistant", "content": "How may I assist you today?"}]

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        if isinstance(message["content"], pd.DataFrame):
            st.dataframe(message["content"])
        else:
            st.write(message["content"])

def get_response(prompt, history_df):
    if prompt in generic_prompts:
        #full_response = "Hi, how can I help you today?"
        full_response = "Han bhai.. kese yad kia?"
    else:
        try:
            full_response, history_df = generate_llm_response(prompt, history_df)
        except:
            #full_response = "I couldn't complete your request, please ask relevant question."
            full_response = "Mereko nhi malum re baba, kuch aur puch."
    return full_response, history_df



if prompt := st.chat_input("Ask your questions here"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

if st.session_state.messages[-1]["role"] != "assistant":
    with st.chat_message("assistant"):
        with st.spinner("Ruk thoda, dhund ke ata hu.."):
        #with st.spinner("Allow me a moment..."):
            full_response, history_df = get_response(prompt, history_df)
            # placeholder = st.empty()
            if isinstance(full_response, pd.DataFrame):
                final_response = pd.DataFrame(full_response)
                st.dataframe(final_response)
            else:
                final_response = full_response
                st.markdown(final_response)

    message = {"role": "assistant", "content": final_response}
    st.session_state.messages.append(message)

st.button('Clear Chat History', on_click=clear_chat_history)
st.markdown(
    """
    *For more information, visit this [Github Repo](https://github.com/singh97kishan/Apple-SCM-LLM).*
    """
)
