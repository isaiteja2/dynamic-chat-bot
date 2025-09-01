import os
from openai import OpenAI
from dotenv import load_dotenv
import chromadb
import uuid

# --- Initialization ---
load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Initializes the persistent client that saves data to disk
chroma_client = chromadb.PersistentClient(path="./chroma_db")


def get_embedding(text: str, model="text-embedding-3-small") -> list[float]:
    """Gets the embedding for a given text using OpenAI's API."""
    # Replace newlines, which can sometimes cause issues with embedding models
    text = text.replace("\n", " ")
    response = client.embeddings.create(input=[text], model=model)
    return response.data[0].embedding

def chunk_text(text: str, max_tokens=400) -> list[str]:
    """
    Splits a long text into smaller chunks, ensuring no single chunk is too large.
    This version is robust enough to handle very long, unbroken paragraphs.
    """
    # First, split the text into paragraphs or sections
    paragraphs = text.split("\n\n")
    chunks = []
    
    for paragraph in paragraphs:
        if not paragraph.strip(): # Skip empty paragraphs
            continue
            
        words = paragraph.split()
        
        # If the whole paragraph is smaller than our limit, add it as one chunk
        if len(words) <= max_tokens:
            chunks.append(paragraph.strip())
        else:
            # If the paragraph is too long, split it into smaller pieces
            current_chunk_words = []
            for word in words:
                current_chunk_words.append(word)
                if len(current_chunk_words) >= max_tokens:
                    chunks.append(" ".join(current_chunk_words))
                    current_chunk_words = []
            if current_chunk_words: # Add the last remaining part of the paragraph
                chunks.append(" ".join(current_chunk_words))
                
    return chunks

def setup_chroma_collection(collection_name: str, chunks: list[str], metadatas: list[dict]):
    """
    Creates and populates a persistent ChromaDB collection with documents and their metadata.
    """
    collection = chroma_client.get_or_create_collection(name=collection_name)
    
    print(f"  > Generating embeddings for {len(chunks)} chunks...")
    chunk_embeddings = [get_embedding(chunk) for chunk in chunks]
    chunk_ids = [str(uuid.uuid4()) for _ in chunks]

    # Add the documents along with their structured metadata
    collection.add(
        embeddings=chunk_embeddings,
        documents=chunks,
        metadatas=metadatas,
        ids=chunk_ids
    )
    return collection

def find_relevant_chunks(collection, question: str, top_k=3, where_filter=None):
    """
    Finds relevant chunks by querying the ChromaDB collection.
    Supports an optional 'where' filter for metadata-based searches.
    """
    query_embedding = get_embedding(question)

    query_args = {
        "query_embeddings": [query_embedding],
        "n_results": top_k,
    }
    
    # Add the metadata filter to the query if provided
    if where_filter:
        query_args["where"] = where_filter

    results = collection.query(**query_args)
    
    # The result contains a list of lists of documents. We want the first list.
    return results['documents'][0] if results['documents'] else []