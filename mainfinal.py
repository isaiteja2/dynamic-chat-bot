import os
import getpass # To securely hide password input
from rag_handler import get_bot_response
from config import INTERNAL_ACCESS_PASSWORD, SUPER_ADMIN_PASSWORD
# We can import and run the setup script's main function directly
import setup as knowledge_base_setup

def main():
    """A command-line interface to test the full RAG bot functionality."""
    
    user_role = "Platform User" # Default role
    conversation_history = []
    
    print("--- RAG Bot CLI Tester ---")
    print("Commands: Type 'role' to switch, 'refresh' to update KB, 'clear' to reset history, 'exit' to quit.")
    print(f"Starting as: {user_role}")
    
    while True:
        prompt = input(f"[{user_role}] >> ")

        # --- Command Handling ---
        if prompt.lower() in ['exit','bye']:
            print("Feel free to get back anytime. Bye for now!")
            break

        if prompt.lower() == 'clear':
            conversation_history = []
            print("✨ Conversation history cleared.")
            continue

        if prompt.lower() == 'role':
            print("\nSelect a new role:")
            print("  [1] Platform User")
            print("  [2] Internal Team")
            print("  [3] Super Admin")
            choice = input("Enter number: ")
            
            if choice == '1':
                user_role = "Platform User"
                print(f"Switched to: {user_role}")
            elif choice == '2':
                password = getpass.getpass("Enter Internal Password: ")
                if password == INTERNAL_ACCESS_PASSWORD:
                    user_role = "Internal Team"
                    print("✅ Authenticated as Internal Team.")
                else:
                    print("❌ Incorrect password.")
            elif choice == '3':
                password = getpass.getpass("Enter Super Admin Password: ")
                if password == SUPER_ADMIN_PASSWORD:
                    user_role = "Super Admin"
                    print("✅ Authenticated as Super Admin.")
                else:
                    print("❌ Incorrect password.")
            else:
                print("Invalid choice.")
            continue

        if prompt.lower() == 'refresh':
            if user_role == 'Super Admin':
                print("🔄 Refreshing knowledge base...")
                # Call the main function from your setup.py script
                knowledge_base_setup.main()
            else:
                print("❌ Permission Denied. Only 'Super Admin' can refresh.")
            continue

        # --- Standard Question-Answering ---
        print("Thinking...")
        conversation_history.append({"role": "user", "content": prompt})
        recent_history = conversation_history[-4:]

        answer = get_bot_response(prompt, user_role, history=recent_history)
        failure_message = "I'm sorry, I could not find an answer to that question in the available documents."
        if failure_message not in answer:
            conversation_history.append({"role": "assistant", "content": answer})
        # conversation_history.append({"role": "assistant", "content": answer})
        print(f"\n Answer:\n{answer}\n")


if __name__ == "__main__":
    main()
