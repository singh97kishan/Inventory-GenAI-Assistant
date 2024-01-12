import joblib
from utilities import few_shots
from langchain.prompts import SemanticSimilarityExampleSelector
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import FAISS


def dump_embeddings(few_shots):
    embeddings = HuggingFaceEmbeddings(model_name = 'sentence-transformers/all-miniLM-L6-v2')
    to_vectorize = [' '.join(example.values()) for example in few_shots]
    vectorstore = FAISS.from_texts(to_vectorize, embeddings, metadatas=few_shots)
    joblib.dump(vectorstore, 'data/vectorstore.joblib')


if __name__=="__main__":
    dump_embeddings(few_shots)