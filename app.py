<<<<<<< HEAD
import streamlit as st
import os
from rag_handler import get_bot_response
from database_handler import init_db, log_conversation, log_feedback
from config import INTERNAL_ACCESS_PASSWORD, SUPER_ADMIN_PASSWORD
import setup as knowledge_base_setup

# --- Page Configuration ---
st.set_page_config(page_title="Corporate Knowledge Bot", layout="wide")
st.title("🤖 Corporate Knowledge Bot")

# --- Initialize Databases ---
# This ensures the logging database and tables are created on the first run
init_db() 

# --- Session State Initialization ---
# This dictionary stores the entire chat history for the current session
if "messages" not in st.session_state:
    st.session_state.messages = []
# This tracks the user's verified role (defaults to the most restrictive)
if "user_role" not in st.session_state:
    st.session_state.user_role = "Platform User"
# This stores the ID of the last conversation turn for linking feedback
if "current_conversation_id" not in st.session_state:
    st.session_state.current_conversation_id = None

# --- Sidebar for Authentication and Role Selection ---
with st.sidebar:
    st.header("Access Control")
    
    role_choice = st.radio(
        "Select Your Role:",
        ("Platform User", "Internal Team", "Super Admin"),
        index=0 # Default to "Platform User"
    )

    # --- Authentication Logic ---
    if role_choice == "Platform User":
        st.session_state.user_role = "Platform User"

    elif role_choice == "Internal Team":
        password_input = st.text_input("Enter Internal Password:", type="password", key="internal_pass")
        if password_input == INTERNAL_ACCESS_PASSWORD:
            st.session_state.user_role = "Internal Team"
        elif password_input:
            st.session_state.user_role = "Platform User"
            st.error("Incorrect password. Reverting to Platform User role.")

    elif role_choice == "Super Admin":
        password_input = st.text_input("Enter Admin Password:", type="password", key="admin_pass")
        if password_input == SUPER_ADMIN_PASSWORD:
            st.session_state.user_role = "Super Admin"
        elif password_input:
            st.session_state.user_role = "Platform User"
            st.error("Incorrect password. Reverting to Platform User role.")
    
    st.info(f"**Current Access Level:** `{st.session_state.user_role}`")

# --- Main Chat Interface ---
# Display existing messages from session history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Handle new user input
if prompt := st.chat_input("Ask a question..."):
    # Add user message to chat history and display it
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Get and display bot response
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            # --- Command Handling for Super Admin ---
            if prompt.lower() == "refresh" and st.session_state.user_role == "Super Admin":
                with st.status("🔄 Refreshing knowledge base in the background...", expanded=True) as status:
                    knowledge_base_setup.main()
                    status.update(label="✅ Knowledge base refreshed successfully!", state="complete")
                response = "The knowledge base has been updated."
            else:
                # --- Standard RAG Logic ---
                recent_history = st.session_state.messages[-4:]
                response = get_bot_response(prompt, st.session_state.user_role, history=recent_history)
                failure_message = "I'm sorry, I could not find an answer to that question in the available documents."
                if failure_message not in response:
                    st.session_state.messages.append({"role": "assistant", "content": response})
            st.markdown(response)
            
            # Log the conversation and store its ID for feedback
            convo_id = log_conversation(st.session_state.user_role, prompt, response)
            st.session_state.current_conversation_id = convo_id

    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": response})

    # --- Feedback Mechanism ---
    if st.session_state.current_conversation_id:
        convo_id = st.session_state.current_conversation_id
        feedback_key_prefix = f"feedback_{convo_id}"
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("👍 Good Answer", key=f"{feedback_key_prefix}_up"):
                log_feedback(convo_id, "up")
                st.toast("Thanks for your feedback!")
        with col2:
            if st.button("👎 Bad Answer", key=f"{feedback_key_prefix}_down"):
                log_feedback(convo_id, "down")
                st.toast("Thanks for your feedback! Your input helps us improve.")
                
        feedback_text = st.text_input(
            "Provide additional feedback (optional) and press Enter", 
            key=f"{feedback_key_prefix}_text"
        )
        if feedback_text:
            log_feedback(convo_id, "text", feedback_text)
