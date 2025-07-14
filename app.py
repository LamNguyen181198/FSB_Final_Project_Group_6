# desktop_app.py
import tkinter as tk
from tkinter import filedialog as fd
from tkinter import ttk, messagebox
import requests
import os

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
            tree.insert("", "end", values=(doc["id"], doc["document_name"], doc["subject"], doc["file_path"]))
    except Exception as e:
        messagebox.showerror("Error", f"Failed to fetch documents:\n{e}")

def browse_file():
    global selected_file_path
    path = fd.askopenfilename(title="Select .docx File", filetypes=[("Word Documents", "*.docx")])
    if path:
        selected_file_path = path
        selected_file_label.config(text=f"Selected File: {os.path.basename(path)}")

def add_document():
    global selected_file_path
    name = entry_name.get().strip()
    subject = subject_name.get().strip()

    if not name or not subject:
        messagebox.showwarning("Missing Info", "Please enter both document name and subject.")
        return

    if not selected_file_path:
        messagebox.showwarning("No File", "Please select a .docx file.")
        return

    try:
        with open(selected_file_path, "rb") as file:
            files = {"file": (os.path.basename(selected_file_path), file, "application/vnd.openxmlformats-officedocument.wordprocessingml.document")}
            data = {"document_name": name, "subject": subject}
            response = requests.post(f"{API_URL}/add_document", data=data, files=files)
            response.raise_for_status()

        entry_name.delete(0, tk.END)
        subject_name.delete(0, tk.END)
        selected_file_label.config(text="No file selected")
        selected_file_path = None
        refresh_table()
    except Exception as e:
        messagebox.showerror("Upload Error", str(e))

# UI setup
root = tk.Tk()
root.title("Document Management Desktop App")
root.geometry("900x600")

frame_form = tk.Frame(root)
frame_form.pack(pady=10)

tk.Label(frame_form, text="Document Name").grid(row=0, column=0)
entry_name = tk.Entry(frame_form, width=30)
entry_name.grid(row=0, column=1)

tk.Label(frame_form, text="Subject").grid(row=1, column=0)
subject_name = tk.Entry(frame_form, width=30)
subject_name.grid(row=1, column=1)

browse_button = tk.Button(root, text="Browse .docx File", command=browse_file)
browse_button.pack(pady=5)

selected_file_label = tk.Label(root, text="No file selected", fg="gray")
selected_file_label.pack()

upload_button = tk.Button(root, text="Add Document", command=add_document)
upload_button.pack(pady=10)

# Table
tree = ttk.Treeview(root, columns=("ID", "Document Name", "Subject", "File Path"), show="headings")
tree.heading("ID", text="ID")
tree.heading("Document Name", text="Document Name")
tree.heading("Subject", text="Subject")
tree.heading("File Path", text="File Path")
tree.pack(padx=10, pady=10, fill="both", expand=True)

refresh_table()

root.mainloop()
