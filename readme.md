# Vector Store Comparison Demo

A simple demonstration comparing Pinecone and Weaviate vector stores using OpenAI embeddings.

## Project Structure

```bash
.
├── data/
│   ├── cat_facts.txt          # Sample dataset of cat facts
│   ├── passages.json          # Additional text passages for vector store
│   └── question_answer.json   # Q&A pairs for testing
├── notebooks/
│   ├── agents/                # Agent-based implementations
│   │   ├── langchain.ipynb    # LangChain agent with routing
│   │   └── claude.ipynb       # Claude-based intelligent agent
│   ├── chatbot/               # Chatbot implementations
│   │   ├── vector_store.ipynb # Document vectorization
│   │   ├── agent.ipynb        # RAG agent with Claude
│   │   ├── OpenAI/            # OpenAI text for DB
│   │   └── Anthropic/         # Anthropic text for DB
│   └── vector_stores/         # Vector store implementations
│       ├── pinecone.ipynb     # Pinecone vector store demo
│       └── weaviate.ipynb     # Weaviate vector store demo
└── requirements.txt           # Project dependencies
```




## Features

### Vector Stores (`notebooks/vector_stores/`)
- Implementations using both Pinecone and Weaviate
- Vector similarity search demonstrations
- OpenAI embeddings integration
- Basic RAG (Retrieval-Augmented Generation) examples

### Intelligent Agents (`notebooks/agents/`)
- LangChain-based routing system
- Claude integration for advanced reasoning
- Hybrid search capabilities
- Tool-based interaction patterns

### Chatbot (`notebooks/chatbot/`)
- Document chunking and vectorization
- RAG together with docuemnt retrieval implementation with Claude 
- Tool-use capabilities
- Provider-specific examples for OpenAI and Anthropic

## Setup

1. Create and activate virtual environment:
```bash
python3 -m venv venv
source venv/bin/activate # On Windows: venv\Scripts\activate
pip3 install -r requirements.txt
```


2. Create a `.env` file with your API keys:
```bash
OPENAI_API_KEY=your_openai_key
PINECONE_API_KEY=your_pinecone_key
WCD_URL=your_weaviate_cloud_url
WEAVIATE_API_KEY=your_weaviate_key
```

## Notebooks
- `pinecone.ipynb`: Demonstrates vector similarity search using Pinecone
- `weaviate.ipynb`: Shows the same functionality using Weaviate

Both notebooks follow similar steps:
1. Load text data
2. Create embeddings using OpenAI
3. Store vectors in the respective database
4. Perform similarity search
5. Format results using GPT

## Data
The demo uses a simple dataset of cat facts stored in `data/cat_facts.txt`. Each fact is converted into an embedding and stored in the vector database.

## Requirements
See `requirements.txt` for all dependencies.