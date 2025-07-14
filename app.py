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
            tree.insert("", "end", values=(doc["id"], doc["file_path"]))
    except Exception as e:
        messagebox.showerror("Error", f"Failed to fetch documents:\n{e}")

def browse_file():
    global selected_file_path
    path = fd.askopenfilename(title="Select any file", filetypes=[("All files", "*.*")])
    if path:
        if not path.lower().endswith(".docx"):
            messagebox.showerror("Invalid File", "Please select a valid .docx Word document.")
            selected_file_path = None
            selected_file_label.config(text="No file selected")
            return

        selected_file_path = path
        selected_file_label.config(text=f"Selected File: {os.path.basename(path)}")


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
root.geometry("900x600")

frame_form = tk.Frame(root)
frame_form.pack(pady=10)

browse_button = tk.Button(root, text="Add File", command=browse_file)
browse_button.pack(pady=5)

selected_file_label = tk.Label(root, text="No file selected", fg="gray")
selected_file_label.pack()

upload_button = tk.Button(root, text="Add Document", command=add_document)
upload_button.pack(pady=10)

# Table
tree = ttk.Treeview(root, columns=("ID","File Path"), show="headings")
tree.heading("ID", text="ID")
tree.heading("File Path", text="File Path")
tree.pack(padx=10, pady=10, fill="both", expand=True)

refresh_table()

root.mainloop()
