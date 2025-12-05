from __future__ import annotations
from pathlib import Path
import httpx
from bs4 import BeautifulSoup
from .config import Source
from .storage import store_artifact

def fetch_source(source: Source, raw_root: Path) -> list[str]:
    """
    Fetch a single source according to its source_type and store artifacts.

    Returns a list of artifact_ids created for this source.
    """
    if source.access_method != "requests":
        raise NotImplementedError("Phase 1 only supports access_method='requests'")

    resp = httpx.get(source.url, follow_redirects=True, timeout=30)
    resp.raise_for_status()

    artifact_ids: list[str] = []

    if source.source_type in ("html_page", "html_index_pdf_links"):
        # Store landing page HTML
        artifact_ids.append(
            store_artifact(
                raw_root=raw_root,
                source=source,
                artifact_type="html",
                content_bytes=resp.content,
                fetched_url=str(resp.url),
                http_status=resp.status_code,
            )
        )

        # Optionally follow PDF links
        if source.source_type == "html_index_pdf_links":
            soup = BeautifulSoup(resp.text, "lxml")
            for a in soup.find_all("a", href=True):
                href = a["href"]
                if not href.lower().endswith(".pdf"):
                    continue
                if source.doc_pattern:
                    text_match = source.doc_pattern in (a.get_text() or "")
                    href_match = source.doc_pattern in href
                    if not (text_match or href_match):
                        continue

                pdf_url = httpx.URL(href, base=resp.url).join(href)
                pdf_resp = httpx.get(pdf_url, follow_redirects=True, timeout=60)
                if pdf_resp.status_code != 200:
                    continue

                artifact_ids.append(
                    store_artifact(
                        raw_root=raw_root,
                        source=source,
                        artifact_type="pdf",
                        content_bytes=pdf_resp.content,
                        fetched_url=str(pdf_resp.url),
                        http_status=pdf_resp.status_code,
                    )
                )

    elif source.source_type == "pdf_direct":
        # Direct PDF link
        artifact_ids.append(
            store_artifact(
                raw_root=raw_root,
                source=source,
                artifact_type="pdf",
                content_bytes=resp.content,
                fetched_url=str(resp.url),
                http_status=resp.status_code,
            )
        )
    else:
        raise ValueError(f"Unknown source_type: {source.source_type}")

    return artifact_ids
