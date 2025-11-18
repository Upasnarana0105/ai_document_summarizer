# AI-Powered Document Summarizer & Insights Generator

## Overview
Full-stack application that extracts text from uploaded PDFs or text files and returns an AI-generated summary, keywords, sentiment, and highlights.

## Project structure
- `backend/` - Flask backend and NLP helper functions
- `frontend/` - Static UI (index.html, script.js, styles.css)
- `sample_files/` - Place sample PDFs here for testing

## Run (lightweight fallback version)
1. Create and activate a Python virtual environment
   ```bash
   python -m venv venv
   source venv/bin/activate  # on Windows: venv\Scripts\activate
   ```

2. Install required packages (for best results, install all; fallback code will run with only Flask + PyPDF2)
   ```bash
   pip install -r backend/requirements.txt
   ```

3. Start the backend
   ```bash
   python backend/app.py
   ```

4. Open `frontend/index.html` in your browser and use the UI.
   - The frontend expects the backend at `http://127.0.0.1:5000`.
   - If you deploy, change the API URL in `frontend/script.js` accordingly.

## Notes
- The provided `backend/model.py` contains **lightweight fallback implementations** (naive summarizer & keyword extractor) so you can run the project without heavy ML dependencies.
- For improved summaries, replace the fallback functions by using a transformer model (HuggingFace `pipeline('summarization')`) — but that requires downloading a model which can be large.
