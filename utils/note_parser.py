import re

def parse_classification_output(text: str) -> list:
    qa_list = []
    blocks = text.strip().split("\n[")

    for block in blocks:
        block = block.strip()
        if not block:
            continue

        # 修复开头被 split 掉的 [
        if not block.startswith("["):
            block = "[" + block

        # 分类和问题
        head_match = re.match(r'\[(.*?)\]\s*(.+)', block)
        if not head_match:
            continue
        category, question = head_match.groups()

        # 提取结构化字段
        definition_match = re.search(r"【定义】(.*?)(?=【|$)", block, re.DOTALL)
        example_match = re.search(r"【示例】(.*?)(?=【|$)", block, re.DOTALL)
        answer_match = re.search(r"【回答】(.*?)(?=【|$)", block, re.DOTALL)

        qa_list.append({
            "category": category.strip(),
            "question": question.strip(),
            "definition": definition_match.group(1).strip() if definition_match else "",
            "example": example_match.group(1).strip() if example_match else "",
            "answer": answer_match.group(1).strip() if answer_match else ""
        })

    return qa_list
