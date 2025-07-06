import tkinter as tk
from tkinter import filedialog, messagebox
import os

from import_docx import insert_or_update_docx_file


class DocxImporterApp(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Exam Document Importer")
        self.geometry("450x250")
        self.resizable(False, False)

        # Subject Input
        tk.Label(self, text="Enter Subject:", font=("Segoe UI", 10)).pack(pady=(20, 5))
        self.subject_entry = tk.Entry(self, width=50, font=("Segoe UI", 10))
        self.subject_entry.pack()

        # File Selection
        tk.Label(self, text="Choose a .docx exam file:", font=("Segoe UI", 10)).pack(pady=(20, 5))
        tk.Button(self, text="📂 Browse for .docx File", command=self.select_file, width=30).pack()

        # Display selected file
        self.selected_file_label = tk.Label(self, text="No file selected", fg="gray", font=("Segoe UI", 9))
        self.selected_file_label.pack(pady=(5, 0))

        # Footer Status
        self.status_label = tk.Label(self, text="", fg="blue", font=("Segoe UI", 9))
        self.status_label.pack(pady=(15, 0))

        self.file_path = None

    def select_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("Word Documents", "*.docx")])
        if not file_path:
            return

        subject = self.subject_entry.get().strip()
        if not subject:
            messagebox.showwarning("Missing Subject", "Please enter a subject before selecting a file.")
            return

        self.file_path = file_path
        file_name = os.path.basename(file_path)
        self.selected_file_label.config(text=f"Selected file: {file_name}")

        try:
            insert_or_update_docx_file(file_path, subject)
            messagebox.showinfo("Success", f"File '{file_name}' imported under subject '{subject}'.")
            self.status_label.config(text="Import successful", fg="green")
        except Exception as e:
            messagebox.showerror("Error", f"❌ Failed to import file: {str(e)}")
            self.status_label.config(text="Import failed", fg="red")


if __name__ == "__main__":
    app = DocxImporterApp()
    app.mainloop()
