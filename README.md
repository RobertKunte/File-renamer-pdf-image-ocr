# PDF Renamer with OCR

This project provides a simple Flask web interface to rename scanned PDF drawings based on text extracted with OpenAI's GPT-4o Vision API. For every processed PDF an image of the first page, the OCR text and the renamed file are saved in the `output` folder. A history of generated files is also kept.

## Requirements
- Python 3.11+
- `pip`

Install dependencies:
```bash
pip install -r requirements.txt
```

## Running the application
1. Copy `.env.example` to `.env` and fill in your OpenAI API key.
2. Start the Flask server:
```bash
python -m src.app
```
3. Open `http://localhost:5000` in your browser.

## Features
- Upload a single PDF or provide a folder containing PDFs.
- OCR text extraction using OpenAI 4o Vision API.
- Generated image and text are displayed in the UI.
- Proposed file name based on OCR text is shown and saved.
- History page shows all processed PDFs.
