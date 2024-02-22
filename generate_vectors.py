import joblib
from utilities import few_shots
from langchain.prompts import SemanticSimilarityExampleSelector
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain.vectorstores import FAISS


def dump_embeddings(few_shots):
    embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
    to_vectorize = [' '.join(example.values()) for example in few_shots]
    vectorstore = FAISS.from_texts(to_vectorize, embeddings, metadatas=few_shots)
    joblib.dump(vectorstore, 'data/vectorstore.joblib')


if __name__=="__main__":
    dump_embeddings(few_shots)