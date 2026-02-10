from __future__ import annotations
import csv
from dataclasses import dataclass
from pathlib import Path
from typing import List
from .patterns import MatchResult, extract_all_matches
import argparse
import pandas as pd

RAW_ROOT = Path("_raw/sources")
SOURCES_PATH = RAW_ROOT / "sources.csv" 

@dataclass
class Artifact:
    artifact_id: str
    source_id: str
    jurisdiction_code: str
    instrument_id: str
    year: str
    local_path: str

def load_text_artifacts(jurisdiction_filter: List[str] | None = None) -> List[Artifact]:
    meta_path = RAW_ROOT / "meta" / "raw_artifacts.csv"
    artifacts: List[Artifact] = []

    if not meta_path.exists():
        raise FileNotFoundError(f"Could not find raw_artifacts metadata at {meta_path}")

    # Build source_id → scheme_id/year lookup from sources file
    source_to_instrument: dict[str, str] = {}
    source_to_year: dict[str, str] = {}
    if SOURCES_PATH.exists():
        sources_df = pd.read_csv(SOURCES_PATH, dtype=str)
        for _, r in sources_df.iterrows():
            sid = str(r.get("source_id", "")).strip()
            inst = str(r.get("scheme_id", "") or r.get("instrument_id", "")).strip()
            year = str(r.get("year", "")).strip()
            if sid and inst:
                source_to_instrument[sid] = inst
            if sid and year:
                source_to_year[sid] = year

    with meta_path.open(newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row.get("artifact_type") not in {"html", "pdf"}:
                continue

            juris = row.get("jurisdiction_code", "")
            if jurisdiction_filter and juris not in jurisdiction_filter:
                continue

            local_path = row.get("local_path", "")
            parts = Path(local_path)
            basename = parts.name.rsplit(".", 1)[0]
            text_rel = Path("text") / row["source_id"] / f"{basename}.txt"

            # Prefer instrument_id from meta; fall back to sources lookup
            instrument_meta = str(row.get("instrument_id", "")).strip()
            instrument_id = instrument_meta or source_to_instrument.get(row["source_id"], "")
            year = source_to_year.get(row["source_id"], "")

            artifacts.append(
                Artifact(
                    artifact_id=row["artifact_id"],
                    source_id=row["source_id"],
                    jurisdiction_code=juris,
                    instrument_id=instrument_id,
                    year=year,
                    local_path=str(text_rel),
                )
            )

    return artifacts

def run_extraction(jurisdiction_filter: List[str] | None = None) -> None:
    artifacts = load_text_artifacts(jurisdiction_filter=jurisdiction_filter)
    out_path = RAW_ROOT / "cp_candidates.csv"
    new_file = not out_path.exists()

    with out_path.open("a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        if new_file:
            writer.writerow([
                "candidate_id",
                "instrument_id",
                "source_id",
                "jurisdiction_code",
                "artifact_id",
                "year",
                "field_name",
                "value",          # generic string value (IPCC codes, dates, pretty rate string)
                "numeric_value",  # numeric price/tax rate where applicable
                "currency",       # currency code (for prices/tax rates)
                "unit",           # unit (e.g. tCO2e)
                "snippet",
                "method",
                "confidence",
            ])

        counter = 0
        for art in artifacts:
            text_path = RAW_ROOT / art.local_path
            if not text_path.exists():
                continue

            text = text_path.read_text(encoding="utf-8", errors="ignore")
            matches = extract_all_matches(text)

            for m in matches:
                start, end = m.span
                snippet_start = max(0, start - 120)
                snippet_end = min(len(text), end + 120)
                snippet = text[snippet_start:snippet_end].replace("\n", " ")

                candidate_id = f"{art.artifact_id}_{counter}"
                counter += 1

                writer.writerow([
                    candidate_id,
                    art.instrument_id,
                    art.source_id,
                    art.jurisdiction_code,
                    art.artifact_id,
                    art.year,
                    m.field_name,
                    m.value,
                    "" if m.numeric_value is None else f"{m.numeric_value:.6g}",
                    m.currency or "",
                    m.unit or "",
                    snippet,
                    m.method,
                    f"{m.confidence:.2f}",
                ])

def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--jurisdiction",
        "-j",
        action="append",
        help="Jurisdiction code(s) to filter (can be repeated). If omitted, runs on all.",
    )
    args = parser.parse_args()
    run_extraction(jurisdiction_filter=args.jurisdiction)

if __name__ == "__main__":
    main()
