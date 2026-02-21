from __future__ import annotations

from pathlib import Path
from typing import Dict, Any, List, Tuple
import re
import pandas as pd

from .utils import download, get_text, sha256_file

def sanitize_filename(name: str) -> str:
    name = re.sub(r"[^A-Za-z0-9._-]+", "_", name).strip("_")
    return name or "artifact"

def download_artifacts(cfg: Dict[str, Any], artifacts_dir: Path) -> pd.DataFrame:
    """
    Downloads artifacts declared in config and returns a dataframe mapping:
      act_id -> local_artifact -> sha256
    for later merging into sources register.

    Supported config patterns:
      artifacts:
        key:
          url: ...
          filename: ...
          act_id: ... (optional)
          kind: pdf|html (optional)

      amending_acts:
        - act_id: ...
          url: ...
          entry_into_force: ...
    """
    artifacts_dir.mkdir(parents=True, exist_ok=True)
    rows = []

    for key, meta in (cfg.get("artifacts", {}) or {}).items():
        url = meta.get("url", "")
        if not url:
            continue
        fn = meta.get("filename") or sanitize_filename(key)
        act_id = meta.get("act_id") or meta.get("source_act_id") or meta.get("act_id_hint") or ""
        kind = (meta.get("kind") or "").lower()

        out_path = artifacts_dir / fn

        if kind == "html" or url.lower().endswith(".html") or url.lower().endswith(".htm"):
            html = get_text(url)
            out_path.write_text(html, encoding="utf-8")
        else:
            download(url, out_path)

        rows.append({
            "act_id": act_id,
            "artifact_key": key,
            "source_url": url,
            "local_artifact": str(out_path),
            "content_hash_sha256": sha256_file(out_path)
        })

    # Handle amending_acts list (pdf/html)
    for act in (cfg.get("amending_acts", []) or []):
        act_id = act.get("act_id","")
        url = act.get("url","")
        if not url:
            continue
        ext = ".pdf" if url.lower().endswith(".pdf") else ".html"
        out_path = artifacts_dir / f"{sanitize_filename(act_id)}{ext}"
        if ext == ".html":
            out_path.write_text(get_text(url), encoding="utf-8")
        else:
            download(url, out_path)

        rows.append({
            "act_id": act_id,
            "artifact_key": "amending_act",
            "source_url": url,
            "local_artifact": str(out_path),
            "content_hash_sha256": sha256_file(out_path)
        })

    return pd.DataFrame(rows)
