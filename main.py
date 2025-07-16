from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import openai
import pdfplumber
import docx
from difflib import SequenceMatcher
from werkzeug.utils import secure_filename

app = Flask(__name__)
CORS(app)

openai.api_key = os.getenv("OPENAI_API_KEY")

def extract_text_from_file(file):
    filename = secure_filename(file.filename)
    ext = os.path.splitext(filename)[1].lower()

    if ext == ".pdf":
        with pdfplumber.open(file) as pdf:
            return "\n".join([page.extract_text() for page in pdf.pages if page.extract_text()])
    elif ext in [".doc", ".docx"]:
        document = docx.Document(file)
        return "\n".join([p.text for p in document.paragraphs])
    else:
        return ""

def calculate_match_score(resume_text, job_description):
    return round(SequenceMatcher(None, resume_text.lower(), job_description.lower()).ratio() * 100, 2)

def generate_tailored_resume(resume_text, job_description):
    prompt = (
        "You are a resume tailoring assistant.\n"
        "Based on the following resume and job description, rewrite the resume to match the job role better.\n\n"
        f"Job Description:\n{job_description}\n\n"
        f"Original Resume:\n{resume_text}\n\n"
        "Tailored Resume:"
    )

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}]
    )
    return response["choices"][0]["message"]["content"].strip()

@app.route("/analyze", methods=["POST"])
def analyze_resume():
    resume_file = request.files["resume"]
    job_description = request.form["job_description"]

    resume_text = extract_text_from_file(resume_file)
    match_score = calculate_match_score(resume_text, job_description)
    tailored_resume = generate_tailored_resume(resume_text, job_description)

    return jsonify({
        "match_score": match_score,
        "tailored_resume": tailored_resume
    })

@app.route("/", methods=["GET"])
def home():
    return "Resume Tailor Backend is Live!"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
