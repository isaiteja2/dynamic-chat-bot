import os
from notion_handler import fetch_all_text_from_page
from embedder import generate_embeddings, query_embeddings
from dotenv import load_dotenv

load_dotenv()

NOTION_PAGE_ID = os.getenv("NOTION_PAGE_ID")

def chunk_text(text, max_length=1000):
    import re
    paragraphs = re.split(r'\n\s*\n', text)
    chunks = []
    current_chunk = ""

    for para in paragraphs:
        if len(current_chunk) + len(para) + 2 <= max_length:
            current_chunk += para + "\n\n"
        else:
            chunks.append(current_chunk.strip())
            current_chunk = para + "\n\n"

    if current_chunk:
        chunks.append(current_chunk.strip())

    return chunks

def main():
    print("Loading Notion content...")
    notion_text = fetch_all_text_from_page(NOTION_PAGE_ID)

    if not notion_text.strip():
        print("❌ No content found in Notion page.")
        return

    print("✅ Notion content loaded.")

    chunks = chunk_text(notion_text)
    print(f"✅ Fetched and chunked {len(chunks)} sections.")

    # 🔍 Show chunked content for debugging
    for i, chunk in enumerate(chunks):
        print(f"\n📄 Chunk {i+1}:\n{chunk}\n{'-'*40}")

    print("Generating embeddings...")
    embeddings = generate_embeddings(chunks)

    while True:
        question = input("\nAsk a question (or type 'exit'): ")
        if question.lower() == "exit":
            break

        relevant_context = query_embeddings(question, chunks, embeddings)

        if not relevant_context:
            print("💬 Answer:\nI'm sorry, I couldn’t find anything in the provided Notion content related to your question.")
            continue

        import openai
        openai.api_key = os.getenv("OPENAI_API_KEY")

        system_prompt = "Answer the question using only the context provided. If the answer is not in the context, say you don’t know."
        user_prompt = f"Context:\n{relevant_context}\n\nQuestion: {question}"

        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
        )

        print("\n💬 Answer:\n" + response.choices[0].message.content.strip())

if __name__ == "__main__":
    main()
