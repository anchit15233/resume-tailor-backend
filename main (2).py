import openai
import os
import re

# ⛔ Insert your OpenAI API key here
openai.api_key = "sk-...your-key..."

def calculate_match_score(resume_text, jd_text):
    resume_words = set(re.findall(r'\b\w+\b', resume_text.lower()))
    jd_words = set(re.findall(r'\b\w+\b', jd_text.lower()))
    matched = resume_words & jd_words
    if len(jd_words) == 0:
        return 0
    return round(len(matched) / len(jd_words) * 100, 2)

def generate_tailored_resume(resume_text, jd_text):
    prompt = f"""You are a professional resume editor.
Here is a resume:
{resume_text}

Here is a job description:
{jd_text}

Please tailor the resume to better match the job description using relevant keywords, especially in the summary and experience sections. Keep it concise and realistic."""
    
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You help tailor resumes to match job descriptions."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=1000,
            temperature=0.7
        )
        return response['choices'][0]['message']['content']
    except Exception as e:
        return f"Error: {str(e)}"
