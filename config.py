import os
from dotenv import load_dotenv

# Load variables from your .env file
load_dotenv()

# --- ChromaDB Configuration ---
# Names for your two separate knowledge base collections in ChromaDB
PUBLIC_COLLECTION_NAME = "notion_public_kb"
INTERNAL_COLLECTION_NAME = "notion_internal_kb"

# Path for the persistent ChromaDB data folder
CHROMA_PATH = "./chroma_db"

# --- Logging Database Configuration ---
# Path for the SQLite logging database file
LOG_DATABASE_PATH = "logs.sqlite3"

# --- Security Configuration ---
# Passwords for elevated access roles, loaded from your .env file
INTERNAL_ACCESS_PASSWORD = os.getenv("INTERNAL_ACCESS_PASSWORD")
SUPER_ADMIN_PASSWORD = os.getenv("SUPER_ADMIN_PASSWORD")
