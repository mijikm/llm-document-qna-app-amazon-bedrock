import json
import os
import sys
import boto3
import streamlit as st

### Embeddings ###
## Amazon Titan Embeddings Model will be used to generate embeddings.
## This embedding model will be called from a langchain library.
## langchain provides multiple options to interact with Amazon Bedrock.
from langchain.embeddings import BedrockEmbeddings
from langchain_community.llms import Bedrock

### Data Ingestion ###
import numpy as np 
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFDirectoryLoader

### Vector Embedding And Vector Store ###
from langchain.vectorstores import FAISS

### LLm Models ###
from langchain.prompts import PromptTemplate
from langchain.chains import RetrievalQA


### Bedrock Clients ###
# Define the model ID for Amazon Titan Embeddings G1 - Text
titan_model_id = "amazon.titan-embed-text-v1"

# Initialize the Bedrock Runtime client
client = boto3.client('bedrock-runtime', region_name = 'us-east-1')

# Call the embedding model from the Bedrock client
bedrock_embeddings = BedrockEmbeddings(model_id=titan_model_id, client=client)


## Data Ingestion ##
def data_ingestion():
    # Check if the data directory exists
    if not os.path.exists("data"):
        st.error("Data directory not found. Please create a 'data' directory and add PDF files.")
        # Count the number of PDFs found
        num_pdfs = 0

        return None

    # Check if any PDF files exist in the directory
    pdf_files = [file for file in os.listdir("data") if file.lower().endswith(".pdf")]
    
    # Count the number of PDFs found
    num_pdfs = len(pdf_files)

    # If no PDFs are found, raise an error using Streamlit
    if num_pdfs == 0:
        return None, num_pdfs  # Exit the function if no PDFs are found

    # Load all the PDF files from the specified directory
    loader = PyPDFDirectoryLoader("data")
    documents = loader.load()

    # Split the documents into smaller chunks for better processing
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=10000, chunk_overlap=1000)
    docs = text_splitter.split_documents(documents)

    return docs, num_pdfs

## Vector Embedding And Vector Store ##
def get_vector_store(docs):
    # Create a vector store using FAISS and the Bedrock embeddings
    vector_store_faiss = FAISS.from_documents(
        docs, 
        bedrock_embeddings
    )
    vector_store_faiss.save_local("faiss_index")

# Create Ahtnropic's Claude model (Claude 2.1)
def get_claude_llm():
    # Initialize the Bedrock LLM client
    llm = Bedrock(
        model_id="anthropic.claude-v2:1", 
        client=client,
        model_kwargs={
            "temperature": 0.7, # Controls randomness in the output (0.0 to 1.0)
            "top_p": 0.9 # Controls the cumulative probability for sampling
        }
    )
    return llm

# Create Mistral AI's Mistral 7B Instruct
def get_mistral_llm():
    # Initialize the Bedrock LLM client
    llm = Bedrock(
        model_id="mistral.mistral-7b-instruct-v0:2", 
        client=client,
        model_kwargs={
            "temperature": 0.7,
            "top_p": 0.9,
            "max_tokens": 512 # Can be changed to 1024 or 2048
        }
        )
    
    return llm

# Create a prompt template for the LLM
prompt_template = """

Human: Use the following pieces of context to provide a concise answer to the question at the end but summarize with at least 80 words and maximum 200 words with detailed explanations.
If you don't know the answer, just say "I don't know" and don't try to make up an answer.
<context>
{context}
</context>

Questions: {question}

Assistant:
"""

# Create a prompt template for the LLM
PROMPT = PromptTemplate(
    template=prompt_template, 
    input_variables=["context", "question"]
)

# Response Generation
def get_response_llm(llm, vector_store_faiss, query):
    # Create a RetrievalQA chain with the LLM and vector store
    qa = RetrievalQA.from_chain_type(
        llm=llm, 
        # text summarization technique
        chain_type="stuff", 
        # vector_store_faiss has the entire index of documents
        retriever=vector_store_faiss.as_retriever(
            search_type="similarity",
            search_kwargs={"k": 3} #top 3 similar documents
            ), 
        return_source_documents=True,
        chain_type_kwargs={"prompt": PROMPT}
    )
    # qa will retrieve the response from the LLM model and store the response in the answer variable
    answer=qa({"query": query})

    return answer['result']


def main():
    st.set_page_config(page_title="Chat PDF", page_icon=":guardsman:", layout="wide")
    st.header("Chat with PDF using Amazon Bedrock💁‍♀️")

    user_question = st.text_input("Ask a question about the PDF Files:")

    # Load the vector store from the local faiss_index directory
    faiss_index = FAISS.load_local("faiss_index", bedrock_embeddings, allow_dangerous_deserialization=True)

    with st.sidebar:
        st.title("Update or Create Vector Store:")

        # Once clicked, it will load the PDF files and convert those into vector stores and store them under faiss_index using FAISS.
        if st.button("Vector Stores Update"):
            with st.spinner("Processing...."):
                docs, num_pdfs = data_ingestion()

                if docs is None:
                    # Handle the case where no PDFs are found
                    st.error(f"No PDF files found. Please upload a PDF.")
                else:
                    st.write(f"Found {num_pdfs} PDF file(s).")
                    # Create a vector store using FAISS and the Bedrock embeddings
                    get_vector_store(docs)
                    st.success("Done - Vector Store Updated!")

    if st.button("Claude Output"):
        # Check if the user has entered a question
        if not user_question.strip():
            st.error("Please enter a question.")
        else:
            with st.spinner("Processing...."):
                # Get the Claude LLM model
                llm = get_claude_llm()

                st.write(get_response_llm(llm,faiss_index, user_question))
                st.success("Done")
    
    if st.button("Mistral Output"):
        # Check if the user has entered a question
        if not user_question.strip():
            st.error("Please enter a question.")
        else:
            with st.spinner("Processing...."):
                # Get the Claude LLM model
                llm = get_mistral_llm()

                st.write(get_response_llm(llm,faiss_index, user_question))
                st.success("Done")

if __name__ == "__main__":
    main()