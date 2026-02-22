from __future__ import annotations
import io
from bs4 import BeautifulSoup
import zipfile
import xml.etree.ElementTree as ET
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

def extract_text_from_docx(content_bytes: bytes) -> str:
    """Extract text from a DOCX document (basic paragraph text)."""
    buf = io.BytesIO(content_bytes)
    try:
        with zipfile.ZipFile(buf) as zf:
            xml = zf.read("word/document.xml")
    except Exception:
        return ""
    try:
        root = ET.fromstring(xml)
    except Exception:
        return ""
    parts: list[str] = []
    for elem in root.iter():
        if elem.tag.endswith("}t") and elem.text:
            parts.append(elem.text)
        elif elem.tag.endswith("}p"):
            parts.append("\n")
    text = "".join(parts)
    lines = [line.strip() for line in text.splitlines()]
    return "\n".join(line for line in lines if line)
