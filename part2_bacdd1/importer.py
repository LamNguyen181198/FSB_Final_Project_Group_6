from docx import Document as DocxDocument
from part2_bacdd1.models import Question

class QuestionImporter:
    def __init__(self, db):
        self.db = db

    def import_from_docx(self, file_path):
        doc = DocxDocument(file_path)
        subject = None
        content = None
        options = []
        answer = None

        for para in doc.paragraphs:
            text = para.text.strip()
            if text.startswith("Môn:"):
                subject = text.replace("Môn:", "").strip()
            elif text.startswith("Câu hỏi:"):
                content = text.replace("Câu hỏi:", "").strip()
            elif text.startswith("A.") or text.startswith("B.") or text.startswith("C.") or text.startswith("D."):
                options.append(text)
            elif text.startswith("Đáp án:"):
                answer = text.replace("Đáp án:", "").strip()
                if subject and content and options and answer:
                    q = Question(subject, content, ";".join(options), answer)
                    self.db.add_question(q)
                    # reset cho câu tiếp theo
                    content = None
                    options = []
                    answer = None
        return True