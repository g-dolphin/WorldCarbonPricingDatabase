from __future__ import annotations

import argparse
import csv
import re
from collections import defaultdict
from pathlib import Path

RAW_ROOT = Path("_raw/sources")
SCHEME_PATH = Path("_raw/_aux_files/scheme_description.csv")
JURISDICTIONS_PATH = Path("_code/_compilation/_utils/jurisdictions.json")

DOC_TYPE_KEYWORDS = {
    "legislation": ["regulation", "law", "act", "ordinance", "decree", "directive", "legislation"],
    "report": ["report", "status report", "annual report", "bulletin", "inventory"],
}


def _load_scheme_names() -> dict[str, str]:
    if not SCHEME_PATH.exists():
        return {}
    out: dict[str, str] = {}
    with SCHEME_PATH.open(newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            scheme_id = str(row.get("scheme_id", "")).strip()
            scheme_name = str(row.get("scheme_name", "")).strip()
            if scheme_id:
                out[scheme_id] = scheme_name
    return out


def _load_existing_source_ids(sources_csv: Path) -> set[str]:
    if not sources_csv.exists():
        return set()
    with sources_csv.open(newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        return {str(row.get("source_id", "")).strip() for row in reader if row.get("source_id")}


def _build_id_counters(existing_ids: set[str]) -> dict[tuple[str, str], int]:
    counters: dict[tuple[str, str], int] = defaultdict(int)
    for sid in existing_ids:
        parts = sid.split("-")
        if len(parts) < 3:
            continue
        prefix = "-".join(parts[:-2])
        token = parts[-2]
        tail = parts[-1]
        if tail.isdigit():
            counters[(prefix, token)] = max(counters[(prefix, token)], int(tail))
    return counters


def _doc_type_token(document_type: str) -> str:
    mapping = {
        "legislation": "leg",
        "official_publication": "gov",
        "webpage": "web",
        "report": "rep",
    }
    return mapping.get(document_type, "src")


def _scheme_prefix(scheme_id: str) -> str:
    parts = scheme_id.split("_")
    if len(parts) >= 2 and len(parts[0]) == 3 and len(parts[1]) <= 3:
        return f"{parts[0].upper()}-{parts[1].upper()}"
    if parts and len(parts[0]) == 3:
        return parts[0].upper()
    return parts[0].upper() if parts else "SRC"


def _guess_document_type(text: str, source_type: str) -> str:
    lower = text.lower()
    for doc_type, keywords in DOC_TYPE_KEYWORDS.items():
        if any(k in lower for k in keywords):
            return doc_type
    if source_type == "pdf_direct":
        return "official_publication"
    return "webpage"


def _guess_year(text: str) -> str:
    matches = re.findall(r"(20\\d{2})", text)
    return matches[-1] if matches else ""


def _guess_jurisdiction(scheme_id: str, scheme_name: str) -> str:
    if scheme_name:
        lowered = scheme_name.lower()
        for token in [" carbon", " ets", " emissions trading", " emission trading"]:
            if token in lowered:
                return scheme_name[: lowered.index(token)].strip()
        return scheme_name.strip()
    return scheme_id


def _infer_source_type(present_types: set[str]) -> str:
    if "html" in present_types and "pdf" in present_types:
        return "html_index_pdf_links"
    if "html" in present_types:
        return "html_page"
    return "pdf_direct"


def _collect_manifest(skip_unknown_scheme: bool) -> dict[tuple[str, str], dict]:
    manifest: dict[tuple[str, str], dict] = {}
    for scheme_dir in RAW_ROOT.iterdir():
        if not scheme_dir.is_dir():
            continue
        scheme_id = scheme_dir.name
        if skip_unknown_scheme and scheme_id == "unknown_scheme":
            continue
        for artifact_type in ["html", "pdf", "text"]:
            type_dir = scheme_dir / artifact_type
            if not type_dir.exists():
                continue
            for source_dir in type_dir.iterdir():
                if not source_dir.is_dir():
                    continue
                source_id = source_dir.name
                key = (scheme_id, source_id)
                entry = manifest.setdefault(
                    key,
                    {
                        "scheme_id": scheme_id,
                        "old_source_id": source_id,
                        "artifact_types": set(),
                        "files": [],
                    },
                )
                entry["artifact_types"].add(artifact_type)
                for path in source_dir.glob("*"):
                    if path.is_file():
                        entry["files"].append(path)
    return manifest


def bootstrap_sources(sources_csv: Path, out_csv: Path, skip_unknown_scheme: bool) -> None:
    scheme_names = _load_scheme_names()
    existing_ids = _load_existing_source_ids(sources_csv)
    counters = _build_id_counters(existing_ids)

    manifest = _collect_manifest(skip_unknown_scheme=skip_unknown_scheme)

    rows = []
    for (scheme_id, old_source_id), entry in sorted(manifest.items()):
        if old_source_id in existing_ids:
            continue
        present_types = entry["artifact_types"]
        source_type = _infer_source_type(present_types)
        sample_name = entry["files"][0].name if entry["files"] else ""
        doc_type = _guess_document_type(sample_name, source_type)
        token = _doc_type_token(doc_type)
        prefix = _scheme_prefix(scheme_id)
        key = (prefix, token)
        counters[key] += 1
        new_source_id = f"{prefix}-{token}-{counters[key]:03d}"

        scheme_name = scheme_names.get(scheme_id, "")
        jurisdiction = _guess_jurisdiction(scheme_id, scheme_name)
        year = _guess_year(sample_name)

        rows.append(
            {
                "source_id": new_source_id,
                "scheme_id": scheme_id,
                "jurisdiction": jurisdiction,
                "document_type": doc_type,
                "source_type": source_type,
                "url": "",
                "doc_pattern": "(20\\d{2})",
                "access_method": "requests",
                "parsing_strategy": "generic_pdf" if source_type == "pdf_direct" else "generic_html",
                "change_frequency": "ad_hoc",
                "active": "0",
                "title": "",
                "institution": "",
                "year": year,
                "citation_key": "",
                "notes": f"bootstrap from disk; old_source_id={old_source_id}",
                "old_source_id": old_source_id,
                "artifact_types": ";".join(sorted(present_types)),
                "sample_file": sample_name,
            }
        )

    fieldnames = [
        "source_id",
        "scheme_id",
        "jurisdiction",
        "document_type",
        "source_type",
        "url",
        "doc_pattern",
        "access_method",
        "parsing_strategy",
        "change_frequency",
        "active",
        "title",
        "institution",
        "year",
        "citation_key",
        "notes",
        "old_source_id",
        "artifact_types",
        "sample_file",
    ]
    out_csv.parent.mkdir(parents=True, exist_ok=True)
    with out_csv.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow(row)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--sources-csv",
        default=str(RAW_ROOT / "sources.csv"),
        help="Path to sources.csv",
    )
    parser.add_argument(
        "--out",
        default=str(RAW_ROOT / "sources_bootstrap.csv"),
        help="Path to output CSV",
    )
    parser.add_argument(
        "--skip-unknown-scheme",
        action="store_true",
        help="Skip unknown_scheme directory",
    )
    args = parser.parse_args()

    bootstrap_sources(
        sources_csv=Path(args.sources_csv),
        out_csv=Path(args.out),
        skip_unknown_scheme=args.skip_unknown_scheme,
    )


if __name__ == "__main__":
    main()