=======
import streamlit as st
import os
from rag_handler import get_bot_response
from database_handler import init_db, log_conversation, log_feedback
from config import INTERNAL_ACCESS_PASSWORD, SUPER_ADMIN_PASSWORD
import setup as knowledge_base_setup

# --- Page Configuration ---
st.set_page_config(page_title="Corporate Knowledge Bot", layout="wide")
st.title("🤖 Corporate Knowledge Bot")

# --- Initialize Databases ---
# This ensures the logging database and tables are created on the first run
init_db() 

# --- Session State Initialization ---
# This dictionary stores the entire chat history for the current session
if "messages" not in st.session_state:
    st.session_state.messages = []
# This tracks the user's verified role (defaults to the most restrictive)
if "user_role" not in st.session_state:
    st.session_state.user_role = "Platform User"
# This stores the ID of the last conversation turn for linking feedback
if "current_conversation_id" not in st.session_state:
    st.session_state.current_conversation_id = None

# --- Sidebar for Authentication and Role Selection ---
with st.sidebar:
    st.header("Access Control")
    
    role_choice = st.radio(
        "Select Your Role:",
        ("Platform User", "Internal Team", "Super Admin"),
        index=0 # Default to "Platform User"
    )

    # --- Authentication Logic ---
    if role_choice == "Platform User":
        st.session_state.user_role = "Platform User"

    elif role_choice == "Internal Team":
        password_input = st.text_input("Enter Internal Password:", type="password", key="internal_pass")
        if password_input == INTERNAL_ACCESS_PASSWORD:
            st.session_state.user_role = "Internal Team"
        elif password_input:
            st.session_state.user_role = "Platform User"
            st.error("Incorrect password. Reverting to Platform User role.")

    elif role_choice == "Super Admin":
        password_input = st.text_input("Enter Admin Password:", type="password", key="admin_pass")
        if password_input == SUPER_ADMIN_PASSWORD:
            st.session_state.user_role = "Super Admin"
        elif password_input:
            st.session_state.user_role = "Platform User"
            st.error("Incorrect password. Reverting to Platform User role.")
    
    st.info(f"**Current Access Level:** `{st.session_state.user_role}`")

# --- Main Chat Interface ---
# Display existing messages from session history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Handle new user input
if prompt := st.chat_input("Ask a question..."):
    # Add user message to chat history and display it
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Get and display bot response
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            # --- Command Handling for Super Admin ---
            if prompt.lower() == "refresh" and st.session_state.user_role == "Super Admin":
                with st.status("🔄 Refreshing knowledge base in the background...", expanded=True) as status:
                    knowledge_base_setup.main()
                    status.update(label="✅ Knowledge base refreshed successfully!", state="complete")
                response = "The knowledge base has been updated."
            else:
                # --- Standard RAG Logic ---
                recent_history = st.session_state.messages[-4:]
                response = get_bot_response(prompt, st.session_state.user_role, history=recent_history)
                failure_message = "I'm sorry, I could not find an answer to that question in the available documents."
                if failure_message not in response:
                    st.session_state.messages.append({"role": "assistant", "content": response})
            st.markdown(response)
            
            # Log the conversation and store its ID for feedback
            convo_id = log_conversation(st.session_state.user_role, prompt, response)
            st.session_state.current_conversation_id = convo_id

    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": response})

    # --- Feedback Mechanism ---
    if st.session_state.current_conversation_id:
        convo_id = st.session_state.current_conversation_id
        feedback_key_prefix = f"feedback_{convo_id}"
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("👍 Good Answer", key=f"{feedback_key_prefix}_up"):
                log_feedback(convo_id, "up")
                st.toast("Thanks for your feedback!")
        with col2:
            if st.button("👎 Bad Answer", key=f"{feedback_key_prefix}_down"):
                log_feedback(convo_id, "down")
                st.toast("Thanks for your feedback! Your input helps us improve.")
                
        feedback_text = st.text_input(
            "Provide additional feedback (optional) and press Enter", 
            key=f"{feedback_key_prefix}_text"
        )
        if feedback_text:
            log_feedback(convo_id, "text", feedback_text)
>>>>>>> 0d335ae133ae7c792c457095bddd4a35573e9ea4
            st.toast("Detailed feedback submitted. Thank you!")