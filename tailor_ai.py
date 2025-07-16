import openai
import os
openai.api_key = os.getenv("OPENAI_API_KEY")

def generate_tailored_resume(resume_text, job_description):
    prompt = f"""
You are a professional career assistant. Tailor the candidate's resume below to better match the given job description.

Job Description:
{job_description}

Resume:
{resume_text}

Tailored Resume:
"""
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a resume tailoring assistant."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.7,
        max_tokens=1000
    )

    return response['choices'][0]['message']['content'].strip()

def calculate_match_score(resume_text, job_description):
    prompt = f"""
Compare the following resume and job description and estimate how well they match on a scale of 0 to 100.

Resume:
{resume_text}

Job Description:
{job_description}

Give ONLY the number.
"""
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a job match evaluator."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.2,
        max_tokens=10
    )

    return float(response['choices'][0]['message']['content'].strip().replace('%', ''))
