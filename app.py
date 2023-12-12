from lang_main import get_few_shot_db_chain
import streamlit as st

st.set_page_config(page_title = 'Apple-SCM')
st.image('imgs/llm.png')

st.title("Apple - Inventory Query Portal")
st.markdown(
    "Welcome to the Apple Store Query Portal! Ask any questions about Inventory, and we'll provide answers."
)

question = st.text_input("Ask a question:")
if question:
    chain = get_few_shot_db_chain()
    answer = chain.run(question)

    st.header("Answer:")
    st.success(answer)

st.markdown(
    """
    *For more information, visit this [Github Repo](https://www.apple.com/).*
    """
)
