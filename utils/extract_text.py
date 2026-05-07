from pathlib import Path
import docx
from PyPDF2 import PdfReader

def extract_text_from_file(path):
    path = Path(path)
    ext = path.suffix.lower()
    try:
        if ext == ".pdf":
            reader = PdfReader(str(path))
            pages = [p.extract_text() or "" for p in reader.pages]
            return "\n".join(pages)
        elif ext == ".docx":
            doc = docx.Document(str(path))
            return "\n".join([p.text for p in doc.paragraphs])
        else:
            return path.read_text(encoding="utf-8", errors="ignore")
    except Exception as e:
        print("extract_text error:", e)
        return ""
