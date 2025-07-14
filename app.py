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

# Display document content
tk.Label(root, text="Document Content Preview:").pack(pady=(10, 0))
text_output = tk.Text(root, height=10, wrap="word")
text_output.pack(padx=10, pady=5, fill="both", expand=True)

# Add a canvas for images
tk.Label(root, text="Embedded Images:").pack(pady=(10, 0))
image_canvas = tk.Canvas(root, height=300)
image_canvas.pack(padx=10, pady=5, fill="both", expand=False)

# To hold image references (to avoid garbage collection)
image_refs = []

refresh_table()

root.mainloop()
