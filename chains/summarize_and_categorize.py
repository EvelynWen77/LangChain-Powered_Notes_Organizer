from langchain.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from langchain.chains import LLMChain
import re

def get_summarize_chain():
    prompt = PromptTemplate(
        input_variables=["note"],
        template="""
你是一个面试笔记助手，请完成以下任务：

从下面的面试笔记中提取所有被问到的**具体问题**，并为每个问题生成结构化信息，格式如下：

---

[分类] 问题内容

- **Definition**: 概念或原理的解释  
- **Example**: 示例或应用场景  
- **Answer**: 面试中应如何回答

分类只能是以下之一：算法、数据库、系统设计、编程语言、操作系统、网络、分布式系统、数据工程、机器学习、项目经验、行为面试、其他

请严格按照此格式输出，字段名用英文（Definition, Example, Answer），每个问题块之间用 `---` 分隔。

面试笔记：
{note}
"""
    )
    llm = ChatOpenAI(temperature=0)
    return LLMChain(prompt=prompt, llm=llm)

import re

def parse_classification_output(text: str) -> list:
    qa_list = []
    blocks = text.strip().split("---")

    for block in blocks:
        lines = block.strip().splitlines()
        if not lines:
            continue

        header = lines[0]
        match = re.match(r"\[(.*?)\]\s*(.+)", header)
        if not match:
            continue

        category, question = match.groups()
        current_field = None
        field_buffers = {"definition": [], "example": [], "answer": []}

        for line in lines[1:]:
            if line.startswith("- **Definition**:"):
                current_field = "definition"
                field_buffers["definition"].append(line.split("**Definition**:")[1].strip())
            elif line.startswith("- **Example**:"):
                current_field = "example"
                field_buffers["example"].append(line.split("**Example**:")[1].strip())
            elif line.startswith("- **Answer**:"):
                current_field = "answer"
                field_buffers["answer"].append(line.split("**Answer**:")[1].strip())
            elif current_field:
                field_buffers[current_field].append(line.strip())

        qa_list.append({
            "category": category.strip(),
            "question": question.strip(),
            "definition": "\n".join(field_buffers["definition"]).strip(),
            "example": "\n".join(field_buffers["example"]).strip(),
            "answer": "\n".join(field_buffers["answer"]).strip()
        })

    return qa_list
