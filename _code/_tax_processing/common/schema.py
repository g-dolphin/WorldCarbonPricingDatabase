from __future__ import annotations

import datetime
import re
from typing import Dict
import pandas as pd

def host(url: str) -> str:
    url = str(url or "")
    return re.sub(r"^https?://([^/]+)/.*$", r"\1", url) if url.startswith("http") else ""

def build_sources_register(acts: pd.DataFrame, retrieved_date: str | None = None, retrieval_method: str = "web (candidate review)") -> pd.DataFrame:
    if retrieved_date is None:
        retrieved_date = datetime.date.today().isoformat()
    out = acts.copy()
    out["source_host"] = out["source_url"].fillna("").apply(host)
    out["retrieved_date"] = retrieved_date
    out["retrieval_method"] = retrieval_method
    out["content_hash_sha256"] = ""
    out["local_artifact"] = ""
    out["notes"] = "Populate hash + local artifact after storing authoritative snapshot."
    cols = ["jurisdiction","act_id","instrument_name","instrument_type","citation","source_url",
            "source_host","retrieved_date","retrieval_method","content_hash_sha256","local_artifact","notes"]
    return out[cols]

def merge_artifact_hashes(sources: pd.DataFrame, artifact_map: pd.DataFrame) -> pd.DataFrame:
    """Merge content_hash_sha256/local_artifact into sources by act_id, with fallback matching on source_url."""
    if artifact_map is None or artifact_map.empty:
        return sources
    out = sources.copy()
    # primary merge by act_id where act_id is provided
    m = artifact_map[artifact_map["act_id"].astype(str).str.len() > 0].drop_duplicates("act_id", keep="last")
    out = out.merge(m[["act_id","local_artifact","content_hash_sha256"]], on="act_id", how="left", suffixes=("","_new"))
    for col in ["local_artifact","content_hash_sha256"]:
        out[col] = out[f"{col}_new"].combine_first(out[col])
        out.drop(columns=[f"{col}_new"], inplace=True)
    # secondary merge by source_url
    u = artifact_map.drop_duplicates("source_url", keep="last")
    out = out.merge(u[["source_url","local_artifact","content_hash_sha256"]], on="source_url", how="left", suffixes=("","_url"))
    for col in ["local_artifact","content_hash_sha256"]:
        out[col] = out[f"{col}_url"].combine_first(out[col])
        out.drop(columns=[f"{col}_url"], inplace=True)
    return out

def write_seed_bundle(out_dir, tables: Dict[str, pd.DataFrame], prefix: str) -> None:
    from pathlib import Path
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    required = [
        ("acts", f"acts_{prefix}_seed.csv"),
        ("provisions", f"provisions_{prefix}_seed.csv"),
        ("rates", f"rates_{prefix}_seed.csv"),
        ("coverage", f"coverage_{prefix}_seed.csv"),
        ("exemptions", f"exemptions_{prefix}_seed.csv"),
        ("sources", f"sources_{prefix}.csv"),
    ]
    for key, fname in required:
        df = tables.get(key)
        if df is None:
            raise ValueError(f"Missing required table: {key}")
        df.to_csv(out_dir/fname, index=False)

    for key, df in tables.items():
        if key in {"acts","provisions","rates","coverage","exemptions","sources"}:
            continue
        df.to_csv(out_dir/f"{key}_{prefix}_seed.csv", index=False)
