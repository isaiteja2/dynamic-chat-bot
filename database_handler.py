import sqlite3
import datetime
from config import LOG_DATABASE_PATH

def init_db():
    """
    Initializes the logging database and creates the necessary tables 
    if they don't already exist.
    """
    conn = sqlite3.connect(LOG_DATABASE_PATH)
    cursor = conn.cursor()
    
    # Create a table to store each conversation turn
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS conversations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            user_role TEXT NOT NULL,
            question TEXT NOT NULL,
            answer TEXT NOT NULL
        )
    """)
    
    # Create a table to store feedback linked to a conversation
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS feedback (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            conversation_id INTEGER NOT NULL,
            feedback_type TEXT NOT NULL, -- 'up', 'down', or 'text'
            feedback_text TEXT,
            FOREIGN KEY (conversation_id) REFERENCES conversations (id)
        )
    """)
    
    conn.commit()
    conn.close()

def log_conversation(user_role, question, answer):
    """
    Logs a question-and-answer pair to the database and returns the unique
    ID for that conversation entry.
    """
    conn = sqlite3.connect(LOG_DATABASE_PATH)
    cursor = conn.cursor()
    
    cursor.execute(
        "INSERT INTO conversations (user_role, question, answer) VALUES (?, ?, ?)",
        (user_role, question, answer)
    )
    
    # Get the ID of the row we just inserted
    conversation_id = cursor.lastrowid
    
    conn.commit()
    conn.close()
    
    # Return the ID so we can link feedback to it
    return conversation_id

def log_feedback(conversation_id, feedback_type, feedback_text=""):
    """Logs user feedback for a specific conversation ID."""
    conn = sqlite3.connect(LOG_DATABASE_PATH)
    cursor = conn.cursor()
    
    cursor.execute(
        "INSERT INTO feedback (conversation_id, feedback_type, feedback_text) VALUES (?, ?, ?)",
        (conversation_id, feedback_type, feedback_text)
    )
    
    conn.commit()
    conn.close()
    
    print(f"Feedback logged for conversation {conversation_id}")