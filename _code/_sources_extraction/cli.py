from __future__ import annotations
import argparse
from pathlib import Path
from .config import load_sources
from .fetch import fetch_source

def main() -> None:
    parser = argparse.ArgumentParser(prog="wcpd-upstream")
    parser.add_argument("command", choices=["fetch-all", "fetch-one"], help="What to run")
    parser.add_argument("--sources", default="_raw/upstream/sources.csv", help="Path to sources.csv")
    parser.add_argument("--raw-root", default="_raw/upstream", help="Root folder for raw artifacts")
    parser.add_argument("--source-id", help="Source ID for fetch-one")
    args = parser.parse_args()

    sources = load_sources(args.sources)
    raw_root = Path(args.raw_root)

    if args.command == "fetch-all":
        for src in sources:
            if not src.active:
                continue
            print(f"Fetching {src.source_id} ({src.url})...")
            try:
                fetch_source(src, raw_root)
            except Exception as exc:  # noqa: BLE001
                print(f"  ERROR fetching {src.source_id}: {exc}")
    elif args.command == "fetch-one":
        if not args.source_id:
            raise SystemExit("--source-id is required for fetch-one")
        match = [s for s in sources if s.source_id == args.source_id]
        if not match:
            raise SystemExit(f"No source found with source_id={args.source_id}")
        fetch_source(match[0], raw_root)
    else:
        raise SystemExit(f"Unknown command: {args.command}")

if __name__ == "__main__":
    main()
