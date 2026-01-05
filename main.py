from langchain_community.document_loaders import PyMuPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from extract_images import extract_images
from dotenv import load_dotenv
import os

load_dotenv()

# Use HuggingFaceEmbeddings consistently
embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

# Load and process the PDF
loader = PyMuPDFLoader(file_path=os.getenv("file_path"))
extract_images(os.getenv("file_path"))
documents = loader.load()

# Split documents into chunks
splitter = RecursiveCharacterTextSplitter(chunk_size=100, chunk_overlap=50)
chunks = splitter.split_documents(documents)  # Use split_documents instead of split_text

# Create or load vectorstore and add documents
vectorstore = Chroma.from_documents(
    documents=chunks,
    embedding=embeddings,
    persist_directory="./vectordb"
)

print(f"Added {len(chunks)} chunks to vectorstore")

# Perform similarity search
results = vectorstore.similarity_search("what is ai?", k=3)

# Print results
for i, doc in enumerate(results, 1):
    print(f"\n--- Result {i} ---")
    print(doc.page_content)  # Print first 200 chars
    print(f"Metadata: {doc.metadata}")