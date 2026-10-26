import os
import sys
import time
from pydantic import BaseModel, Field
from typing import List
from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
import src.config as config
from src.utils.logging_setup import logger

class SupportResponse(BaseModel):
    answer: str = Field(description="Mukammal jawab.")
    sources: List[str] = Field(description="Use kiye gaye sources ke exact naam.")
    confidence: str = Field(description="'high', 'partial', ya 'none'")
    answered: bool = Field(description="Agar context mein jawab mila toh True, warna False")

def get_rag_chain():
    try:
        embeddings = OpenAIEmbeddings(model=config.EMBEDDING_MODEL)
        vector_store = Chroma(persist_directory=config.VECTOR_STORE_DIR, embedding_function=embeddings)
        retriever = vector_store.as_retriever(search_kwargs={"k": 4})
        logger.info("Vector store loaded successfully for RAG chain.")
    except Exception as e:
        logger.error(f"Failed to load vector store: {e}")
        raise RuntimeError("Vector store load nahi ho saka. Pehle 'python -m src.ingestion.build_index' run karein.")
    
    llm = ChatOpenAI(model=config.CHAT_MODEL, temperature=0)
    structured_llm = llm.with_structured_output(SupportResponse)

    qa_system_prompt = """You are a professional Customer Support Assistant for Pearlz Home Systems.
    Answer STRICTLY using the provided CONTEXT. 
    1. If not found in CONTEXT, say EXACTLY: "I cannot find this information in the documentation. Please contact support."
    2. Never invent prices, dates, or warranty rules.
    3. Cite only the exact source files provided in the CONTEXT.
    
    CONTEXT:
    {context}"""
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", qa_system_prompt),
        MessagesPlaceholder("chat_history"),
        ("human", "{input}"),
    ])
    
    def format_docs(docs):
        formatted = []
        for doc in docs:
            source = doc.metadata.get('source', 'unknown')
            formatted.append(f"Source: {source}\n{doc.page_content}")
        return "\n\n".join(formatted)

    class ProductionRAGChain:
        def invoke(self, inputs):
            start_time = time.time()
            query = inputs.get("input", "")
            history = inputs.get("chat_history", [])
            
            logger.info(f"Incoming Query: '{query}'")
            
            try:
                # 1. Retrieval with scores/metadata
                docs = retriever.invoke(query)
                retrieved_sources = list(set([doc.metadata.get('source', 'unknown') for doc in docs]))
                context_text = format_docs(docs)
                
                logger.info(f"Retrieved {len(docs)} chunks from sources: {retrieved_sources}")
                
                # 2. LLM Invocation
                chain = prompt | structured_llm
                response = chain.invoke({
                    "context": context_text,
                    "chat_history": history,
                    "input": query
                })
                
                # 3. Citation Validation (Feature 5 / Task 10): Drop fake/un-supplied citations
                validated_sources = []
                if response.answered and response.sources:
                    for src in response.sources:
                        if any(src.lower() in rs.lower() for rs in retrieved_sources):
                            validated_sources.append(src)
                        else:
                            logger.warning(f"Dropped hallucinated/un-supplied citation: '{src}'")
                    response.sources = list(set(validated_sources))
                    
                # Fallback if sources empty but answered
                if response.answered and not response.sources:
                    response.sources = retrieved_sources
                
                latency = round(time.time() - start_time, 2)
                logger.info(f"Turn completed successfully in {latency}s. Answered: {response.answered}, Confidence: {response.confidence}")
                
                return response
                
            except Exception as e:
                latency = round(time.time() - start_time, 2)
                logger.error(f"Error during chain execution after {latency}s: {e}")
                # Graceful degradation fallback object
                return SupportResponse(
                    answer="An unexpected error occurred while processing your request. Please contact support.",
                    sources=[],
                    confidence="none",
                    answered=False
                )

    return ProductionRAGChain()