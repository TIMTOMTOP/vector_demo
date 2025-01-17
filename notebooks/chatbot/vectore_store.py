#%%
from pinecone import Pinecone, ServerlessSpec
import os
import dotenv
import json
from tqdm import tqdm
from openai import OpenAI
import tiktoken
#%%

def chunk_text_by_tokens(text: str, chunk_size=500, overlap=100, model_name="gpt-3.5-turbo") -> list:
    encoding = tiktoken.encoding_for_model(model_name)
    token_ids = encoding.encode(text)

    chunks = []
    start = 0
    while start < len(token_ids):
        end = start + chunk_size
        chunk_ids = token_ids[start:end]
        chunk_text = encoding.decode(chunk_ids)
        chunks.append(chunk_text)
        start += (chunk_size - overlap)
    return chunks
#%%

dotenv.load_dotenv()

pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))

client= OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def load_passages(data_dir="."):
    passages = {}

    for root, dirs, files in os.walk(data_dir):

        for file in files:
            if file.endswith('.md'):
                file_path = os.path.join(root, file)
                relative_path = os.path.relpath(file_path, data_dir)
                
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        full_text = f.read()
                    
                    full_text=full_text.strip()

                    chunked_passages = chunk_text_by_tokens(
                        full_text, 
                        chunk_size=500, 
                        overlap=100, 
                        model_name="gpt-3.5-turbo"
                    )

                    passages[relative_path] = chunked_passages
                        
                except Exception as e:
                    print(f"Error reading file {file_path}: {e}")
    
    print(f"Loaded {len(passages)} passages from {data_dir}")
    return passages

#%%


data=load_passages()

embedding_dict={}

for key, value in data.items():
    embedding_dict[key] = client.embeddings.create(
        model="text-embedding-3-small",
        input=value
    )

#%%

index_name = "showcase-index"

pc.create_index(
    name=index_name,
    dimension=1536,
    metric="cosine",
    spec=ServerlessSpec(
        cloud="aws",
        region="us-east-1",
    )
)

index=pc.Index(index_name)

#%%

vectors=[]

for file_path, file_embeddings in embedding_dict.items():
    file_vectors = [
        {
            "id": f"{file_path}_{i}",  # Create unique ID combining file path and index
            "values": embedding.embedding,
            "metadata": {
                "source_file": file_path,
                "text":data[file_path][i]
            }
        }
        for i, embedding in enumerate(file_embeddings.data)
    ]
    
    # Extend our main vectors list with the vectors from this file
    vectors.extend(file_vectors)

print(f"Created {len(vectors)} total vectors")


#%%
index.upsert(vectors=vectors)


#%%
# just fetch the first vector
A = index.fetch(ids=["Anthropic/pdf-support.md_3"])

