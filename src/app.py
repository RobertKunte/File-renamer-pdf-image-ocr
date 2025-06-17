from __future__ import annotations

import shutil
from pathlib import Path
from datetime import datetime
import json
from typing import Optional, List

from flask import Flask, render_template, request, redirect, url_for, send_from_directory
from werkzeug.utils import secure_filename
from dotenv import load_dotenv

from .ocr import pdf_first_page_to_image, ocr_image, sanitize_filename
from .utils import save_history, HISTORY_FILE

load_dotenv()


ALLOWED_EXTENSIONS = {"pdf"}
OUTPUT_DIR = Path("output")
OUTPUT_DIR.mkdir(exist_ok=True)


def allowed_file(filename: str) -> bool:
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


def create_app() -> Flask:
    app = Flask(__name__)

    @app.route("/")
    def index():
        return render_template("index.html")

    @app.route("/process", methods=["POST"])
    def process():
        folder = request.form.get("folder")
        files: List[Path] = []
        if folder:
            files = [Path(folder) / f for f in Path(folder).glob("*.pdf")]
        if "file" in request.files and request.files["file"].filename:
            file = request.files["file"]
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                upload_path = OUTPUT_DIR / filename
                file.save(upload_path)
                files.append(upload_path)
        results = []
        for pdf_path in files:
            image = pdf_first_page_to_image(str(pdf_path))
            text = ocr_image(image)
            base_name = sanitize_filename(text)
            image_path = OUTPUT_DIR / f"{base_name}.png"
            text_path = OUTPUT_DIR / f"{base_name}.txt"
            pdf_new_path = OUTPUT_DIR / f"{base_name}.pdf"
            image.save(image_path)
            text_path.write_text(text)
            shutil.copy(pdf_path, pdf_new_path)
            save_history({
                "time": datetime.utcnow().isoformat(),
                "original": str(pdf_path),
                "pdf": str(pdf_new_path),
                "image": str(image_path),
                "text": str(text_path),
            })
            results.append({
                "image": image_path.name,
                "text": text,
                "pdf": pdf_new_path.name,
            })
        return render_template("index.html", results=results)

    @app.route("/history")
    def history():
        entries = []
        if HISTORY_FILE.exists():
            entries = json.loads(HISTORY_FILE.read_text())[::-1]
        return render_template("history.html", entries=entries)

    @app.route('/output/<path:filename>')
    def output_files(filename):
        return send_from_directory(OUTPUT_DIR, filename)

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
