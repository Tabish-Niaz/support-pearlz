import warnings
warnings.filterwarnings("ignore")
from langchain_core.messages import HumanMessage, AIMessage
from src.chains.rag_chain import get_rag_chain

def main():
    print("\n" + "="*50)
    print("🤖 SupportPearlz Agent (With Memory) is Ready!")
    print("Type 'exit' to quit, 'reset' to clear history.")
    print("="*50 + "\n")
    
    chain = get_rag_chain()
    chat_history = []
    
    while True:
        query = input("You ➔ ")
        if query.lower() in ['exit', 'quit', 'q']:
            print("Goodbye! 👋")
            break
        elif query.lower() == 'reset':
            chat_history = []
            print("🔄 Chat history cleared!")
            continue
            
        if not query.strip():
            continue
            
        try:
            # Direct response object mil raha hai
            response = chain.invoke({"input": query, "chat_history": chat_history})
            
            print(f"\nBot ➔ {response.answer}")
            
            if response.answered and response.sources:
                unique_sources = list(set(response.sources))
                print(f"\n   [Confidence: {response.confidence.upper()}]")
                print(f"   [Sources: {', '.join(unique_sources)}]")
            elif not response.answered:
                print(f"\n   [Confidence: NONE (Refused to guess)]")
            
            # History update karna
            chat_history.extend([HumanMessage(content=query), AIMessage(content=response.answer)])
            if len(chat_history) > 10:
                chat_history = chat_history[-10:]
                
        except Exception as e:
            print(f"\n⚠️ Error: {e}")
            
        print("\n" + "-" * 50 + "\n")

if __name__ == "__main__":
    main()