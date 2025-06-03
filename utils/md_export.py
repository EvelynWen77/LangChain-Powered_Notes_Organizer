import os
from datetime import datetime
from utils.note_loader import load_all_note_metadata_with_id

EXPORT_DIR = "./data/markdown_exports"
os.makedirs(EXPORT_DIR, exist_ok=True)

def export_to_markdown(summary_text: str, raw_note: str, category: str,
                       company: str, round_num: str, date: str, position: str) -> str:
    filename = f"{company}_{position}_{date}.md".replace(" ", "_")
    path = os.path.join(EXPORT_DIR, filename)
    with open(path, "w", encoding="utf-8") as f:
        f.write(f"# Interview Note\n\n")
        f.write(f"**Company**: {company}  \n")
        f.write(f"**Position**: {position}  \n")
        f.write(f"**Date**: {date}  \n")
        f.write(f"**Round**: {round_num}  \n")
        f.write(f"**Category**: {category}  \n\n")
        f.write("## 🧾 Structured Summary\n\n")
        f.write(summary_text.strip() + "\n\n")
        f.write("---\n\n")
        f.write("## 📝 Raw Interview Note\n\n")
        f.write(raw_note.strip())
    return path

def export_all_to_markdown() -> str:
    rows = load_all_note_metadata_with_id()
    if not rows:
        return "No notes found to export."

    md_content = "# 📦 All Interview Questions (Structured)\n\n"

    for row in rows:
        (
            note_id,
            company,
            position,
            date,
            round_num,
            category,
            question,
            definition,
            example,
            answer
        ) = row

        md_content += f"## {company} - {position} ({date})\n"
        md_content += f"- **Round**: {round_num}  \n"
        md_content += f"- **Category**: {category}  \n"
        md_content += f"- **Question**: {question}  \n\n"
        if definition:
            md_content += f"**Definition**: {definition}\n\n"
        if example:
            md_content += f"**Example**: {example}\n\n"
        if answer:
            md_content += f"**Answer**: {answer}\n\n"
        md_content += "---\n\n"

    filename = datetime.now().strftime("all_questions_structured_%Y%m%d_%H%M%S.md")
    path = os.path.join(EXPORT_DIR, filename)
    with open(path, "w", encoding="utf-8") as f:
        f.write(md_content)

    return path

def qa_list_to_markdown(qa_list: list) -> str:
    blocks = []
    for item in qa_list:
        block = f"[{item['category']}] {item['question']}\n\n"
        block += f"- **Definition**: {item.get('definition', '').strip() or '（无）'}\n"
        block += f"- **Example**: {item.get('example', '').strip() or '（无）'}\n"
        block += f"- **Answer**: {item.get('answer', '').strip() or '（无）'}\n"
        blocks.append(block)
    return "\n---\n\n".join(blocks)
