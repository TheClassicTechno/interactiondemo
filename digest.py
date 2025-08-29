
# Email Digest Generator
# ---------------------
# This module loads emails, summarizes them using OpenAI, and generates a PDF digest.

import json
import os
from fpdf import FPDF
import openai

# Set OpenAI API key from environment variable
openai.api_key = os.getenv("OPENAI_API_KEY")

def generate_digest_from_emails(emails):
    """
    Summarizes a list of emails into a structured morning briefing using OpenAI.
    Sections: Deadlines, Meetings, Expenses, Other/Miscellaneous.
    """
    email_text = ""
    # Build a single string with all emails for the prompt
    for e in emails:
        sender = e.get('sender', e.get('from', 'Unknown'))
        email_text += f"From: {sender}\nSubject: {e['subject']}\nBody: {e['body']}\n\n"

    # Prompt for OpenAI summarization
    prompt = f"""
Summarize the following emails into a structured Morning Briefing daily when people check their emails.
Use sections: Deadlines, Meetings, Expenses, Other/Miscellaneous.
Keep it concise and use clear bullet points.
Emails:
{email_text}
"""

    # Call OpenAI API to generate the digest
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
    """
    Saves the digest text to a PDF file using FPDF.
    """
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", "B", 16)
    # Title
    pdf.cell(200, 10, "Good Morning! Morning Briefing :)", ln=True, align="C")
    pdf.ln(10)
    pdf.set_font("Arial", size=12)
    # Write each line of the digest
    for line in text.split("\n"):
        pdf.multi_cell(0, 10, line)
    pdf.output(output_path)
    return output_path
