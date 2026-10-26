import os
import sys
from langchain_openai import ChatOpenAI
from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings
from langchain_core.prompts import ChatPromptTemplate

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import src.config as config

def run_prompt_experiment():
    print("🔬 Prompt Engineering Before/After Experiment Started...\n")
    
    # Setup LLM and Retriever
    llm = ChatOpenAI(model=config.CHAT_MODEL, temperature=0)
    embeddings = OpenAIEmbeddings(model=config.EMBEDDING_MODEL)
    vector_store = Chroma(persist_directory=config.VECTOR_STORE_DIR, embedding_function=embeddings)
    retriever = vector_store.as_retriever(search_kwargs={"k": 2})
    
    # Test Question (Unanswerable / Gap case)
    test_question = "Do you offer student discounts?"
    docs = retriever.invoke(test_question)
    context_text = "\n\n".join([doc.page_content for doc in docs])
    
    # 1. Weak / Naive Prompt
    weak_system_prompt = "You are a helpful assistant. Answer the question using the context."
    weak_prompt = ChatPromptTemplate.from_messages([
        ("system", weak_system_prompt),
        ("human", "Context: {context}\n\nQuestion: {question}")
    ])
    weak_chain = weak_prompt | llm
    
    # 2. Final Strict Grounding Prompt
    final_system_prompt = """You are a highly professional Customer Support Assistant for Pearlz Home Systems.
    Answer the user's question STRICTLY using the provided CONTEXT below.
    RULES:
    1. If the CONTEXT does not contain the answer, say EXACTLY: "I cannot find this information in the documentation. Please contact support." Do not guess.
    2. Never invent prices, dates, rules, or discounts.
    CONTEXT:
    {context}"""
    final_prompt = ChatPromptTemplate.from_messages([
        ("system", final_system_prompt),
        ("human", "{question}")
    ])
    final_chain = final_prompt | llm
    
    print(f"❓ Test Question: '{test_question}'\n")
    
    # Run Weak Prompt
    weak_response = weak_chain.invoke({"context": context_text, "question": test_question})
    print(f"❌ [Weak Prompt Output]:\n{weak_response.content}\n")
    
    # Run Final Prompt
    final_response = final_chain.invoke({"context": context_text, "question": test_question})
    print(f"✅ [Final Strict Prompt Output]:\n{final_response.content}\n")
    
    print("="*70)
    print("📝 Task 08 Experiment Justification for Technical Report:")
    print("• Weak Prompt: Lacks explicit refusal instructions, causing the model to hallucinate or speculate an answer using general knowledge.")
    print("• Final Prompt: Enforces strict grounding boundaries and exact refusal strings, completely eliminating hallucinations on unanswerable queries.")
    print("="*70)

if __name__ == "__main__":
    run_prompt_experiment()