# main.py
from fastapi import FastAPI, UploadFile, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import sqlite3
import os
import shutil

app = FastAPI()

# Allow CORS from desktop app
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

UPLOAD_FOLDER = "uploaded_docs"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# SQLite init
def init_db():
    conn = sqlite3.connect("database/exam_documents.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS exam_documents (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            file_path TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

init_db()

@app.get("/document")
def get_document():
    conn = sqlite3.connect("database/exam_documents.db")
    cursor = conn.cursor()
    cursor.execute("SELECT DISTINCT id, file_path FROM exam_documents")
    rows = cursor.fetchall()
    conn.close()
    return [{"id": row[0], "file_path": row[1]} for row in rows]

@app.post("/add_document")
def add_document(
    file: UploadFile = Form(...)
):
    try:
        file_location = os.path.join(UPLOAD_FOLDER, file.filename)
        with open(file_location, "wb") as f:
            shutil.copyfileobj(file.file, f)

        conn = sqlite3.connect("database/exam_documents.db")
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO exam_documents (file_path)
            VALUES (?)
        """, (file_location,))
        conn.commit()
        new_id = cursor.lastrowid
        conn.close()

        return {
            "id": new_id,
            "file_path": file_location
        }
    except Exception as e:
        import traceback
        traceback.print_exc()  # Optional: log full error to console
        raise HTTPException(status_code=500, detail=str(e))

