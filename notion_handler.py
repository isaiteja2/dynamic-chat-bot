from notion_client import Client
import os
from dotenv import load_dotenv
import time

# --- Initialization ---
load_dotenv()
notion = Client(auth=os.getenv("NOTION_API_KEY"))


def fetch_all_text_from_database(database_id: str) -> list[dict]:
    """
    Queries a Notion database and extracts text and metadata from each page,
    robustly handling pages with empty properties and creating rich content for embedding.
    """
    all_pages_data = []
    paginated_query = {}

    print(f"Querying Notion database ({database_id}) to get all pages...")
    while True:
        response = notion.databases.query(database_id=database_id, **paginated_query)

        for page in response['results']:
            page_id = page['id']
            metadata = {}
            page_title = "Untitled Page"
            page_properties_text = []

            for prop_name, prop_value in page['properties'].items():
                prop_type = prop_value['type']
                content = None
                
                if prop_type == 'title' and prop_value['title']:
                    content = "".join([t['plain_text'] for t in prop_value['title']])
                    page_title = content if content else "Untitled Page"
                elif prop_type == 'rich_text' and prop_value['rich_text']:
                    content = "".join([t['plain_text'] for t in prop_value['rich_text']])
                elif prop_type == 'select' and prop_value['select']:
                    content = prop_value['select']['name']
                elif prop_type == 'multi_select' and prop_value['multi_select']:
                    content = ", ".join([s['name'] for s in prop_value['multi_select']])
                elif prop_type == 'number' and prop_value['number'] is not None:
                    content = str(prop_value['number'])
                
                if content:
                    metadata_key = prop_name.lower().replace(" ", "_")
                    metadata[metadata_key] = content
                    # Also add the property text to a list for embedding
                    page_properties_text.append(f"{prop_name}: {content}")

            if not metadata:
                metadata["has_no_properties"] = "true"

            print(f"  > Fetching page body for: {page_title}")
            page_body = fetch_all_text_from_page(page_id)
            
            # --- THIS IS THE KEY CHANGE ---
            # Combine the structured properties text AND the page body for a rich context
            properties_summary = "\n".join(page_properties_text)
            content_for_embedding = f"{properties_summary}\n\n{page_body}"
            
            all_pages_data.append({"content": content_for_embedding, "metadata": metadata})

        if not response.get("has_more"):
            break
        paginated_query["start_cursor"] = response.get("next_cursor")
            
    return all_pages_data


def fetch_all_text_from_page(page_id: str) -> str:
    """
    Fetches and combines all text from a single Notion page, including all nested blocks,
    and correctly formats links, embedded files, and child pages.
    """
    def process_rich_text(rich_text_array: list) -> str:
        """Helper to parse rich_text arrays for inline hyperlinks."""
        full_text = ""
        for rt in rich_text_array:
            text_content = rt.get("plain_text", "")
            if rt.get("href"):
                full_text += f"[{text_content}]({rt['href']})"
            else:
                full_text += text_content
        return full_text

    def get_text(block: dict) -> str:
        """Extracts text from a single Notion block."""
        t = ""
        block_type = block.get("type", None)
        if not block_type: return t

        if block_type in ["paragraph", "heading_1", "heading_2", "heading_3", "bulleted_list_item", "numbered_list_item", "toggle", "quote"]:
            rich_text_array = block.get(block_type, {}).get("rich_text", [])
            processed_text = process_rich_text(rich_text_array)
            if "heading_1" in block_type: t = f"# {processed_text}"
            elif "heading_2" in block_type: t = f"## {processed_text}"
            elif "heading_3" in block_type: t = f"### {processed_text}"
            elif "bulleted_list_item" in block_type: t = f"- {processed_text}"
            elif "numbered_list_item" in block_type: t = f"1. {processed_text}"
            elif "quote" in block_type: t = f"> {processed_text}"
            else: t = processed_text
        
        elif block_type == "to_do":
            rich_text_array = block.get("to_do", {}).get("rich_text", [])
            processed_text = process_rich_text(rich_text_array)
            checked = block.get("to_do", {}).get("checked", False)
            t = f"[{'x' if checked else ' '}] {processed_text}"
        
        elif block_type in ["image", "file", "pdf"]:
            file_data = block.get(block_type, {})
            caption_text = process_rich_text(file_data.get("caption", []))
            file_url = file_data.get("external", {}).get("url") or file_data.get("file", {}).get("url")
            if file_url:
                t = f"{block_type.capitalize()} Description: {caption_text}\n{block_type.capitalize()} Source: {file_url}"

        elif block_type == "embed":
            embed_url = block.get("embed", {}).get("url")
            caption_text = process_rich_text(block.get("embed", {}).get("caption", []))
            if embed_url:
                t = f"Embedded Content: {caption_text}\nSource Link: {embed_url}"

        elif block_type == "code":
            rich_text_array = block.get("code", {}).get("rich_text", [])
            t = f"```\n{''.join([rt.get('plain_text', '') for rt in rich_text_array])}\n```"

        return t

    def fetch_blocks_recursively(block_id: str) -> list[str]:
        """Recursively fetches all blocks and their children with proper context."""
        result_text = []
        next_cursor = None
        
        while True:
            time.sleep(0.4) 
            response = notion.blocks.children.list(block_id=block_id, start_cursor=next_cursor)
            
            for block in response.get("results", []):
                block_type = block.get("type")
                text = get_text(block)
                
                if block_type == "child_page":
                    child_page_title = block.get("child_page", {}).get("title", "Untitled Child Page")
                    child_page_content = fetch_all_text_from_page(block["id"])
                    full_child_page_text = f"\n--- Start of Nested Page: {child_page_title} ---\n{child_page_content}\n--- End of Nested Page ---\n"
                    result_text.append(full_child_page_text)
                else:
                    if text:
                        result_text.append(text)
                    if block.get("has_children"):
                        result_text.extend(fetch_blocks_recursively(block["id"]))

            if not response.get("has_more"):
                break
            next_cursor = response.get("next_cursor")
                
        return result_text

    return "\n".join(fetch_blocks_recursively(page_id))