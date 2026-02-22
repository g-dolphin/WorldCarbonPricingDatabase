from __future__ import annotations

import argparse
from pathlib import Path
import importlib
import sys

HERE = Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))

from tax_processing import main as build_final_tables


TAX_SCHEMES_DIR = Path(__file__).resolve().parent / "tax_schemes"


def _discover_schemes() -> list[str]:
    schemes = []
    for p in TAX_SCHEMES_DIR.iterdir():
        if not p.is_dir():
            continue
        if (p / "build.py").exists():
            schemes.append(p.name)
    return sorted(schemes)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--seeds-root", default=str(Path("_raw/_preproc/_preproc_tax/seeds")))
    ap.add_argument("--out-root", default=str(Path("_raw/_preproc/_preproc_tax/out")))
    ap.add_argument("--scheme", action="append", help="Run only these scheme IDs")
    ap.add_argument("--download-artifacts", action="store_true")
    ap.add_argument("--with-6akap", action="store_true", help="Swe tax only")
    args = ap.parse_args()

    seeds_root = Path(args.seeds_root)
    out_root = Path(args.out_root)
    seeds_root.mkdir(parents=True, exist_ok=True)
    out_root.mkdir(parents=True, exist_ok=True)

    schemes = args.scheme or _discover_schemes()
    for scheme_id in schemes:
        mod = importlib.import_module(f"tax_schemes.{scheme_id}.build")
        seeds_dir = seeds_root / scheme_id
        out_dir = out_root / scheme_id
        seeds_dir.mkdir(exist_ok=True)
        out_dir.mkdir(exist_ok=True)

        # Run seed builder
        argv = ["build.py", "--out", str(seeds_dir)]
        if args.download_artifacts:
            argv.append("--download-artifacts")
        if scheme_id == "swe_tax" and args.with_6akap:
            argv.append("--with-6akap")
        old = sys.argv[:]
        sys.argv = argv
        try:
            mod.main()
        finally:
            sys.argv = old

        # Build final tables from seeds
        build_final_tables(str(seeds_dir), str(out_dir), scheme_id)


if __name__ == "__main__":
    main()
