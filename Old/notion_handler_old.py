import os
from notion_client import Client
from dotenv import load_dotenv

load_dotenv()
notion = Client(auth=os.getenv("NOTION_TOKEN"))

def retrieve_block_text(block):
    type_ = block["type"]
    text_items = block[type_].get("text", []) if type_ in block else []

    text = "".join(t.get("plain_text", "") for t in text_items)

    if type_ == "heading_1":
        return "# " + text
    elif type_ == "heading_2":
        return "## " + text
    elif type_ == "heading_3":
        return "### " + text
    elif type_ == "bulleted_list_item":
        return "- " + text
    elif type_ == "numbered_list_item":
        return "1. " + text
    elif type_ == "toggle":
        return "▶ " + text
    elif type_ == "paragraph":
        return text
    elif type_ == "quote":
        return f"> {text}"
    elif type_ == "code":
        return f"```\n{text}\n```"
    elif type_ == "callout":
        return "💬 " + text
    else:
        print(f"⚠️ Skipped unsupported block type: {type_}")
        return None

def fetch_all_text_from_page(page_id):
    def fetch_block_text_recursive(block_id, depth=0):
        texts = []
        try:
            blocks = notion.blocks.children.list(block_id, page_size=100)["results"]
        except Exception as e:
            print(f"❌ Error fetching children for block {block_id}: {e}")
            return texts

        for block in blocks:
            block_type = block["type"]

            # Handle known textual blocks
            text = retrieve_block_text(block)
            if text:
                texts.append("    " * depth + text)

            # Handle nested pages
            if block_type == "child_page":
                page_title = block["child_page"].get("title", "Untitled Page")
                texts.append("    " * depth + f"# Page: {page_title}")
                texts.extend(fetch_block_text_recursive(block["id"], depth + 1))

            # Handle synced blocks (not guaranteed to contain children)
            elif block_type == "synced_block" and block.get("has_children"):
                texts.append("    " * depth + "## Synced Block")
                texts.extend(fetch_block_text_recursive(block["id"], depth + 1))

            elif block.get("has_children"):
                texts.extend(fetch_block_text_recursive(block["id"], depth + 1))

        return texts
