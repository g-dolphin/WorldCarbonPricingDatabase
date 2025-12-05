from __future__ import annotations
import io
from bs4 import BeautifulSoup
import pdfplumber

def extract_text_from_html(content_bytes: bytes) -> str:
    """Extract readable text from an HTML document."""
    soup = BeautifulSoup(content_bytes, "lxml")
    for tag in soup(["script", "style", "noscript"]):
        tag.extract()
    text = soup.get_text("\n")
    lines = [line.strip() for line in text.splitlines()]
    return "\n".join(line for line in lines if line)

def extract_text_from_pdf(content_bytes: bytes) -> str:
    """Extract text from a (mostly text-based) PDF document."""
    buf = io.BytesIO(content_bytes)
    parts: list[str] = []
    with pdfplumber.open(buf) as pdf:
        for page in pdf.pages:
            parts.append(page.extract_text() or "")
    return "\n\n".join(parts)
