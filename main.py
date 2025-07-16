from flask import Flask, request, jsonify
from flask_cors import CORS
from resume_parser import extract_text_from_file
from tailor_ai import generate_tailored_resume, calculate_match_score

app = Flask(__name__)
CORS(app)  # Allow frontend on Netlify to connect

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

if __name__ == "__main__":
    app.run(debug=True)
