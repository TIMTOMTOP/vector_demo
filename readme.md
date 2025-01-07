# Vector Store Comparison Demo

A simple demonstration comparing Pinecone and Weaviate vector stores using OpenAI embeddings.

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