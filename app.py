# desktop_app.py
import tkinter as tk
from docx import Document
from tkinter import filedialog as fd
from tkinter import ttk, messagebox
import requests
import os
from PIL import Image, ImageTk
import io
import zipfile
from part2_bacdd1 import db, importer
from part2_bacdd1.models import Question
from part2_bacdd1.db import Database
db = Database()

API_URL = "http://127.0.0.1:8000"

selected_file_path = None

def refresh_table():
    for row in tree.get_children():
        tree.delete(row)
    try:
        response = requests.get(f"{API_URL}/document")
        response.raise_for_status()
        documents = response.json()
        for doc in documents:
            tree.insert("", "end", values=(doc["id"], doc["file_path"]))
    except Exception as e:
        messagebox.showerror("Error", f"Failed to fetch documents:\n{e}")

def display_docx_content(file_path):
    text_output.delete("1.0", tk.END)
    image_canvas.delete("all")
    image_refs.clear()

    try:
        doc = Document(file_path)

        # --- Extract paragraphs
        for para in doc.paragraphs:
            if para.text.strip():
                text_output.insert(tk.END, para.text + "\n")

        # --- Extract tables
        for table in doc.tables:
            text_output.insert(tk.END, "\n[Table]\n")
            for row in table.rows:
                row_data = [cell.text.strip() for cell in row.cells]
                text_output.insert(tk.END, " | ".join(row_data) + "\n")

        # --- Extract and render images
        with zipfile.ZipFile(file_path) as docx_zip:
            image_files = [f for f in docx_zip.namelist() if f.startswith("word/media/")]
            y_offset = 10
            for img_name in image_files:
                with docx_zip.open(img_name) as img_file:
                    img = Image.open(io.BytesIO(img_file.read()))
                    img.thumbnail((300, 300))
                    tk_img = ImageTk.PhotoImage(img)
                    image_canvas.create_image(10, y_offset, anchor="nw", image=tk_img)
                    image_refs.append(tk_img)  # Prevent garbage collection
                    y_offset += img.height + 10

    except Exception as e:
        messagebox.showerror("Read Error", f"Error reading document: {e}")

def browse_file():
    global selected_file_path
    path = fd.askopenfilename(title="Select any file", filetypes=[("All files", "*.*")])
    if path:
        if not path.lower().endswith(".docx"):
            messagebox.showwarning("File Warning", "This file is not a .docx file. It may not be supported.")

        selected_file_path = path
        selected_file_label.config(text=f"Selected File: {os.path.basename(path)}")
        display_docx_content(selected_file_path)

def add_document():
    global selected_file_path
    if not selected_file_path:
        messagebox.showwarning("No File", "Please select a .docx file.")
        return

    try:
        with open(selected_file_path, "rb") as file:
            files = {"file": (os.path.basename(selected_file_path), file, "application/vnd.openxmlformats-officedocument.wordprocessingml.document")}
            response = requests.post(f"{API_URL}/add_document", files=files)
            response.raise_for_status()

        selected_file_label.config(text="No file selected")
        selected_file_path = None
        refresh_table()
    except Exception as e:
        messagebox.showerror("Upload Error", str(e))

# UI setup
root = tk.Tk()
root.title("Document Management Desktop App")
root.geometry("1200x800")

notebook = ttk.Notebook(root)
tab_doc = tk.Frame(notebook)
tab_question = tk.Frame(notebook)
notebook.add(tab_doc, text="Document Management")
notebook.add(tab_question, text="Question Management")
notebook.pack(fill="both", expand=True)

frame_form = tk.Frame(tab_doc)
frame_form.pack(pady=10)

browse_button = tk.Button(tab_doc, text="Add File", command=browse_file)
browse_button.pack(pady=5)

selected_file_label = tk.Label(tab_doc, text="No file selected", fg="gray")
selected_file_label.pack()

upload_button = tk.Button(tab_doc, text="Upload Document", command=add_document)
upload_button.pack(pady=10)

# Table
tree = ttk.Treeview(tab_doc, columns=("ID","File Path"), show="headings")
tree.heading("ID", text="ID")
tree.heading("File Path", text="File Path")
tree.pack(padx=10, pady=10, fill="both", expand=True)

# Display document content
tk.Label(tab_doc, text="Document Content Preview:").pack(pady=(10, 0))
text_output = tk.Text(tab_doc, height=10, wrap="word")
text_output.pack(padx=10, pady=5, fill="both", expand=True)

# Add a canvas for images
tk.Label(tab_doc, text="Embedded Images:").pack(pady=(10, 0))
image_canvas = tk.Canvas(tab_doc, height=300)
image_canvas.pack(padx=10, pady=5, fill="both", expand=False)

