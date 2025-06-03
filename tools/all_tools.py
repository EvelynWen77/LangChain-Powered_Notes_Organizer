from langchain.tools import Tool
from retriever.vector_store import load_faiss_index
from chains.summarize_and_categorize import get_summarize_chain
from utils.note_loader import load_all_note_metadata_with_id
from utils.md_export import export_all_to_markdown
from collections import Counter

# 1. 语义搜索
def semantic_query_tool_func(query: str) -> str:
    vectorstore = load_faiss_index()
    results = vectorstore.similarity_search(query, k=5)
    return "\n\n".join([f"[{r.metadata.get('category', '未分类')}] {r.page_content}" for r in results])

semantic_query_tool = Tool(
    name="SemanticInterviewSearch",
    func=semantic_query_tool_func,
    description="Search similar questions using semantic embedding."
)

# 2. 总结分类
def summarize_func(text: str) -> str:
    chain = get_summarize_chain()
    return chain.run(note=text)

summarize_tool = Tool(
    name="SummarizeNote",
    func=summarize_func,
    description="Summarize and classify a new interview note."
)

# 3. 分类统计
def note_stat_func(_: str = "") -> str:
    rows = load_all_note_metadata_with_id()
    categories = [r[5] for r in rows]  # 5 = category
    counter = Counter(categories)
    total = len(rows)
    lines = [f"{cat}: {count}" for cat, count in counter.items()]
    return f"Total questions: {total}\n" + "\n".join(lines)

note_stat_tool = Tool(
    name="NoteStatistics",
    func=note_stat_func,
    description="Show question counts grouped by category."
)

# 4. 导出
def export_func(_: str = "") -> str:
    path = export_all_to_markdown()
    return f"📂 Markdown exported to:\n`{path}`"

export_tool = Tool(
    name="ExportNotes",
    func=export_func,
    description="Export all interview questions to markdown."
)

# 5. 关键词过滤（改为搜索问题）
def keyword_filter_func(keyword: str) -> str:
    rows = load_all_note_metadata_with_id()
    results = [r for r in rows if keyword.lower() in r[6].lower()]
    if not results:
        return f"No questions containing '{keyword}'"
    return "\n".join([f"[{r[5]}] {r[6]}" for r in results[:5]])

keyword_filter_tool = Tool(
    name="KeywordFilter",
    func=keyword_filter_func,
    description="Find interview questions by keyword."
)

# 6. 公司筛选（提取公司下所有问题）
def company_summary_func(company: str) -> str:
    rows = load_all_note_metadata_with_id()
    company_rows = [r for r in rows if company.lower() in r[1].lower()]
    if not company_rows:
        return f"No questions found for company: {company}"
    return "\n".join([f"[{r}" for r in company_rows[:10]])

company_summary_tool = Tool(
    name="CompanySummary",
    func=company_summary_func,
    description="Show questions from a specific company."
)

def fetch_all_records(_: str = "") -> str:
    rows = load_all_note_metadata_with_id()
    # print(f'DEBUG: all rows from db: {rows}')
    if not rows:
        return "No interview questions found."

    formatted = []
    for i, r in enumerate(rows, 1):
        note_id, company, position, date, round_num, category, question = r[:7]
        formatted.append(
            f"{i}. [{category}] {question}\n"
            f"   - Company: {company}\n"
            f"   - Position: {position}\n"
            f"   - Date: {date}\n"
            f"   - Round: {round_num}"
        )
    return "\n\n".join(formatted)


fetch_all_records_tool = Tool(
    name="FetchRecentInterviewQuestions",
    func=fetch_all_records,
    description="List 10 recent interview questions including company, position, category, date, and round."
)




# ✅ 工具注册统一入口
ALL_TOOLS = [
    semantic_query_tool,
    summarize_tool,
    note_stat_tool,
    export_tool,
    keyword_filter_tool,
    company_summary_tool,
    fetch_all_records_tool,
]
