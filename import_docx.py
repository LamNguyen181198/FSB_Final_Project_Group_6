"""
import_docx: Import docx files into a database
"""
from datetime import date
import os.path
import sqlite3

import config


def insert_or_update_docx_file(file_path: str, subject: str):
    # 1. Validate file extension
    if not file_path.lower().endswith(".docx"):
        print("❌ Only .docx files are allowed.")
        return

    file_name = os.path.basename(file_path)
    today = date.today()

    try:
        conn = sqlite3.connect(config.DATABASE_PATH)
        cursor = conn.cursor()

        # 2. Check if document already exists
        cursor.execute("SELECT ID FROM exam_documents WHERE document = ?", (file_name,))
        existing = cursor.fetchone()

        if existing:
            # 3. Update subject and date
            cursor.execute(
                "UPDATE exam_documents SET subject = ?, added_date = ? WHERE document = ?",
                (subject, today, file_name)
            )
            print(f"Updated '{file_name}' with subject '{subject}' and date {today}")
        else:
            # 4. Insert new record
            cursor.execute(
                "INSERT INTO exam_documents (document, subject, added_date) VALUES (?, ?, ?)",
                (file_name, subject, today)
            )
            print(f"Inserted '{file_name}' with subject '{subject}' into database.")

        conn.commit()

    except sqlite3.Error as e:
        print("SQLite error:", e)

