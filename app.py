import os
from dotenv import load_dotenv
load_dotenv()

import streamlit as st
from datetime import datetime
from langchain_openai import ChatOpenAI
from chains.summarize_and_categorize import get_summarize_chain, parse_classification_output
from utils.note_loader import (
    init_db,
    save_questions_to_db,
    load_all_note_metadata_with_id,
    delete_note_by_id,
)
from utils.md_export import export_to_markdown, qa_list_to_markdown
from agent_runner import run_agent_query

init_db()
st.set_page_config(page_title="Interview Note Assistant")

page = st.sidebar.radio("📂 Navigation", ["Add Note", "View History", "Search"])

# -----------------------------
# Add Note Page
# -----------------------------
if page == "Add Note":
    st.title("🧠 Add Interview Note")

    company = st.text_input("🏢 Company", value=st.session_state.get("edit_company", ""))
    position = st.text_input("💼 Position", value=st.session_state.get("edit_position", ""))
    date = st.date_input("📅 Interview Date", value=st.session_state.get("edit_date", datetime.today()))
    round_num = st.text_input("🔁 Round", value=st.session_state.get("edit_round", ""))
    note = st.text_area("✏️ Paste your interview note here")

    if st.button("Classify & Summarize"):
        if not note.strip():
            st.warning("Please enter a note.")
        else:
            chain = get_summarize_chain()
            raw_output = chain.run(note=note)
            qa_list = parse_classification_output(raw_output)

            if not qa_list:
                st.warning("⚠️ 无法识别出有效的问题分类。")
            else:
                save_questions_to_db(company, position, str(date), round_num, qa_list)
                st.success("✅ 成功分类并保存每条问题！")
                st.markdown("### 🧾 分类结果")
                for item in qa_list:
                    st.markdown(f"**[{item['category']}]** {item['question']}")
                    st.markdown(f"- **定义**: {item['definition']}")
                    st.markdown(f"- **示例**: {item['example']}")
                    st.markdown(f"- **标准回答**: {item['answer']}")
                    st.markdown("---")

                markdown_summary = qa_list_to_markdown(qa_list)
                md_path = export_to_markdown(markdown_summary, note, "多问题", company, round_num, str(date), position)

                with open(md_path, "rb") as f:
                    st.download_button("📥 Download Markdown", data=f, file_name=os.path.basename(md_path))

                for key in ["edit_note_id", "edit_company", "edit_position", "edit_date", "edit_round"]:
                    st.session_state.pop(key, None)

# -----------------------------
# View History Page
# -----------------------------
elif page == "View History":
    st.title("📜 Interview History")
    rows = load_all_note_metadata_with_id()

    if not rows:
        st.info("No interview notes recorded yet.")
    else:
        companies = sorted(set(r[1] for r in rows))
        positions = sorted(set(r[2] for r in rows))
        selected_company = st.selectbox("📍 Filter by Company", ["All"] + companies)
        selected_position = st.selectbox("🧑‍💻 Filter by Position", ["All"] + positions)

        filtered_rows = [
            r for r in rows
            if (selected_company == "All" or r[1] == selected_company)
            and (selected_position == "All" or r[2] == selected_position)
        ]

        for row in filtered_rows:
            (
                qa_id, company, position, date, round_num,
                category, question, definition, example, answer
            ) = row
            with st.container():
                st.markdown(f"### [{category}] {question}")
                st.markdown(f"**Company**: {company} | **Position**: {position} | **Date**: {date} | **Round**: {round_num}")
                st.markdown(f"- **定义**: {definition}")
                st.markdown(f"- **示例**: {example}")
                st.markdown(f"- **标准回答**: {answer}")

                col1, _ = st.columns(2)
                if col1.button("🗑️ Delete", key=f"del_{qa_id}"):
                    delete_note_by_id(qa_id)
                    st.experimental_rerun()

                st.markdown("---")

# -----------------------------
# Search Page (Agent)
# -----------------------------
elif page == "Search":
    st.title("🔎 Ask Your Interview Notes")

    query = st.text_input("Ask a question")

    if st.button("Search"):
        if not query.strip():
            st.warning("Please enter a query.")
        else:
            with st.spinner("🤖 Agent thinking..."):
                try:
                    result = run_agent_query(query)
                    st.markdown("### 💬 Agent Response")
                    st.markdown(result)
                except Exception as e:
                    st.error(f"Agent Error: {e}")

