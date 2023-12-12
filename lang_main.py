from langchain.llms import GooglePalm
from langchain.utilities import SQLDatabase
from langchain_experimental.sql import SQLDatabaseChain
from langchain.vectorstores import FAISS
from langchain.prompts import SemanticSimilarityExampleSelector
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.chains.sql_database.prompt import PROMPT_SUFFIX, _mysql_prompt
from langchain.prompts.prompt import PromptTemplate
from langchain.prompts import FewShotPromptTemplate

import os
from few_shots import few_shots
from dotenv import load_dotenv
load_dotenv()

def get_few_shot_db_chain():
    llm = GooglePalm(google_api_key= os.environ['GOOGLE_API_KEY'], temperature=0.1)

    db_user = "root"
    db_password = "root"
    db_host = "localhost"
    db_name = "apple_store"

    db = SQLDatabase.from_uri(f"mysql+pymysql://{db_user}:{db_password}@{db_host}/{db_name}",
                               sample_rows_in_table_info =3)
    
    embeddings = HuggingFaceEmbeddings(model_name='sentence-transformers/all-MiniLM-L6-v2')

    to_vectorize = [" ".join(example.values()) for example in few_shots]
    vectorstore = FAISS.from_texts(to_vectorize, embeddings, metadatas=few_shots)
    exampleSelector = SemanticSimilarityExampleSelector(vectorstore = vectorstore, k=2)
    examplePrompt = PromptTemplate( input_variables = ["Question", "SQLQuery", "SQLResult", "Answer"], 
                                    template = "\nQuestion: {Question}\nSQLQuery: {SQLQuery}\nSQLResult: {SQLResult}\nAnswer: {Answer}")
    fewShotPrompt = FewShotPromptTemplate(
        example_selector = exampleSelector,
        example_prompt = examplePrompt,
        prefix = _mysql_prompt,
        suffix = PROMPT_SUFFIX,
        input_variables = ["input", "table_info", "top_k"] #variables used in prompts
        )
    chain = SQLDatabaseChain.from_llm(llm, db, verbose=True, prompt = fewShotPrompt)
    return chain

if __name__ == '__main__':
    chain = get_few_shot_db_chain()
    print(chain.run("What is the price of inventory for all iphone?"))
