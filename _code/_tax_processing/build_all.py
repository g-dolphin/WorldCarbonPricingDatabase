from __future__ import annotations
import argparse
from pathlib import Path
import importlib
import sys

TAX_SCHEMES_DIR = Path(__file__).resolve().parent / "tax_schemes"

def _discover_schemes() -> list[str]:
    schemes = []
    for p in TAX_SCHEMES_DIR.iterdir():
        if not p.is_dir():
            continue
        if (p / "build.py").exists():
            schemes.append(p.name)
    return sorted(schemes)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default=str(Path("_raw/_preproc/_preproc_tax/seeds")))
    ap.add_argument("--download-artifacts", action="store_true")
    ap.add_argument("--with-6akap", action="store_true", help="Sweden only")
    args = ap.parse_args()

    out_root = Path(args.out)
    out_root.mkdir(parents=True, exist_ok=True)

    for scheme_id in _discover_schemes():
        mod = importlib.import_module(f"tax_schemes.{scheme_id}.build")
        out = out_root / scheme_id
        out.mkdir(exist_ok=True)
        old = sys.argv[:]
        sys.argv = ["build.py", "--out", str(out)]
        if args.download_artifacts:
            sys.argv.append("--download-artifacts")
        if scheme_id == "swe_tax" and args.with_6akap:
            sys.argv.append("--with-6akap")
        try:
            mod.main()
        finally:
            sys.argv = old

if __name__ == "__main__":
    main()
