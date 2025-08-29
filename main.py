
# FastAPI backend for the Email Digest App
# ----------------------------------------
# Receives uploaded email JSON, generates a digest, and returns a PDF.

from fastapi import FastAPI, UploadFile, File
from fastapi.responses import FileResponse
import json
from digest import generate_digest_from_emails, save_pdf
import openai
import os

# Load environment variables from .env file
from dotenv import load_dotenv
load_dotenv()

# Set OpenAI API key
openai.api_key = os.getenv("OPENAI_API_KEY")

# Enable CORS for frontend (React)
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Endpoint to generate a PDF digest from uploaded emails JSON
@app.post("/generate-digest/")
async def generate_digest(file: UploadFile = File(...)):
    # Read uploaded file content
    content = await file.read()
    # Parse JSON to get emails
    emails = json.loads(content)
    # Generate digest text using OpenAI
    digest_text = generate_digest_from_emails(emails)
    # Save digest as PDF
    pdf_path = save_pdf(digest_text, "output_digest.pdf")
    # Return PDF as file response
    return FileResponse(pdf_path, filename="morning_digest.pdf")
