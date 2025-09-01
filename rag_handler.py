<<<<<<< HEAD
import chromadb
import re
from config import CHROMA_PATH, PUBLIC_COLLECTION_NAME, INTERNAL_COLLECTION_NAME
from embedding_handler import find_relevant_chunks
# Import both functions from the chatgpt_handler
from chatgpt_handler import ask_question, rewrite_query

def extract_entity(question: str, entity_list: list) -> str | None:
    """A simple function to find a known entity (like a company name) in the user's question."""
    for entity in entity_list:
        # Use word boundaries (\b) to avoid partial matches (e.g., 'Art' in 'Apartment')
        if re.search(r'\b' + re.escape(entity) + r'\b', question, re.IGNORECASE):
            return entity
    return None


def get_bot_response(question: str, user_role: str, history: list = []) -> str:
    """
    Orchestrates the advanced RAG process using query rewriting and metadata filters.
    """
    client = chromadb.PersistentClient(path=CHROMA_PATH)
    context_chunks = []

    # --- Step 1: Rewrite the query for better retrieval ---
    print("  > Rewriting query based on history...")
    search_query = rewrite_query(question, history)
    print(f"  > Rewritten query: '{search_query}'")

    # --- Step 2: Role-Based and Metadata-Filtered Retrieval ---
    if user_role in ["Internal Team", "Super Admin"]:
        print(" > Searching PUBLIC and INTERNAL knowledge bases...")
        try:
            internal_collection = client.get_collection(name=INTERNAL_COLLECTION_NAME)
            
            # IMPORTANT: This key MUST match the title column of your internal Notion DB.
            # E.g., if your title column is "Client Name", the key is "client_name".
            # If your title column is "Pages", the key is "pages".
            entity_metadata_key = "client_name" # <-- VERIFY THIS KEY

            # Get a list of all possible entities (e.g., company names) from the metadata
            all_metadatas = internal_collection.get(include=["metadatas"])
            entity_list = list(set([
                m[entity_metadata_key] for m in all_metadatas['metadatas'] if entity_metadata_key in m
            ]))
            
            # Try to extract a specific entity from the rewritten query
            entity = extract_entity(search_query, entity_list)
            
            if entity:
                print(f"  > Found entity: '{entity}'. Performing filtered search...")
                # If an entity is mentioned, perform a highly-relevant filtered search
                context_chunks = find_relevant_chunks(
                    internal_collection, 
                    search_query, 
                    top_k=5, 
                    where_filter={entity_metadata_key: entity} # The powerful metadata filter
                )
            else:
                # If no specific entity is mentioned, fall back to a general semantic search
                print("  > No specific entity found. Performing general search...")
                public_collection = client.get_collection(name=PUBLIC_COLLECTION_NAME)
                public_chunks = find_relevant_chunks(public_collection, search_query, top_k=2)
                internal_chunks = find_relevant_chunks(internal_collection, search_query, top_k=2)
                context_chunks = public_chunks + internal_chunks

        except (ValueError, IndexError, KeyError):
            return "Error: One or more knowledge bases are not available or are missing required metadata. Please run the setup script."
    elif user_role == "Platform User":
        print(" > Searching PUBLIC knowledge base...")
        try:
            public_collection = client.get_collection(name=PUBLIC_COLLECTION_NAME)
            # Get a list of all page titles from the public database metadata
            all_metadatas = public_collection.get(include=["metadatas"])
            # The title column for your public DB is "Pages", which becomes "pages"
            entity_list = list(set([m['pages'] for m in all_metadatas['metadatas'] if 'pages' in m]))
            # Try to extract a specific page title from the query
            entity = extract_entity(search_query, entity_list)
            
            if entity:
                print(f"  > Found entity: '{entity}'. Performing filtered search on public DB...")
                context_chunks = find_relevant_chunks(
                    public_collection, 
                    search_query, 
                    top_k=5, 
                    where_filter={"pages": entity} # Use the metadata filter
                )
            else:
                print("  > No specific entity found. Performing general search on public DB...")
                context_chunks = find_relevant_chunks(public_collection, search_query, top_k=3)
                
        except (ValueError, IndexError, KeyError):
            return "Error: The public knowledge base is not available or is missing metadata."
            
    # elif user_role == "Platform User":
    #     print(" > Searching PUBLIC knowledge base...")
    #     try:
    #         public_collection = client.get_collection(name=PUBLIC_COLLECTION_NAME)
    #         context_chunks = find_relevant_chunks(public_collection, search_query, top_k=3)
    #     except ValueError:
    #         return "Error: The public knowledge base is not available. Please contact an administrator."
            
    else:
        return "Error: Invalid user role specified. Access denied."

    # --- Step 3: Generate the Final Answer ---
    if not context_chunks:
        return "I'm sorry, I could not find any relevant information to answer your question."

    context = "\n---\n".join(context_chunks)
    
    # Pass the ORIGINAL question, retrieved context, and history to the LLM
    answer = ask_question(question, context, history)
