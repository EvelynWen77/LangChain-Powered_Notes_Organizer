import sqlite3
import os

DB_PATH = os.getenv("DB_PATH", "notes.db")

def init_db():
    with sqlite3.connect(DB_PATH) as conn:
        cur = conn.cursor()
        cur.execute("""
            CREATE TABLE IF NOT EXISTS questions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                company TEXT,
                position TEXT,
                date TEXT,
                round TEXT,
                category TEXT,
                question TEXT,
                definition TEXT,
                example TEXT,
                answer TEXT
            )
        """)
        conn.commit()

def save_questions_to_db(company, position, date, round_num, qa_list):
    with sqlite3.connect(DB_PATH) as conn:
        cur = conn.cursor()
        for item in qa_list:
            cur.execute("""
                INSERT INTO questions (company, position, date, round, category, question, definition, example, answer)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                company,
                position,
                date,
                round_num,
                item.get("category", ""),
                item.get("question", ""),
                item.get("definition", ""),
                item.get("example", ""),
                item.get("answer", ""),
            ))
        conn.commit()

def load_all_note_metadata_with_id():
    with sqlite3.connect(DB_PATH) as conn:
        cur = conn.cursor()
        cur.execute("""
            SELECT id, company, position, date, round, category, question, definition, example, answer
            FROM questions
            ORDER BY date DESC
        """)
        return cur.fetchall()

def delete_note_by_id(note_id):
    with sqlite3.connect(DB_PATH) as conn:
        cur = conn.cursor()
        cur.execute("DELETE FROM questions WHERE id = ?", (note_id,))
        conn.commit()

def load_notes_as_documents():
    from langchain.schema import Document
    with sqlite3.connect(DB_PATH) as conn:
        cur = conn.cursor()
        cur.execute("""
            SELECT company, position, date, round, category, question
            FROM questions
        """)
        rows = cur.fetchall()
        docs = []
        for r in rows:
            metadata = {
                "company": r[0],
                "position": r[1],
                "date": r[2],
                "round": r[3],
                "category": r[4],
            }
            docs.append(Document(page_content=r[5], metadata=metadata))
        return docs
