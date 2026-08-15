from app.services.retriever import Retriever

retriever = Retriever()

query = "What is machine learning?"

results = retriever.retrieve(query)

print("\nTop Matches:\n")
results = retriever.retrieve(query)

for doc in results:
    
    
    print(doc)
    print("-" * 40)