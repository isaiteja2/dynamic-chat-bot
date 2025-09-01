import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def get_answer_from_chatgpt(query, context_chunks):
    system_prompt = (
        "You are a helpful assistant answering questions about the Revolution RE platform. "
        "Use the provided context chunks only. If the answer isn't in the context, say you don’t know."
    )

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": f"Context:\n{''.join(context_chunks)}\n\nQuestion: {query}"}
    ]

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=messages,
        temperature=0.3,
    )
    return response.choices[0].message.content.strip()
