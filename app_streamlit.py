# import streamlit as st
# from langchain_core.messages import HumanMessage, AIMessage
# from src.chains.rag_chain import get_rag_chain

# st.set_page_config(page_title="SupportPearlz Assistant", page_icon="🤖", layout="centered")

# st.title("🤖 SupportPearlz Customer Support Agent")
# st.markdown("Ask questions about Pearlz Home Systems products, warranties, and policies.")

# # Initialize RAG chain
# @st.cache_resource
# def load_chain():
#     return get_rag_chain()

# chain = load_chain()

# # Initialize session state for chat history
# if "chat_history" not in st.session_state:
#     st.session_state.chat_history = []

# # Display chat history
# for message in st.session_state.chat_history:
#     role = "user" if isinstance(message, HumanMessage) else "assistant"
#     with st.chat_message(role):
#         st.markdown(message.content)

# # User input handling
# if query := st.chat_input("Type your support question here..."):
#     with st.chat_message("user"):
#         st.markdown(query)
        
#     with st.chat_message("assistant"):
#         with st.spinner("Searching documentation and thinking..."):
#             try:
#                 response = chain.invoke({"input": query, "chat_history": st.session_state.chat_history})
                
#                 # Answer display
#                 st.markdown(response.answer)
                
#                 # Confidence & Sources display
#                 if response.answered and response.sources:
#                     unique_sources = list(set(response.sources))
#                     st.info(f"**Confidence:** {response.confidence.upper()} | **Sources:** {', '.join(unique_sources)}")
#                 elif not response.answered:
#                     st.warning(f"**Confidence:** NONE (Refused to guess)")
                
#                 # Update history
#                 st.session_state.chat_history.extend([
#                     HumanMessage(content=query), 
#                     AIMessage(content=response.answer)
#                 ])
                
#             except Exception as e:
#                 st.error(f"An error occurred: {e}")

# # Sidebar reset button
# if st.sidebar.button("Clear Chat History"):
#     st.session_state.chat_history = []
#     st.rerun()


# import streamlit as st
# from langchain_core.messages import HumanMessage, AIMessage
# from src.chains.rag_chain import get_rag_chain

# # --- Page Configuration ---
# st.set_page_config(
#     page_title="SupportPearlz | AI Customer Support Agent",
#     page_icon="🤖",
#     layout="wide",
#     initial_sidebar_state="expanded"
# )

# # --- Custom CSS Styling for Professional Look ---
# st.markdown("""
#     <style>
#     .main {
#         background-color: #f8f9fa;
#     }
#     .stChatMessage {
#         padding: 15px;
#         border-radius: 12px;
#         margin-bottom: 10px;
#     }
#     .stChatInputContainer {
#         padding-bottom: 20px;
#     }
#     .css-1v0mbdj {
#         border-right: 1px solid #e0e0e0;
#     }
#     h1 {
#         color: #1f4e79;
#         font-family: 'Helvetica Neue', sans-serif;
#     }
#     .metric-box {
#         background-color: #ffffff;
#         padding: 10px 15px;
#         border-radius: 8px;
#         border-left: 4px solid #1f4e79;
#         box-shadow: 0 2px 4px rgba(0,0,0,0.05);
#         margin-bottom: 10px;
#     }
#     </style>
# """, unsafe_allow_html=True)

# # --- Sidebar Configuration & Info ---
# with st.sidebar:
#     st.image("https://img.icons8.com/color/96/artificial-intelligence.png", width=70)
#     st.title("SupportPearlz Ops")
#     st.markdown("---")
#     st.markdown("### 🛠️ System Status")
#     st.success("🟢 Vector Store: Active")
#     st.success("🟢 LLM Engine: GPT-4o-mini")
#     st.success("🟢 Grounding Guardrail: ON")
    
#     st.markdown("---")
#     st.markdown("### 📊 Session Controls")
#     if st.button("🗑️ Clear Conversation", use_container_width=True):
#         st.session_state.chat_history = []
#         st.rerun()
        
#     st.markdown("---")
#     st.markdown("<small>Designed for Pearlz Home Systems <br> Advanced RAG Agent v2.4</small>", unsafe_allow_html=True)

# # --- Main Header ---
# st.title("🤖 SupportPearlz AI Assistant")
# st.markdown("Welcome to the enterprise customer intelligence portal. Ask queries regarding product manuals, warranties, return policies, or troubleshooting codes.")
# st.markdown("---")

# # --- Initialize RAG Chain ---
# @st.cache_resource
# def load_chain():
#     return get_rag_chain()

