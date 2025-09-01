# import os
# from notion_handler import fetch_all_text_from_page
# from embedding_handler import chunk_text, setup_chroma_collection, find_relevant_chunks
# from chatgpt_handler import ask_question
# import chromadb

# def main():
#     # --- Initialize a temporary, in-memory ChromaDB client ---
#     # This database will only exist while the script is running.
#     chroma_client = chromadb.Client()

#     # --- Initial Data Loading and Indexing ---
#     # Get Notion page ID from environment variables or user input
#     page_id = os.getenv("NOTION_PAGE_ID")
#     if not page_id:
#         page_id = input("Enter the Notion Page ID: ")

#     print("📄 Fetching page content...")
#     text = fetch_all_text_from_page(page_id)

#     print("✂️ Chunking content...")
#     chunks = chunk_text(text)

#     print("🧠 Creating temporary vector database in memory...")
#     # Create a unique name for the collection for this session
#     collection_name = "notion_page_temp_collection"
#     # The setup function will create and populate our temporary database
#     collection = setup_chroma_collection(collection_name, chunks, chroma_client)

#     # --- Main Chat Loop ---
#     print("\n✅ Bot is ready! Type your question, or type 'exit' to quit.\n")

#     while True:
#         question = input(">> ")
#         if question.lower() in ["exit", "quit"]:
#             print("👋 Goodbye!")
#             break

#         print("🔍 Finding relevant context from ChromaDB...")
#         # Use the find_relevant_chunks function that queries the collection
#         relevant_chunks = find_relevant_chunks(collection, question)
#         context = "\n".join(relevant_chunks)

#         print("🤖 Answering...\n")
#         answer = ask_question(question, context)
#         print(f"💬 {answer}\n")

# if __name__ == "__main__":
#     main()

# Code without refreshing data
# import os
# import chromadb
# # Import the specific error type from chromadb
# from chromadb.errors import NotFoundError
# from notion_handler import fetch_all_text_from_database
# from embedding_handler import chunk_text, setup_chroma_collection, find_relevant_chunks
# from chatgpt_handler import ask_question

# # Initialize a client to check for the persistent database
# chroma_client = chromadb.PersistentClient(path="./chroma_db")

# def main():
#     # --- Database and Collection Setup ---
#     database_id = os.getenv("NOTION_DATABASE_ID")
#     if not database_id:
#         raise ValueError("NOTION_DATABASE_ID not found in .env file. Please add it.")

#     collection_name = f"notion_db_{database_id.replace('-', '')}"

#     try:
#         # Check if the knowledge base has already been indexed and stored on disk
#         collection = chroma_client.get_collection(name=collection_name)
#         print(f"✅ Connected to existing knowledge base: '{collection_name}'")
#     except NotFoundError: # <--- CORRECTED EXCEPTION
#         # If the collection doesn't exist, this is the first run.
#         # This block will now execute correctly.
#         print(f"Knowledge base '{collection_name}' not found. Starting one-time setup...")

#         print(f"📄 Fetching all pages from Notion database: {database_id}")
#         full_text = fetch_all_text_from_database(database_id)
        
#         print("✂️ Chunking all content...")
#         chunks = chunk_text(full_text)

#         print(f"🧠 Indexing all {len(chunks)} chunks in ChromaDB. This will take a while...")
#         collection = setup_chroma_collection(collection_name, chunks)
#         print("✅ Indexing complete!")

#     # --- Main Chat Loop ---
#     print("\n✅ Bot is ready! Ask anything about your Notion workspace. Type 'exit' to quit.\n")
    
#     while True:
#         question = input(">> ")
#         if question.lower() in ["exit", "quit"]:
#             print("👋 Goodbye!")
#             break

#         relevant_chunks = find_relevant_chunks(collection, question)
#         context = "\n".join(relevant_chunks)
#         answer = ask_question(question, context)
#         print(f"💬 {answer}\n")

# if __name__ == "__main__":
#     main()

# Code with Refresh functionality
import os
import chromadb
# Import the specific error type from chromadb
from chromadb.errors import NotFoundError
from notion_handler import fetch_all_text_from_database
from embedding_handler import chunk_text, setup_chroma_collection, find_relevant_chunks
from chatgpt_handler import ask_question

# Initialize a client to manage the persistent database
chroma_client = chromadb.PersistentClient(path="./chroma_db")

def main():
    # --- STEP 1: INITIAL SETUP ---
    # This block runs only once when the script starts. It ensures the
    # collection is ready before the user can ask questions.
    database_id = os.getenv("NOTION_DATABASE_ID")
    if not database_id:
        raise ValueError("NOTION_DATABASE_ID not found in .env file. Please add it.")

    collection_name = f"notion_db_{database_id.replace('-', '')}"

    try:
        # Connect to the existing collection on disk
        collection = chroma_client.get_collection(name=collection_name)
        # print(f"✅ Connected to existing knowledge base: '{collection_name}'")
    except NotFoundError:
        # If it doesn't exist, create it for the first time
        print(f"Knowledge base '{collection_name}' not found. Starting one-time setup...")
        full_text = fetch_all_text_from_database(database_id)
        chunks = chunk_text(full_text)
        print(f"🧠 Indexing all {len(chunks)} chunks. This will take a while...")
        collection = setup_chroma_collection(collection_name, chunks)
        print("✅ Indexing complete!")

    # --- STEP 2: MAIN CHAT & COMMAND LOOP ---
    # This loop handles all user interaction after the initial setup.
    print("\n✅ Bot is ready! Type 'refresh' to update, or 'exit' to quit.\n")
    
    while True:
        question = input(">> ")

        if question.lower() in ['exit','quit']:
            print("👋 Goodbye!")
            break
        
        # --- The 'refresh' logic is now inside the main loop ---
        if question.lower() == 'refresh':
            print("🔄 Refreshing knowledge base...")
            
            # Delete the old collection to ensure a clean slate
            chroma_client.delete_collection(name=collection_name)
            
            # Re-run the entire setup process
            full_text = fetch_all_text_from_database(database_id)
            chunks = chunk_text(full_text)
            print(f"🧠 Re-indexing all {len(chunks)} chunks...")
            # Re-assign the collection variable to the new, updated collection
            collection = setup_chroma_collection(collection_name, chunks)
            print("✅ Knowledge base refreshed successfully!\n")
            continue # Skip the rest of the loop and wait for the next question
        
        # --- Standard Question-Answering Logic ---
        print("🔍 Finding relevant context...")
        relevant_chunks = find_relevant_chunks(collection, question)
        context = "\n".join(relevant_chunks)
        
        print("🤖 Answering...\n")
        answer = ask_question(question, context)
        print(f"💬 {answer}\n")
        print("Type 'quit' or 'exit' to end the session or reach out to us at support@revolutionre.com.\n")
if __name__ == "__main__":
    main()