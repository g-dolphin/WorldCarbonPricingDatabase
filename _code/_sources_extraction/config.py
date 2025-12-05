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

def load_sources(path: str | Path) -> List[Source]:
    """Load sources metadata from a CSV file into Source objects."""
    df = pd.read_csv(path)
    sources: List[Source] = []
    for _, row in df.iterrows():
        sources.append(Source(
            source_id=str(row["source_id"]),
            jurisdiction_code=str(row.get("jurisdiction_code", "")),
            instrument_id=str(row.get("instrument_id", "")),
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
        ))
    return sources
