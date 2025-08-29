import json
import os
from fpdf import FPDF
import openai

openai.api_key = os.getenv("OPENAI_API_KEY")

def generate_digest_from_emails(emails):
    email_text = ""
    for e in emails:
        sender = e.get('sender', e.get('from', 'Unknown'))
        email_text += f"From: {sender}\nSubject: {e['subject']}\nBody: {e['body']}\n\n"

    prompt = f"""
Summarize the following emails into a structured Morning Briefing daily when people check their emails.
Use sections: Deadlines, Meetings, Expenses, Other/Miscellaneous.
Keep it concise and use clear bullet points.
Emails:
{email_text}
"""

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant that summarizes emails into a morning briefing."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=500
    )
    digest_text = response["choices"][0]["message"]["content"]
    return digest_text.strip()

def save_pdf(text, output_path="output_digest.pdf"):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", "B", 16)
    pdf.cell(200, 10, "Good Morning! Morning Briefing :)", ln=True, align="C")
    pdf.ln(10)
    pdf.set_font("Arial", size=12)
    for line in text.split("\n"):
        pdf.multi_cell(0, 10, line)
    pdf.output(output_path)
    return output_path
