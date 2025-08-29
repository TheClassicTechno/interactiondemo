import json
import os
from fpdf import FPDF
from dotenv import load_dotenv
import openai

load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
openai.api_key = OPENAI_API_KEY

def load_emails(file_path):
    with open(file_path, "r") as f:
        return json.load(f)

def generate_digest(emails):
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
    pdf.set_font("Arial", size=12)

    # Title
    pdf.set_font("Arial", "B", 16)
    pdf.cell(200, 10, "Good Morning! Morning Briefing :)", ln=True, align="C")
    pdf.ln(10)

    # Body
    pdf.set_font("Arial", size=12)
    for line in text.split("\n"):
        pdf.multi_cell(0, 10, line)

    pdf.output(output_path)


import glob

if __name__ == "__main__":
    # Find all emails*.json files in the current directory
    json_files = glob.glob("emails*.json")
    if not json_files:
        print("No emails JSON files found.")
    for json_file in json_files:
        emails = load_emails(json_file)
        digest = generate_digest(emails)
        # Name output PDF based on input file, e.g., emails2.json -> output_digest_emails2.pdf
        base = os.path.splitext(os.path.basename(json_file))[0]
        output_pdf = f"output_digest_{base}.pdf"
        save_pdf(digest, output_pdf)
        print(f"Digest generated: {output_pdf}")
