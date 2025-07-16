from flask import Flask, request, jsonify
from flask_cors import CORS
from resume_parser import extract_text_from_file
from tailor_ai import generate_tailored_resume, calculate_match_score

app = Flask(__name__)
CORS(app)  # Allow frontend on Netlify to connect

@app.route("/analyze", methods=["POST"])
def analyze_resume():
    try:
        resume_file = request.files["resume"]
        job_description = request.form["job_description"]

        print("✅ Received resume:", resume_file.filename)
        print("✅ Received job description:", job_description[:100])

        resume_text = extract_text_from_file(resume_file)
        print("✅ Extracted resume text length:", len(resume_text))

        match_score = calculate_match_score(resume_text, job_description)
        print("✅ Match score calculated:", match_score)

        tailored_resume = generate_tailored_resume(resume_text, job_description)
        print("✅ Tailored resume generated.")

        return jsonify({
            "match_score": match_score,
            "tailored_resume": tailored_resume
        })

    except Exception as e:
        print("❌ Error in analyze_resume():", e)
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
