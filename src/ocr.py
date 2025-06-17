import base64
import os
from io import BytesIO
from typing import Tuple

from pdf2image import convert_from_path
from PIL import Image
import openai


def pdf_first_page_to_image(pdf_path: str) -> Image.Image:
    """Convert the first page of a PDF to a PIL image."""
    images = convert_from_path(pdf_path, first_page=1, last_page=1)
    return images[0]


def ocr_image(image: Image.Image) -> str:
    """Use OpenAI GPT-4o Vision to extract text from an image."""
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY not set")

    buffered = BytesIO()
    image.save(buffered, format="PNG")
    img_b64 = base64.b64encode(buffered.getvalue()).decode()

    client = openai.OpenAI(api_key=api_key)
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "image_url",
                        "image_url": {"url": f"data:image/png;base64,{img_b64}"},
                    },
                    {
                        "type": "text",
                        "text": "Extract the drawing number or title for renaming",
                    },
                ],
            }
        ],
        max_tokens=50,
    )
    return response.choices[0].message.content.strip()


def sanitize_filename(text: str) -> str:
    """Sanitize text for use as a filename."""
    import re

    name = re.sub(r"[^0-9a-zA-Z_-]+", "_", text.strip())
    return name[:50] or "document"
