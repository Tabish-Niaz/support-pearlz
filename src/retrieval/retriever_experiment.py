import os
import sys
from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
import src.config as config

def run_retriever_experiments():
    print("🔍 Retriever Strategy Experiment Started...\n")
    
    # 1. Load Vector Store
    embeddings = OpenAIEmbeddings(model=config.EMBEDDING_MODEL)
    vector_store = Chroma(
        persist_directory=config.VECTOR_STORE_DIR, 
        embedding_function=embeddings
    )
    
    # Test queries (jaise manual ke mutabiq)
    test_queries = [
        "How long is the warranty on the AquaPearl 500 Pro?",
        "My purifier beeps three times and the light flashes red.",
        "What is the return window for unused items?"
    ]
    
    strategies = [
        {"name": "Plain Similarity (k=3)", "search_type": "similarity", "search_kwargs": {"k": 3}},
        {"name": "Plain Similarity (k=8)", "search_type": "similarity", "search_kwargs": {"k": 8}},
        {"name": "MMR (Diversity, k=4)", "search_type": "mmr", "search_kwargs": {"k": 4, "fetch_k": 10}}
    ]

    print(f"{'Strategy':<30} | {'Query Index':<12} | {'Retrieved Chunks':<18}")
    print("-" * 70)

    for strat in strategies:
        retriever = vector_store.as_retriever(
            search_type=strat["search_type"],
            search_kwargs=strat["search_kwargs"]
        )
        
        for idx, query in enumerate(test_queries, 1):
            docs = retriever.invoke(query)
            print(f"{strat['name']:<30} | Query #{idx:<10} | {len(docs):<18}")
            
    print("\n" + "="*70)
    print("📝 Task 06 Justification & Relevance Gate for Technical Report:")
    print("• Plain Similarity (small k=3) offers high precision but risks missing context if the answer spans chunks.")
    print("• Plain Similarity (large k=8) broadens recall but introduces noise and dilutes the prompt context.")
    print("• MMR (Maximal Marginal Relevance) trades off relevance against redundancy, selecting diverse chunks which is ideal for multi-step queries.")
    print("• Relevance Gate Rule: If the top vector similarity score falls below an empirically calibrated threshold, the system declares 'no relevant information found' and triggers the refusal path.")
    print("="*70)

if __name__ == "__main__":
    run_retriever_experiments()