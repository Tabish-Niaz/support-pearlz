# SupportPearlz: Customer Support RAG Knowledge Agent

**Course:** AAI-407/PRAC-03 (Agentic AI / Generative AI)  
**Level:** Advanced  
**Stack:** Python, LangChain, OpenAI, ChromaDB, Pydantic  

SupportPearlz is an advanced, production-grade Retrieval-Augmented Generation (RAG) customer support assistant built for **Pearlz Home Systems**. It ingests heterogeneous company documents into a persistent vector store, processes multi-turn customer queries with conversation history and query rewriting, enforces strict grounding and refusal policies, validates citations, and provides structured outputs.

---

## 🚀 Project Features & Architecture

* **Two Separate Pipelines:** Clean separation between the offline *Ingestion Pipeline* (document loading, splitting, embedding, persistence) and the online *Query Pipeline* (retrieval, relevance gate, prompt templating, LLM generation, citation resolution)[cite: 6, 7].
* **Heterogeneous Loaders:** Automatically parses and normalizes PDF manuals, Markdown policies, and CSV pricing sheets[cite: 10, 12].
* **Persistent Vector Store:** Powered by ChromaDB; indexes are built once and loaded directly from disk on subsequent runs without re-embedding[cite: 8, 13].
* **Conversational Memory & Query Condensation:** Manages chat history and rewrites pronoun-heavy follow-up questions into standalone queries[cite: 15, 17].
* **Strict Grounding & Refusal:** Prevents hallucinations by forcing the model to answer strictly from retrieved context and refuse unanswerable questions[cite: 15, 17].
* **Automated Evaluation Harness:** Built-in test runner that executes test cases across categories (Easy, Multi-step, Unanswerable, Adversarial) and logs results[cite: 16, 18].

---

## 📂 Project Directory Structure
```text
SupportPearlz_Project/
├── data/
│   ├── knowledge_base/      # 10+ authored source documents (PDF, MD, CSV)
│   └── vector_store/        # Persisted ChromaDB index (git-ignored)
├── logs/                    # Centralized system execution logs
├── src/
│   ├── config.py            # Validated settings via python-dotenv
│   ├── ingestion/           # Document loaders and chunking modules
│   ├── retrieval/           # Retriever configuration
│   ├── chains/              # RAG chain, prompts, and Pydantic schemas
│   └── utils/               # Centralized logging setup
├── evaluation/
│   ├── test_questions.json  # Comprehensive test cases
│   ├── run_eval.py          # Automated evaluation runner
│   └── results/             # Generated evaluation json reports
├── docs/                    # Architecture diagram & technical report
├── screenshots/             # Execution and output screenshots
├── app_cli.py               # Interactive CLI chat entry point
├── requirements.txt         # Pinned python dependencies
└── README.md


⚙️ Prerequisites & Setup Instructions

1. Clone or Open the Project

Ensure you are in the project root directory:
cd SupportPearlz_Project

2. Create and Activate Virtual Environment

python -m venv venv
# On Windows:
venv\Scripts\activate

3. Install Dependencies

Install the required pinned packages:   

pip install -r requirements.txt

4. Configure Environment Variables

Create a .env file in the root directory based on your configuration needs (or copy from an example):

Code snippet

OPENAI_API_KEY=your_openai_api_key_here
CHAT_MODEL=gpt-4o-mini
EMBEDDING_MODEL=text-embedding-3-small
VECTOR_STORE_DIR=data/vector_store
KNOWLEDGE_BASE_DIR=data/knowledge_base
CHUNK_SIZE=800
CHUNK_OVERLAP=120
RETRIEVAL_K=4
LOG_LEVEL=INFO

⚠️ Note: Never commit your actual .env file or API keys to version control.   


🔨 How to Run the Project

Step 1: Build the Vector Index (Ingestion Pipeline)

Run the ingestion script to load, split, and embed all knowledge base documents into the persistent vector store:
python -m src.ingestion.build_index

(Subsequent runs will load the index directly from disk without re-embedding).

Step 2: Start the Interactive Chat (Query Pipeline)

Launch the command-line assistant loop:   

python app_cli.py


Commands inside CLI:

Type your question normally (e.g., "What is the return window?").

Type reset to clear conversation history.

Type exit or quit to close the session.


Step 3: Run the Automated Evaluation Harness

To execute the test suite and generate evaluation reports in evaluation/results/:

python evaluation/run_eval.py


🛡️ Known Limitations

The system relies strictly on retrieved context; queries requiring real-time external data (such as live shipment tracking or weather) are correctly routed to the refusal path.

Semantic retrieval may occasionally require exact SKU matching adjustments, which are mitigated via structured pricing CSV handling.