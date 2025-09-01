import os
from openai import OpenAI
from dotenv import load_dotenv

# --- Initialization ---
load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def rewrite_query(question: str, history: list) -> str:
    """
    Uses a fast LLM to rewrite a follow-up question into a standalone query
    based on the conversation history.
    """
    if not history:
        return question

    # Format the history for the prompt
    history_text = "\n".join([f"{msg['role']}: {msg['content']}" for msg in history])
    
    prompt = f"""
    Based on the following chat history, rewrite the user's final question to be a complete, self-contained question that can be understood without the preceding context.
    If the question is already self-contained, simply return it as is.

    Chat History:
    ---
    {history_text}
    ---

    Final Question: "{question}"

    Rewritten Question:
    """
    
    try:
        response = client.chat.completions.create(
            # Use a fast and cheap model for this simple rewriting task
            model="gpt-4o-mini", 
            messages=[{"role": "user", "content": prompt}],
            temperature=0.0 # Be very deterministic
        )
        rewritten = response.choices[0].message.content.strip()
        # Remove quotes if the model adds them
        return rewritten.strip('"')
    except Exception as e:
        print(f"Error during query rewriting: {e}")
        # Fallback to the original question on error
        return question


def ask_question(question: str, context: str, history: list = []):
    """
    Sends the question, retrieved context, and conversation history to the 
    primary OpenAI API to generate a final, conversational answer.
    """
    # Build the list of messages for the API call, starting with the history
    messages = []
    if history:
        messages.extend(history)

    # Add the final user prompt, which includes the retrieved context and the latest question
    final_prompt = f"""
    You are a helpful assistant for a knowledge base. Your task is to answer the user's question based exclusively on the context provided.

    INSTRUCTIONS:
    1. Read the context carefully and consider the preceding conversation history to maintain a natural conversational flow.
    2. Formulate an answer to the user's latest question using only the information found in the context. Do not use any outside knowledge.
    3. If the context includes a hyperlink, image, or file relevant to the answer, you must cite it at the end of your response.
    4. If the context does not contain the answer, simply state: "I'm sorry, I could not find an answer to that question in the available documents."

    CONTEXT:
    ---
    {context}
    ---

    QUESTION: {question}
    """
    messages.append({"role": "user", "content": final_prompt})
    
    try:
        response = client.chat.completions.create(
            # Use a powerful model for the final answer generation
            model="gpt-4o",
            messages=messages,
            temperature=0.2,
        )
        return response.choices[0].message.content.strip()

    except Exception as e:
        print(f"An error occurred with the OpenAI API: {e}")
        return "Sorry, I encountered an error while trying to generate a response."