# with st.spinner("Initializing neural retrieval pipeline..."):
#     chain = load_chain()

# # --- Initialize Session State ---
# if "chat_history" not in st.session_state:
#     st.session_state.chat_history = []

# # --- Render Chat History ---
# for message in st.session_state.chat_history:
#     role = "user" if isinstance(message, HumanMessage) else "assistant"
#     with st.chat_message(role, avatar="🧑‍💻" if role == "user" else "🤖"):
#         st.markdown(message.content)

# # --- Chat Input & Response Handling ---
# if query := st.chat_input("Type your support query here (e.g., 'What is the return window?')"):
#     # Display user message
#     with st.chat_message("user", avatar="🧑‍💻"):
#         st.markdown(query)
        
#     # Display assistant response with loading spinner
#     with st.chat_message("assistant", avatar="🤖"):
#         with st.spinner("🔍 Searching knowledge base & verifying citations..."):
#             try:
#                 response = chain.invoke({"input": query, "chat_history": st.session_state.chat_history})
                
#                 # Main Answer
#                 st.markdown(response.answer)
                
#                 # Metadata / Confidence Card Display
#                 if response.answered and response.sources:
#                     unique_sources = list(set(response.sources))
#                     conf_color = "green" if response.confidence.lower() == "high" else "orange"
                    
#                     st.markdown(f"""
#                         <div class="metric-box">
#                             <span style="color: {conf_color}; font-weight: bold;">● CONFIDENCE: {response.confidence.upper()}</span><br>
#                             <span style="color: #555; font-size: 0.9em;">📚 <b>Verified Sources:</b> {', '.join(unique_sources)}</span>
#                         </div>
#                     """, unsafe_allow_html=True)
                    
#                 elif not response.answered:
#                     st.markdown("""
#                         <div class="metric-box" style="border-left-color: #d9534f;">
#                             <span style="color: #d9534f; font-weight: bold;">● STATUS: REFUSED (Out of Scope / Unanswerable)</span><br>
#                             <span style="color: #555; font-size: 0.9em;">🛡️ Grounding guardrail blocked unverified generation.</span>
#                         </div>
#                     """, unsafe_allow_html=True)
                
#                 # Append to Session History
#                 st.session_state.chat_history.extend([
#                     HumanMessage(content=query), 
#                     AIMessage(content=response.answer)
#                 ])
                
#             except Exception as e:
#                 st.error(f"⚠️ System Encountered an Error: {e}")

import streamlit as st
from langchain_core.messages import HumanMessage, AIMessage
from src.chains.rag_chain import get_rag_chain

