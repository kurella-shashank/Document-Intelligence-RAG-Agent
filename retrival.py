from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma

# Use HuggingFaceEmbeddings wrapper instead of SentenceTransformer directly
embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

# Load the vectorstore
vectorstore = Chroma(embedding_function=embeddings, persist_directory="./vectordb")

# Load existing vectorstore
vectorstore = Chroma(
    embedding_function=embeddings,
    persist_directory="./vectordb"
    )

import redis
import json
r = redis.Redis(host='localhost', port=6379, decode_responses=True)
# r.set("who are you?", "I am Shashank!")
while True:
    question = input("Ask anything!: ")
    
    if question.lower() in ['exit', 'quit']:
        break
    
    # Check cache
    cache = r.get(question)
    
    if cache:
        print("\n[From Cache]")
        cached_results = json.loads(cache)
        for i, result in enumerate(cached_results, 1):
            print(f"\n--- Result {i} ---")
            print(result['content'][:200])
            print(f"Metadata: {result['metadata']}")
    else:
        print("\n[From Vector Store]")
        results = vectorstore.similarity_search(question, k=3)
        
        # Convert Document objects to serializable format
        serializable_results = [
            {
                'content': doc.page_content,
                'metadata': doc.metadata
            }
            for doc in results
        ]
        
        # Store in Redis as JSON string
        r.set(question, json.dumps(serializable_results), ex=3600)  # Cache for 1 hour
        
        # Print results
        for i, doc in enumerate(results, 1):
            print(f"\n--- Result {i} ---")
            print(doc.page_content[:200])
            print(f"Metadata: {doc.metadata}")