# To hold image references (to avoid garbage collection)
image_refs = []

refresh_table()

# --- Tab 2: Question Management ---
tk.Label(tab_question, text="Subject:").pack()
subject_entry = tk.Entry(tab_question, width=50)
subject_entry.pack()

tk.Label(tab_question, text="Question Content:").pack()
content_entry = tk.Entry(tab_question, width=80)
content_entry.pack()

tk.Label(tab_question, text="Options:").pack()
options_frame = tk.Frame(tab_question)
options_frame.pack()

option_entries = []
for opt in ["A", "B", "C", "D"]:
    row = tk.Frame(options_frame)
    row.pack(fill="x", pady=2)
    label = tk.Label(row, text=f"Option {opt}:", width=12)
    label.pack(side="left")
    entry = tk.Entry(row, width=60)
    entry.pack(side="left", fill="x", expand=True)
    option_entries.append(entry)

tk.Label(tab_question, text="Correct Answer:").pack()
answer_entry = tk.Entry(tab_question, width=20)
answer_entry.pack()

def add_question():
    subject = subject_entry.get().strip()
    content = content_entry.get().strip()
    answer = answer_entry.get().strip()

    option_labels = ["A", "B", "C", "D"]
    options = []
    for label, entry in zip(option_labels, option_entries):
        text = entry.get().strip()
        if text:
            options.append(f"{label}. {text}")

    options_str = ";".join(options)

    if subject and content and options_str and answer:
        db.add_question(Question(subject, content, options_str, answer))
        refresh_questions()
        messagebox.showinfo("Add Question", "Question added successfully!")

def refresh_questions():
    subject = subject_entry.get().strip()
    question_list.delete(0, tk.END)
    for row in db.get_questions(subject):
        question_list.insert(tk.END, f"{row[0]}: {row[1]} | {row[2]} | Answer: {row[3]}")

def update_question():
    selected = question_list.curselection()
    if selected:
        qid = question_list.get(selected[0]).split(":")[0]
        subject = subject_entry.get().strip()
        content = content_entry.get().strip()
        answer = answer_entry.get().strip()

        option_labels = ["A", "B", "C", "D"]
        options = []
        for label, entry in zip(option_labels, option_entries):
            text = entry.get().strip()
            if text:
                options.append(f"{label}. {text}")

        options_str = ";".join(options)

        db.update_question(qid, subject, content, options_str, answer)
        refresh_questions()
        messagebox.showinfo("Update Question", "Question updated successfully!")

def delete_question():
    selected = question_list.curselection()
    if selected:
        qid = question_list.get(selected[0]).split(":")[0]
        db.delete_question(qid)
        refresh_questions()
        messagebox.showinfo("Delete Question", "Question deleted successfully!")

question_importer = importer.QuestionImporter(db)
def import_questions_from_file():
    path = fd.askopenfilename(title="Select question file (.docx)", filetypes=[("Word files", "*.docx")])
    if path:
        try:
            question_importer.import_from_docx(path)
            messagebox.showinfo("Success", "Questions imported successfully!")
            refresh_questions()
        except Exception as e:
            messagebox.showerror("Import Error", str(e))

question_list = tk.Listbox(tab_question, width=100)
question_list.pack(padx=10, pady=10)

question_list.bind('<<ListboxSelect>>', lambda e: on_select_question(e))

def on_select_question(event):
    selected = question_list.curselection()
    if selected:
        qid = question_list.get(selected[0]).split(":")[0]
        subject = subject_entry.get().strip()
        rows = db.get_questions(subject)
        for row in rows:
            if str(row[0]) == qid:
                content_entry.delete(0, tk.END)
                content_entry.insert(0, row[1])

                opts = row[2].split(";")
                for i, e in enumerate(option_entries):
                    e.delete(0, tk.END)
                    if i < len(opts):
                        opt_text = opts[i].strip()
                        if ". " in opt_text:
                            opt_text = opt_text.split(". ", 1)[1]
                        e.insert(0, opt_text)

                answer_entry.delete(0, tk.END)
                answer_entry.insert(0, row[3])
                break

tk.Button(tab_question, text="Import Questions from File", command=import_questions_from_file).pack(pady=10)
tk.Button(tab_question, text="Load Questions", command=refresh_questions).pack()
tk.Button(tab_question, text="Add Question", command=add_question).pack(pady=2)
tk.Button(tab_question, text="Update Question", command=update_question).pack(pady=2)
tk.Button(tab_question, text="Delete Question", command=delete_question).pack(pady=2)

root.mainloop()
