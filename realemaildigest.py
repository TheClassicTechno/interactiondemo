import os
import json
import base64
from fpdf import FPDF
from bs4 import BeautifulSoup
from dotenv import load_dotenv
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
import openai
#from langfuse import Client as LFClient

# -----------------------------
# Load environment variables
# -----------------------------
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")           # OpenAI key
#LANGFUSE_SECRET_KEY = os.getenv("LANGFUSE_SECRET_KEY") # Langfuse key

openai.api_key = OPENAI_API_KEY
#lf_client = LFClient(api_key=LANGFUSE_SECRET_KEY)

# -----------------------------
# Gmail API setup
# -----------------------------
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']
creds = Credentials.from_authorized_user_file("token.json", SCOPES)
service = build('gmail', 'v1', credentials=creds)

# -----------------------------
# Fetch latest N emails
# -----------------------------
def fetch_latest_emails(n=5):
    results = service.users().messages().list(userId='me', maxResults=n, labelIds=['INBOX']).execute()
    messages = results.get('messages', [])
    
    email_list = []
    for msg in messages:
        msg_data = service.users().messages().get(userId='me', id=msg['id'], format='full').execute()
        headers = {h['name']: h['value'] for h in msg_data['payload']['headers']}
        sender = headers.get("From", "Unknown")
        subject = headers.get("Subject", "No Subject")
        date = headers.get("Date", "")
        
        # Extract body
        body = ""
        if 'parts' in msg_data['payload']:
            for part in msg_data['payload']['parts']:
                if part['mimeType'] == 'text/plain':
                    body = base64.urlsafe_b64decode(part['body']['data']).decode('utf-8')
                    break
                elif part['mimeType'] == 'text/html':
                    html_body = base64.urlsafe_b64decode(part['body']['data']).decode('utf-8')
                    body = BeautifulSoup(html_body, "html.parser").get_text()
        else:
            if msg_data['payload']['body'].get('data'):
                body = base64.urlsafe_b64decode(msg_data['payload']['body']['data']).decode('utf-8')
        
        email_list.append({
            "sender": sender,
            "subject": subject,
            "date": date,
            "body": body.strip()
        })
    
    return email_list

# -----------------------------
# Generate digest using OpenAI
# -----------------------------
def generate_digest(emails):
    email_text = ""
    for e in emails:
        email_text += f"From: {e['sender']}\nSubject: {e['subject']}\nBody: {e['body']}\n\n"

    prompt = f"""
Summarize the following emails into a structured 'Morning Briefing'.
Use sections: Deadlines, Meetings, Expenses, Other.
Keep it concise and use bullet points and emojis.
Emails:
{email_text}
"""

    run = lf_client.track("digest_generation")
    run.add_input(prompt)

    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3,
        max_tokens=600
    )

    digest_text = response['choices'][0]['message']['content']
    run.add_output(digest_text)
    run.finish()

    return digest_text.strip()

# -----------------------------
# Save digest to color-coded PDF
# -----------------------------
COLOR_MAP = {
    "Deadlines": (255, 0, 0),   # Red
    "Meetings": (0, 0, 255),    # Blue
    "Expenses": (0, 128, 0),    # Green
    "Other": (255, 215, 0)      # Yellow
}

def save_pdf(text, output_path="output_digest.pdf"):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", "B", 16)
    pdf.cell(200, 10, "🌅 Morning Briefing", ln=True, align="C")
    pdf.ln(10)

    pdf.set_font("Arial", size=12)
    current_section = None
    for line in text.split("\n"):
        line_strip = line.strip()
        # Detect section headers
        for section in COLOR_MAP:
            if line_strip.startswith(section):
                current_section = section
                pdf.set_text_color(*COLOR_MAP[section])
                pdf.multi_cell(0, 10, line_strip)
                break
        else:
            pdf.set_text_color(0, 0, 0)  # Default black for content
            pdf.multi_cell(0, 10, line_strip)

    pdf.output(output_path)

# -----------------------------
# Main
# -----------------------------
if __name__ == "__main__":
    print("📨 Fetching latest emails from Gmail...")
    emails = fetch_latest_emails(5)
    print(f"✅ Fetched {len(emails)} emails.")

    print("🤖 Generating AI digest with OpenAI...")
    digest = generate_digest(emails)

    print("🖨 Saving digest to color-coded PDF...")
    save_pdf(digest)
    print("✅ Digest generated: output_digest.pdf")