=======
import chromadb
import re
from config import CHROMA_PATH, PUBLIC_COLLECTION_NAME, INTERNAL_COLLECTION_NAME
from embedding_handler import find_relevant_chunks
# Import both functions from the chatgpt_handler
from chatgpt_handler import ask_question, rewrite_query

def extract_entity(question: str, entity_list: list) -> str | None:
    """A simple function to find a known entity (like a company name) in the user's question."""
    for entity in entity_list:
        # Use word boundaries (\b) to avoid partial matches (e.g., 'Art' in 'Apartment')
        if re.search(r'\b' + re.escape(entity) + r'\b', question, re.IGNORECASE):
            return entity
    return None


def get_bot_response(question: str, user_role: str, history: list = []) -> str:
    """
    Orchestrates the advanced RAG process using query rewriting and metadata filters.
    """
    client = chromadb.PersistentClient(path=CHROMA_PATH)
    context_chunks = []

    # --- Step 1: Rewrite the query for better retrieval ---
    print("  > Rewriting query based on history...")
    search_query = rewrite_query(question, history)
    print(f"  > Rewritten query: '{search_query}'")

    # --- Step 2: Role-Based and Metadata-Filtered Retrieval ---
    if user_role in ["Internal Team", "Super Admin"]:
        print(" > Searching PUBLIC and INTERNAL knowledge bases...")
        try:
            internal_collection = client.get_collection(name=INTERNAL_COLLECTION_NAME)
            
            # IMPORTANT: This key MUST match the title column of your internal Notion DB.
            # E.g., if your title column is "Client Name", the key is "client_name".
            # If your title column is "Pages", the key is "pages".
            entity_metadata_key = "client_name" # <-- VERIFY THIS KEY

            # Get a list of all possible entities (e.g., company names) from the metadata
            all_metadatas = internal_collection.get(include=["metadatas"])
            entity_list = list(set([
                m[entity_metadata_key] for m in all_metadatas['metadatas'] if entity_metadata_key in m
            ]))
            
            # Try to extract a specific entity from the rewritten query
            entity = extract_entity(search_query, entity_list)
            
            if entity:
                print(f"  > Found entity: '{entity}'. Performing filtered search...")
                # If an entity is mentioned, perform a highly-relevant filtered search
                context_chunks = find_relevant_chunks(
                    internal_collection, 
                    search_query, 
                    top_k=5, 
                    where_filter={entity_metadata_key: entity} # The powerful metadata filter
                )
            else:
                # If no specific entity is mentioned, fall back to a general semantic search
                print("  > No specific entity found. Performing general search...")
                public_collection = client.get_collection(name=PUBLIC_COLLECTION_NAME)
                public_chunks = find_relevant_chunks(public_collection, search_query, top_k=2)
                internal_chunks = find_relevant_chunks(internal_collection, search_query, top_k=2)
                context_chunks = public_chunks + internal_chunks

        except (ValueError, IndexError, KeyError):
            return "Error: One or more knowledge bases are not available or are missing required metadata. Please run the setup script."
    elif user_role == "Platform User":
        print(" > Searching PUBLIC knowledge base...")
        try:
            public_collection = client.get_collection(name=PUBLIC_COLLECTION_NAME)
            # Get a list of all page titles from the public database metadata
            all_metadatas = public_collection.get(include=["metadatas"])
            # The title column for your public DB is "Pages", which becomes "pages"
            entity_list = list(set([m['pages'] for m in all_metadatas['metadatas'] if 'pages' in m]))
            # Try to extract a specific page title from the query
            entity = extract_entity(search_query, entity_list)
            
            if entity:
                print(f"  > Found entity: '{entity}'. Performing filtered search on public DB...")
                context_chunks = find_relevant_chunks(
                    public_collection, 
                    search_query, 
                    top_k=5, 
                    where_filter={"pages": entity} # Use the metadata filter
                )
            else:
                print("  > No specific entity found. Performing general search on public DB...")
                context_chunks = find_relevant_chunks(public_collection, search_query, top_k=3)
                
        except (ValueError, IndexError, KeyError):
            return "Error: The public knowledge base is not available or is missing metadata."
            
    # elif user_role == "Platform User":
    #     print(" > Searching PUBLIC knowledge base...")
    #     try:
    #         public_collection = client.get_collection(name=PUBLIC_COLLECTION_NAME)
    #         context_chunks = find_relevant_chunks(public_collection, search_query, top_k=3)
    #     except ValueError:
    #         return "Error: The public knowledge base is not available. Please contact an administrator."
            
    else:
        return "Error: Invalid user role specified. Access denied."

    # --- Step 3: Generate the Final Answer ---
    if not context_chunks:
        return "I'm sorry, I could not find any relevant information to answer your question."

    context = "\n---\n".join(context_chunks)
    
    # Pass the ORIGINAL question, retrieved context, and history to the LLM
    answer = ask_question(question, context, history)
>>>>>>> 0d335ae133ae7c792c457095bddd4a35573e9ea4
    return answer