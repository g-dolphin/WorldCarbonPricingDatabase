from __future__ import annotations
import datetime as dt
import re
from pathlib import Path
import httpx
from bs4 import BeautifulSoup
from .config import Source
from .storage import store_artifact

DEFAULT_HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (X11; Linux x86_64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0.0.0 Safari/537.36"
    )
}

def _extract_year(text: str, pattern: str | None = None) -> int | None:
    if not text:
        return None
    if pattern:
        try:
            match = re.search(pattern, text, flags=re.IGNORECASE)
        except re.error:
            match = None
        if match:
            for group in match.groups():
                if group and group.isdigit() and len(group) == 4:
                    return int(group)
            found = re.findall(r"(20\d{2})", match.group(0))
            if found:
                return int(found[-1])
    found = re.findall(r"(20\d{2})", text)
    return int(found[-1]) if found else None


def _select_links(soup: BeautifulSoup, selector: str | None) -> list[tuple[str, str]]:
    links: list[tuple[str, str]] = []
    if selector:
        for node in soup.select(selector):
            href = node.get("href")
            if not href:
                continue
            links.append((href, node.get_text(" ", strip=True)))
    if not links:
        for a in soup.find_all("a", href=True):
            links.append((a["href"], a.get_text(" ", strip=True)))
    return links


def _candidate_pdf_links(
    soup: BeautifulSoup, source: Source, base_url: httpx.URL
) -> list[tuple[str, int | None]]:
    candidates: list[tuple[str, int | None]] = []
    for href, text in _select_links(soup, source.doc_link_selector):
        if not href.lower().endswith(".pdf"):
            continue
        if source.doc_pattern:
            if not re.search(source.doc_pattern, href, flags=re.IGNORECASE) and not re.search(
                source.doc_pattern, text, flags=re.IGNORECASE
            ):
                continue
        year = _extract_year(f"{text} {href}", source.doc_pattern)
        url = httpx.URL(href, base=base_url).join(href)
        candidates.append((str(url), year))
    return candidates


def _year_url_candidates(source: Source) -> list[tuple[str, int]]:
    if not source.year_url_template:
        return []
    current_year = dt.datetime.utcnow().year
    start_year = current_year
    if source.last_seen_year and source.last_seen_year.isdigit():
        start_year = max(start_year, int(source.last_seen_year) + 1)
    target_years = list(range(start_year, current_year + 2))
    return [
        (source.year_url_template.format(year=year), year) for year in target_years
    ]


def fetch_source(source: Source, raw_root: Path) -> list[str]:
    """
    Fetch a single source according to its source_type and store artifacts.

    Returns a list of artifact_ids created for this source.
    """
    if source.access_method != "requests":
        raise NotImplementedError("Phase 1 only supports access_method='requests'")

    headers = DEFAULT_HEADERS
    if "r.jina.ai" in source.url:
        headers = None
    resp = httpx.get(source.url, follow_redirects=True, timeout=30, headers=headers)
    resp.raise_for_status()

    artifact_ids: list[str] = []

    is_pdf_url = str(resp.url).lower().endswith(".pdf") or source.url.lower().endswith(".pdf")
    is_docx_url = str(resp.url).lower().endswith(".docx") or source.url.lower().endswith(".docx")
    content_type = resp.headers.get("content-type", "").lower()
    is_pdf_content = "application/pdf" in content_type
    is_docx_content = "application/vnd.openxmlformats-officedocument.wordprocessingml.document" in content_type
    if source.source_type in ("html_page", "html_index_pdf_links") and (is_pdf_url or is_pdf_content or is_docx_url or is_docx_content):
        # Fallback: treat as direct PDF when the response is a PDF.
        artifact_type = "docx" if (is_docx_url or is_docx_content) else "pdf"
        artifact_ids.append(
            store_artifact(
                raw_root=raw_root,
                source=source,
                artifact_type=artifact_type,
                content_bytes=resp.content,
                fetched_url=str(resp.url),
                http_status=resp.status_code,
            )
        )
    elif source.source_type in ("html_page", "html_index_pdf_links"):
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
            candidates = _candidate_pdf_links(soup, source, resp.url)
            candidates.extend(_year_url_candidates(source))

            last_seen_year = None
            if source.last_seen_year and source.last_seen_year.isdigit():
                last_seen_year = int(source.last_seen_year)

            if last_seen_year is not None:
                candidates = [
                    c for c in candidates if c[1] is None or c[1] > last_seen_year
                ] or candidates

            candidates = sorted(candidates, key=lambda c: (c[1] or 0), reverse=True)
            seen_urls: set[str] = set()
            for pdf_url, _year in candidates[:5]:
                if pdf_url in seen_urls:
                    continue
                seen_urls.add(pdf_url)
                pdf_resp = httpx.get(
                    pdf_url,
                    follow_redirects=True,
                    timeout=60,
                    headers=DEFAULT_HEADERS,
                )
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
    elif source.source_type == "docx_direct":
        artifact_ids.append(
            store_artifact(
                raw_root=raw_root,
                source=source,
                artifact_type="docx",
                content_bytes=resp.content,
                fetched_url=str(resp.url),
                http_status=resp.status_code,
            )
        )
    else:
        raise ValueError(f"Unknown source_type: {source.source_type}")

    return artifact_ids
