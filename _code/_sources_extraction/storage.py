from __future__ import annotations
import csv
import hashlib
from datetime import datetime, timezone
from pathlib import Path
from .parse import extract_text_from_html, extract_text_from_pdf
from .config import Source

def _timestamp() -> str:
    return datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S")

def _hash_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()[:12]

def store_artifact(
    raw_root: Path,
    source: Source,
    artifact_type: str,
    content_bytes: bytes,
    fetched_url: str,
    http_status: int | None,
) -> str:
    """
    Store a raw HTML/PDF artifact, log it in raw_artifacts.csv,
    and write a corresponding text file.
    """
    ts = _timestamp()
    h = _hash_bytes(content_bytes)
    artifact_id = f"{source.source_id}_{ts}_{h}"

    if artifact_type not in {"html", "pdf"}:
        raise ValueError(f"Unsupported artifact_type: {artifact_type}")

    ext = "html" if artifact_type == "html" else "pdf"
    scheme_id = (source.instrument_id or "").strip() or "unknown_scheme"
    out_dir = raw_root / scheme_id / artifact_type / source.source_id
    out_dir.mkdir(parents=True, exist_ok=True)
    file_path = out_dir / f"{ts}_{h}.{ext}"
    file_path.write_bytes(content_bytes)

    meta_dir = raw_root / scheme_id / "meta"
    meta_dir.mkdir(parents=True, exist_ok=True)
    meta_path = meta_dir / "raw_artifacts.csv"
    new = not meta_path.exists()

    with meta_path.open("a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        if new:
            writer.writerow([
                "artifact_id",
                "source_id",
                "jurisdiction_code",
                "instrument_id",
                "artifact_type",
                "local_path",
                "fetched_url",
                "fetched_at",
                "http_status",
                "content_hash",
            ])
        writer.writerow([
            artifact_id,
            source.source_id,
            source.jurisdiction_code,
            source.instrument_id,
            artifact_type,
            str(file_path.relative_to(raw_root)),
            fetched_url,
            datetime.now(timezone.utc).isoformat(),
            http_status if http_status is not None else "",
            h,
        ])

    # Text extraction
    if artifact_type == "html":
        text = extract_text_from_html(content_bytes)
    else:
        text = extract_text_from_pdf(content_bytes)

    if text.strip():
        text_dir = raw_root / scheme_id / "text" / source.source_id
        text_dir.mkdir(parents=True, exist_ok=True)
        text_path = text_dir / f"{ts}_{h}.txt"
        text_path.write_text(text, encoding="utf-8")

    return artifact_id
