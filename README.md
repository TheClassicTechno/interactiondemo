# Email Digest App
# InboxifyAI
A full-stack application that summarizes emails into a structured morning briefing and generates a downloadable PDF digest. Built with Python (FastAPI, OpenAI, FPDF) for the backend and React (TypeScript) for the frontend.

---

## Features
- Upload emails as JSON (or fetch from Gmail API with Python script)
- Summarize and prioritize emails using OpenAI
- Generate a polished PDF digest
- Download the digest from the frontend

---


## Backend Setup (FastAPI)

1. **Clone the repository and navigate to the backend folder:**
   ```sh
   cd interactiondemo
   ```

2. **Create and activate a virtual environment:**
   ```sh
   python -m venv venv
   # On Windows:
   .\venv\Scripts\activate
   # On macOS/Linux:
   source venv/bin/activate
   ```

3. **Install Python dependencies:**
   ```sh
   pip install -r requirements.txt
   ```

4. **Set your OpenAI API key:**
   - Create a `.env` file in the backend root:
     ```env
     OPENAI_API_KEY=your-openai-api-key-here
     ```

5. **Start the FastAPI server:**
   ```sh
   uvicorn main:app --reload
   ```
   - The backend will run at `http://localhost:8000`

---

## Frontend Setup (React)

1. **Navigate to the frontend folder:**
   ```sh
   cd frontend
   ```

2. **Install Node dependencies:**
   ```sh
   npm install
   ```

3. **Start the React development server:**
   ```sh
   npm start
   ```
   - The frontend will run at `http://localhost:3000`

---

## Usage

1. Open the frontend in your browser: [http://localhost:3000](http://localhost:3000)
2. Upload a JSON file containing emails (see `emails.json` or `emails_deadlines_meetings.json` for format examples).
3. Click "Generate Digest" to receive and download the PDF summary.

---



## Troubleshooting
- If you see CORS errors, make sure both servers are running and the ports match the CORS config.
- If OpenAI API errors occur, check your API key and usage limits.
- For PDF issues, ensure `fpdf` is installed and working in your Python environment.

---

## License
MIT
