from dotenv import load_dotenv
import os

# load_dotenv(dotenv_path=".env")  # Load from .env
# print(os.getenv("NOTION_API_KEY"))  # Should print your key, not None

load_dotenv()
print("DEBUG: API KEY =", os.getenv("NOTION_API_KEY"))
print("DEBUG: PAGE ID =", os.getenv("NOTION_PAGE_ID"))


'''
tools = [
        {
            "type": "function",
            "function": {
                "name": "query_knowledge_base",
                "description": "Use this function to answer questions about internal company documents, guides, and meeting notes from the Notion knowledge base.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "question": {
                            "type": "string",
                            "description": "The specific question to ask the knowledge base."
                        }
                    },
                    "required": ["question"]
                }
            }
        }
    ]
'''