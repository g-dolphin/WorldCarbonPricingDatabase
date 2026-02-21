from __future__ import annotations

import hashlib
from pathlib import Path
import requests

def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()

def download(url: str, out_path: Path, timeout: int = 180) -> None:
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with requests.get(url, stream=True, timeout=timeout) as r:
        r.raise_for_status()
        with out_path.open("wb") as f:
            for chunk in r.iter_content(chunk_size=1024 * 256):
                if chunk:
                    f.write(chunk)

def get_text(url: str, timeout: int = 180) -> str:
    r = requests.get(url, timeout=timeout)
    r.raise_for_status()
    return r.text
