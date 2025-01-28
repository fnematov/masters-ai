import os
from dotenv import load_dotenv
from PyPDF2 import PdfReader
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.chains import RetrievalQA
from langchain.chat_models import ChatOpenAI

# Required Libraries
# pip install PyPDF2 langchain faiss-cpu openai python-dotenv

# Load environment variables
load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")
if not openai_api_key:
    raise ValueError("OPENAI_API_KEY is not set in the .env file.")

# Step 1: Load PDF and Extract Text
def extract_text_from_pdf(pdf_path):
    reader = PdfReader(pdf_path)
    text = ""
    for page in reader.pages:
        text += page.extract_text() or ""
    return text

# Step 2: Initialize FAISS Vectorstore
def create_vectorstore(text):
    embeddings = OpenAIEmbeddings(openai_api_key=openai_api_key)
    texts = text.split("\n")  # Split into smaller chunks if needed
    vectorstore = FAISS.from_texts(texts, embeddings)
    return vectorstore

# Step 3: Create QA Chain
def create_qa_chain(vectorstore):
    retriever = vectorstore.as_retriever()
    retriever.search_kwargs["k"] = 5  # Retrieve top 5 results
    llm = ChatOpenAI(
        temperature=0,
        openai_api_key=openai_api_key,
        system_prompt=(
            "You are an expert assistant designed to provide precise and reliable answers regarding the Uzbekistan Tax Code as outlined in the provided document. Always ensure your responses are clear, concise, and based solely on the content of the document. When explaining complex topics, use simple language and examples to ensure customer understanding. If a question is ambiguous, ask for clarification instead of making assumptions. Your priority is to provide legally accurate information while maintaining professionalism and clarity"
        )
    )
    qa_chain = RetrievalQA.from_chain_type(llm=llm, retriever=retriever, return_source_documents=True)
    return qa_chain

# Step 4: Chat with PDF
def chat_with_pdf(qa_chain):
    print("\nChat with your PDF! Type 'exit' to end the chat.")
    while True:
        query = input("You: ")
        if query.lower() == 'exit':
            print("Exiting chat. Goodbye!")
            break
        result = qa_chain({"query": query})
        if result["source_documents"]:
            print("AI:", result["result"])
            print("Sources:", [doc.page_content for doc in result["source_documents"]])
        else:
            print("AI: I couldn't find relevant information in the document.")

if __name__ == "__main__":
    pdf_path = "chat_data.pdf"  # PDF file name

    if not os.path.exists(pdf_path):
        print(f"Error: File '{pdf_path}' not found.")
    else:
        # Extract text from PDF
        pdf_text = extract_text_from_pdf(pdf_path)

        # Create vectorstore
        vectorstore = create_vectorstore(pdf_text)

        # Create QA chain
        qa_chain = create_qa_chain(vectorstore)

        # Start chat
        chat_with_pdf(qa_chain)