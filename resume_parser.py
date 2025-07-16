import pdfplumber
import docx
import os
from werkzeug.utils import secure_filename

def extract_text_from_file(file):
    filename = secure_filename(file.filename)
    extension = os.path.splitext(filename)[1].lower()

    if extension == ".pdf":
        with pdfplumber.open(file) as pdf:
            text = "\n".join([page.extract_text() or "" for page in pdf.pages])
        return text.strip()

    elif extension in [".docx", ".doc"]:
        doc = docx.Document(file)
        return "\n".join([para.text for para in doc.paragraphs])

    else:
        return "Unsupported file format."
