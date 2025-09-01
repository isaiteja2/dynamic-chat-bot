<<<<<<< HEAD
import os
import chromadb
from chromadb.errors import NotFoundError
from notion_handler import fetch_all_text_from_database
from embedding_handler import chunk_text, setup_chroma_collection
from config import CHROMA_PATH, PUBLIC_COLLECTION_NAME, INTERNAL_COLLECTION_NAME

def main():
    """
    Builds or rebuilds the persistent ChromaDB vector stores from Notion.
    """
    print("--- 🧠 Starting Knowledge Base Setup ---")
    
    client = chromadb.PersistentClient(path=CHROMA_PATH)
    
    # --- 1. Setup Public Knowledge Base ---
    public_db_id = os.getenv("NOTION_PUBLIC_DB_ID")
    if public_db_id:
        print(f"\n[1/2] Setting up PUBLIC knowledge base from DB: {public_db_id}")
        
        print("  > Deleting old public collection if it exists...")
        try:
            client.delete_collection(name=PUBLIC_COLLECTION_NAME)
            print("  > Old public collection deleted.")
        except (ValueError, NotFoundError):
        # except (ValueError):
            print("  > No old public collection to delete, creating anew.")
            
        print("  > Fetching all pages and their metadata from Notion...")
        pages_data = fetch_all_text_from_database(public_db_id)
        
        all_chunks = []
        all_metadatas = []
        
        for page in pages_data:
            page_content = page['content']
            page_metadata = page['metadata']
            chunks_for_page = chunk_text(page_content)
            all_chunks.extend(chunks_for_page)
            all_metadatas.extend([page_metadata] * len(chunks_for_page))

        print(f"  > Indexing {len(all_chunks)} chunks for the public collection...")
        setup_chroma_collection(PUBLIC_COLLECTION_NAME, all_chunks, all_metadatas)
        
        print("✅ Public knowledge base setup complete.")
    else:
        print("⚠️ NOTION_PUBLIC_DB_ID not found in .env, skipping public KB setup.")

    # --- 2. Setup Internal Knowledge Base ---
    internal_db_id = os.getenv("NOTION_INTERNAL_DB_ID")
    if internal_db_id:
        print(f"\n[2/2] Setting up INTERNAL knowledge base from DB: {internal_db_id}")
        
        print("  > Deleting old internal collection if it exists...")
        try:
            client.delete_collection(name=INTERNAL_COLLECTION_NAME)
            print("  > Old internal collection deleted.")
        except (ValueError, NotFoundError):
        # except (ValueError):
            print("  > No old internal collection to delete, creating anew.")
            
        print("  > Fetching all pages and their metadata from Notion...")
        pages_data = fetch_all_text_from_database(internal_db_id)

        all_chunks = []
        all_metadatas = []

        for page in pages_data:
            page_content = page['content']
            page_metadata = page['metadata']
            chunks_for_page = chunk_text(page_content)
            all_chunks.extend(chunks_for_page)
            all_metadatas.extend([page_metadata] * len(chunks_for_page))
        
        print(f"  > Indexing {len(all_chunks)} chunks for the internal collection...")
        setup_chroma_collection(INTERNAL_COLLECTION_NAME, all_chunks, all_metadatas)
        
        print("✅ Internal knowledge base setup complete.")
    else:
        print("⚠️ NOTION_INTERNAL_DB_ID not found in .env, skipping internal KB setup.")

    print("\n--- All setups complete! ---")

if __name__ == "__main__":
    main()
=======
import os
import chromadb
# from chromadb.errors import NotFoundError
from notion_handler import fetch_all_text_from_database
from embedding_handler import chunk_text, setup_chroma_collection
from config import CHROMA_PATH, PUBLIC_COLLECTION_NAME, INTERNAL_COLLECTION_NAME

def main():
    """
    Builds or rebuilds the persistent ChromaDB vector stores from Notion.
    """
    print("--- 🧠 Starting Knowledge Base Setup ---")
    
    client = chromadb.PersistentClient(path=CHROMA_PATH)
    
    # --- 1. Setup Public Knowledge Base ---
    public_db_id = os.getenv("NOTION_PUBLIC_DB_ID")
    if public_db_id:
        print(f"\n[1/2] Setting up PUBLIC knowledge base from DB: {public_db_id}")
        
        print("  > Deleting old public collection if it exists...")
        try:
            client.delete_collection(name=PUBLIC_COLLECTION_NAME)
            print("  > Old public collection deleted.")
        # except (ValueError, NotFoundError):
        except (ValueError):
            print("  > No old public collection to delete, creating anew.")
            
        print("  > Fetching all pages and their metadata from Notion...")
        pages_data = fetch_all_text_from_database(public_db_id)
        
        all_chunks = []
        all_metadatas = []
        
        for page in pages_data:
            page_content = page['content']
            page_metadata = page['metadata']
            chunks_for_page = chunk_text(page_content)
            all_chunks.extend(chunks_for_page)
            all_metadatas.extend([page_metadata] * len(chunks_for_page))

        print(f"  > Indexing {len(all_chunks)} chunks for the public collection...")
        setup_chroma_collection(PUBLIC_COLLECTION_NAME, all_chunks, all_metadatas)
        
        print("✅ Public knowledge base setup complete.")
    else:
        print("⚠️ NOTION_PUBLIC_DB_ID not found in .env, skipping public KB setup.")

    # --- 2. Setup Internal Knowledge Base ---
    internal_db_id = os.getenv("NOTION_INTERNAL_DB_ID")
    if internal_db_id:
        print(f"\n[2/2] Setting up INTERNAL knowledge base from DB: {internal_db_id}")
        
        print("  > Deleting old internal collection if it exists...")
        try:
            client.delete_collection(name=INTERNAL_COLLECTION_NAME)
            print("  > Old internal collection deleted.")
        # except (ValueError, NotFoundError):
        except (ValueError):
            print("  > No old internal collection to delete, creating anew.")
            
        print("  > Fetching all pages and their metadata from Notion...")
        pages_data = fetch_all_text_from_database(internal_db_id)

        all_chunks = []
        all_metadatas = []

        for page in pages_data:
            page_content = page['content']
            page_metadata = page['metadata']
            chunks_for_page = chunk_text(page_content)
            all_chunks.extend(chunks_for_page)
            all_metadatas.extend([page_metadata] * len(chunks_for_page))
        
        print(f"  > Indexing {len(all_chunks)} chunks for the internal collection...")
        setup_chroma_collection(INTERNAL_COLLECTION_NAME, all_chunks, all_metadatas)
        
        print("✅ Internal knowledge base setup complete.")
    else:
        print("⚠️ NOTION_INTERNAL_DB_ID not found in .env, skipping internal KB setup.")

    print("\n--- All setups complete! ---")

if __name__ == "__main__":
    main()
>>>>>>> 0d335ae133ae7c792c457095bddd4a35573e9ea4
