from dataclasses import dataclass
from pathlib import Path
from typing import Optional, List
import pandas as pd

@dataclass
class Source:
    source_id: str
    jurisdiction_code: str
    instrument_id: str
    document_type: str
    url: str
    source_type: str
    doc_pattern: Optional[str]
    access_method: str
    parsing_strategy: str
    change_frequency: str
    active: bool
    title: Optional[str]
    institution: Optional[str]
    year: Optional[str]
    citation_key: Optional[str]
    notes: Optional[str]
    doc_link_selector: Optional[str]
    year_url_template: Optional[str]
    last_seen_year: Optional[str]
    current_year_covered: Optional[str]
    release_month: Optional[str]
    last_checked: Optional[str]
    next_check_due: Optional[str]

def load_sources(path: str | Path) -> List[Source]:
    """Load sources metadata from a CSV file into Source objects."""
    df = pd.read_csv(path)
    sources: List[Source] = []
    for _, row in df.iterrows():
        jurisdiction = str(row.get("jurisdiction", "") or row.get("jurisdiction_code", "")).strip()
        scheme_id = str(row.get("scheme_id", "") or row.get("instrument_id", "")).strip()
        sources.append(Source(
            source_id=str(row["source_id"]),
            jurisdiction_code=jurisdiction,
            instrument_id=scheme_id,
            document_type=str(row.get("document_type", "")),
            url = str(row.get("url", "")).strip(),
            source_type = str(row.get("source_type", "html_page")).strip() or "html_page",
            doc_pattern=row.get("doc_pattern") if isinstance(row.get("doc_pattern"), str) and row.get("doc_pattern") else None,
            access_method=str(row.get("access_method", "requests")),
            parsing_strategy=str(row.get("parsing_strategy", "generic_html")),
            change_frequency=str(row.get("change_frequency", "ad_hoc")),
            active=bool(row.get("active", 0)),
            title=str(row.get("title")) if not pd.isna(row.get("title")) else None,
            institution=str(row.get("institution")) if not pd.isna(row.get("institution")) else None,
            year=str(row.get("year")) if not pd.isna(row.get("year")) else None,
            citation_key=str(row.get("citation_key")) if not pd.isna(row.get("citation_key")) else None,
            notes=str(row.get("notes")) if not pd.isna(row.get("notes")) else None,
            doc_link_selector=str(row.get("doc_link_selector")) if not pd.isna(row.get("doc_link_selector")) else None,
            year_url_template=str(row.get("year_url_template")) if not pd.isna(row.get("year_url_template")) else None,
            last_seen_year=str(row.get("last_seen_year")) if not pd.isna(row.get("last_seen_year")) else None,
            current_year_covered=str(row.get("current_year_covered")) if not pd.isna(row.get("current_year_covered")) else None,
            release_month=str(row.get("release_month")) if not pd.isna(row.get("release_month")) else None,
            last_checked=str(row.get("last_checked")) if not pd.isna(row.get("last_checked")) else None,
            next_check_due=str(row.get("next_check_due")) if not pd.isna(row.get("next_check_due")) else None,
        ))
    return sources
