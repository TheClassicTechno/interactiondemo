from fastapi import FastAPI, UploadFile, File
from fastapi.responses import FileResponse
import json
from digest import generate_digest_from_emails, save_pdf

app = FastAPI()

@app.post("/generate-digest/")
async def generate_digest(file: UploadFile = File(...)):
    content = await file.read()
    emails = json.loads(content)
    digest_text = generate_digest_from_emails(emails)
    pdf_path = save_pdf(digest_text, "output_digest.pdf")
    return FileResponse(pdf_path, filename="morning_digest.pdf")