# --- Page Configuration ---
st.set_page_config(
    page_title="SupportPearlz | AI Customer Intelligence",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Advanced Glassmorphism & Cyber-Dark UI Styling ---
st.markdown("""
    <style>
    /* Main Background & Font */
    .stApp {
        background: linear-gradient(135deg, #0f172a 0%, #1e1b4b 100%);
        color: #f8fafc;
        font-family: 'Inter', sans-serif;
    }
    
    /* Sidebar Styling */
    [data-testid="stSidebar"] {
        background-color: #090d16;
        border-right: 1px solid rgba(255, 255, 255, 0.1);
    }
    
    /* Chat Bubble Styling */
    .stChatMessage {
        background: rgba(255, 255, 255, 0.03);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 16px;
        padding: 20px;
        backdrop-filter: blur(10px);
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37);
        margin-bottom: 16px;
    }
    
    /* Input Box Container */
    .stChatInputContainer {
        padding-bottom: 25px;
    }
    .stChatInputContainer textarea {
        background-color: rgba(255, 255, 255, 0.05) !important;
        color: #ffffff !important;
        border: 1px solid rgba(255, 255, 255, 0.15) !important;
        border-radius: 12px !important;
    }

    /* Custom Header Title */
    .main-title {
        font-size: 2.5rem;
        font-weight: 800;
        background: linear-gradient(90deg, #38bdf8, #818cf8, #c084fc);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0px;
    }
    
    .sub-title {
        color: #94a3b8;
        font-size: 1.05rem;
        margin-top: 5px;
        margin-bottom: 25px;
    }

    /* Enterprise Metric Card */
    .enterprise-card {
        background: rgba(15, 23, 42, 0.7);
        border: 1px solid rgba(56, 189, 248, 0.2);
        border-left: 5px solid #38bdf8;
        padding: 14px 18px;
        border-radius: 10px;
        margin-top: 12px;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.2);
    }
    
    .refusal-card {
        background: rgba(43, 15, 20, 0.7);
        border: 1px solid rgba(248, 113, 113, 0.2);
        border-left: 5px solid #f87171;
        padding: 14px 18px;
        border-radius: 10px;
        margin-top: 12px;
    }
    
    /* Sidebar Badges */
    .status-badge {
        display: inline-block;
        padding: 4px 10px;
        border-radius: 20px;
        font-size: 0.75rem;
        font-weight: 600;
        background: rgba(34, 197, 94, 0.15);
        color: #4ade80;
        border: 1px solid rgba(34, 197, 94, 0.3);
        margin-bottom: 6px;
    }
    </style>
""", unsafe_allow_html=True)

# --- Sidebar Command Center ---
with st.sidebar:
    st.markdown("### ⚡ SupportPearlz Core")
    st.markdown("<div class='status-badge'>🟢 RAG Engine Online</div>", unsafe_allow_html=True)
    st.markdown("<div class='status-badge'>🛡️ Grounding Guardrail Active</div>", unsafe_allow_html=True)
    
    st.markdown("---")
    st.markdown("#### ⚙️ System Specifications")
    st.markdown("""
    - **Orchestration:** LangChain LCEL
    - **Vector Index:** ChromaDB (Persisted)
    - **Embeddings:** OpenAI Small
    - **Generation Model:** GPT-4o-mini
    """)
    
    st.markdown("---")
    st.markdown("#### 🎛️ Session Management")
    if st.button("🗑️ Clear Chat History", use_container_width=True):
        st.session_state.chat_history = []
        st.rerun()
        
    st.markdown("---")
    st.markdown("<p style='font-size:0.8rem; color:#64748b;'>Pearlz Home Systems (Pvt) Ltd.<br>Advanced Support Intelligence v2.5</p>", unsafe_allow_html=True)

# --- Main Header ---
st.markdown('<p class="main-title">🛡️ SupportPearlz Intelligence Hub</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-title">Enterprise-grade RAG Support Assistant with strict grounding guardrails, automated source attribution, and conversational memory.</p>', unsafe_allow_html=True)

# --- Initialize RAG Chain ---
@st.cache_resource
def load_chain():
    return get_rag_chain()

with st.spinner("🔄 Loading vector index and binding neural pipeline..."):
    chain = load_chain()

# --- Initialize Session State ---
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# --- Render Chat History ---
for message in st.session_state.chat_history:
    role = "user" if isinstance(message, HumanMessage) else "assistant"
    avatar = "👤" if role == "user" else "🤖"
    with st.chat_message(role, avatar=avatar):
        st.markdown(message.content)

# --- Chat Input & Response Pipeline ---
if query := st.chat_input("Ask a support query (e.g., 'What is the return window for opened items?')"):
    
    # User message
    with st.chat_message("user", avatar="👤"):
        st.markdown(query)
        
    # Assistant response
    with st.chat_message("assistant", avatar="🤖"):
        with st.spinner("🔍 Executing semantic search, context retrieval & guardrail validation..."):
            try:
                response = chain.invoke({"input": query, "chat_history": st.session_state.chat_history})
                
                # Main Answer Text
                st.markdown(response.answer)
                
                # Verified Source Attribution Card or Refusal Card
                if response.answered and response.sources:
                    unique_sources = list(set(response.sources))
                    conf_color = "#4ade80" if response.confidence.lower() == "high" else "#facc15"
                    
                    st.markdown(f"""
                        <div class="enterprise-card">
                            <span style="color: {conf_color}; font-weight: 700; font-size: 0.85em;">● CONFIDENCE: {response.confidence.upper()}</span><br>
                            <span style="color: #cbd5e1; font-size: 0.9em; margin-top: 4px; display: inline-block;">📚 <b>Verified Citations:</b> {', '.join(unique_sources)}</span>
                        </div>
                    """, unsafe_allow_html=True)
                    
                elif not response.answered:
                    st.markdown("""
                        <div class="refusal-card">
                            <span style="color: #f87171; font-weight: 700; font-size: 0.85em;">● GUARDRAIL: REFUSAL TRIGGERED</span><br>
                            <span style="color: #cbd5e1; font-size: 0.9em; margin-top: 4px; display: inline-block;">🛡️ Out-of-scope query successfully blocked from hallucination.</span>
                        </div>
                    """, unsafe_allow_html=True)
                
                # Update Session History
                st.session_state.chat_history.extend([
                    HumanMessage(content=query), 
                    AIMessage(content=response.answer)
                ])
                
            except Exception as e:
                st.error(f"⚠️ Pipeline Error Encountered: {e}")