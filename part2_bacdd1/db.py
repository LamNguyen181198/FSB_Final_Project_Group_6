import sqlite3

from part2_bacdd1.models import Question

class Database:
    def __init__(self, db_path="database/exam_documents.db"):
        self.db_path = db_path
        self.init_db()

    def init_db(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS questions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                subject TEXT NOT NULL,
                content TEXT NOT NULL,
                options TEXT NOT NULL,
                answer TEXT NOT NULL
            )
        """)
        conn.commit()
        conn.close()

    def add_question(self, question: Question):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO questions (subject, content, options, answer)
            VALUES (?, ?, ?, ?)
        """, (question.subject, question.content, question.options, question.answer))
        conn.commit()
        conn.close()

    def get_questions(self, subject):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT id, content, options, answer FROM questions WHERE subject=?", (subject,))
        rows = cursor.fetchall()
        conn.close()
        return rows

    
    def update_question(self, qid, subject, content, options, answer):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE questions SET subject=?, content=?, options=?, answer=?
            WHERE id=?
        """, (subject, content, options, answer, qid))
        conn.commit()
        conn.close()

    def delete_question(self, qid):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("DELETE FROM questions WHERE id=?", (qid,))
        conn.commit()
        conn.close()


    
    