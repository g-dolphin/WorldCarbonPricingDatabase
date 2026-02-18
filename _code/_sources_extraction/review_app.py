# _code/upstream/review_app.py

from __future__ import annotations

import copy
import datetime as dt
import difflib
import importlib.util
import json
import os
import pprint
import subprocess
import hashlib
import base64
import uuid
from pathlib import Path
from urllib.parse import urlparse
from typing import Any, Iterable, Optional

import httpx
import pandas as pd
import streamlit as st
from streamlit.components.v1 import html as st_html

# -------------------------------------------------------------------
# Paths / constants
# -------------------------------------------------------------------

RAW_ROOT = Path("_raw/sources")
CAND_PATH = RAW_ROOT / "cp_candidates.csv"
REVIEW_PATH = RAW_ROOT / "cp_review_state.csv"
DISCOVERY_PATH = RAW_ROOT / "discovery_candidates.csv"
SOURCES_PATH = RAW_ROOT / "sources.csv"  # or sources_master.csv later
SCHEME_PATH = Path("_raw/_aux_files/scheme_description.csv")
RAW_DB_ROOT = Path("_raw")
RAW_PRICE_DIR = RAW_DB_ROOT / "price"
RAW_SCOPE_DIR = RAW_DB_ROOT / "scope"
RAW_REBATES_DIR = RAW_DB_ROOT / "priceRebates" / "tax"
RAW_STRUCTURE_DIR = RAW_DB_ROOT / "_aux_files" / "wcpd_structure"
IPCC_MAP_PATH = RAW_DB_ROOT / "_aux_files" / "ipcc2006_iea_category_codes.csv"
ECP_IPCC_MAP_PATH = Path(
    "/Users/geoffroydolphin/GitHub/ECP/_raw/_aux_files/ipcc2006_iea_category_codes.csv"
)
JURIS_GROUPS_PATH = RAW_DB_ROOT / "_aux_files" / "jurisdiction_groups.json"
DATASET_ROOT = Path("_dataset/data")
ETS_PRICE_UTIL_PATH = Path("_code/_compilation/_utils/ets_prices.py")

GAS_OPTIONS = {
    "CO2": "CO2",
    "CH4": "CH4",
    "N2O": "N2O",
    "F-GASES": "Fgases",
}

SERPAPI_KEY_ENV = "SERPAPI_KEY"
SCHEME_COLUMNS = [
    "scheme_id",
    "scheme_name",
    "scheme_type",
    "implementing_legislation",
    "legislation_year",
    "implementation_year",
    "ghg",
    "sector",
    "source",
    "comment",
]

REQUIRED_SOURCE_COLUMNS = [
    "source_id",
    "jurisdiction",
    "scheme_id",
    "document_type",
    "url",
    "source_type",
    "doc_pattern",
    "doc_link_selector",
    "year_url_template",
    "access_method",
    "parsing_strategy",
    "change_frequency",
    "active",
    "title",
    "institution",
    "year",
    "citation_key",
    "notes",
    "last_seen_year",
    "current_year_covered",
    "release_month",
    "last_checked",
    "next_check_due",
]

def _resolve_logo_path() -> Path | None:
    candidates = [
        Path("/Users/geoffroydolphin/GitHub/wcpd_dashboard/frontend/public/wcpd_new_2_tm.png"),
        Path("/Users/geoffroydolphin/GitHub/wcpd-dashboard/frontend/public/wcpd_new_2_tm.png"),
        Path("/Users/geoffroydolphin/GitHub/wcpd-dashboard/frontend/public/wcpd_new_2.png"),
    ]
    for path in candidates:
        if path.exists():
            return path
    return None


WCPD_DASHBOARD_LOGO = _resolve_logo_path()

# -------------------------------------------------------------------
# Shared loaders (cached)
# -------------------------------------------------------------------


def _candidates_signature() -> tuple[int, int]:
    if not CAND_PATH.exists():
        return (0, 0)
    stat = CAND_PATH.stat()
    return (stat.st_mtime_ns, stat.st_size)


@st.cache_data
def load_candidates(cand_sig: tuple[int, int] | None = None) -> pd.DataFrame:
    _ = cand_sig  # cache key only
    if not CAND_PATH.exists():
        return pd.DataFrame()
    df = pd.read_csv(CAND_PATH, dtype=str)
    if "numeric_value" in df.columns:
        df["numeric_value"] = pd.to_numeric(df["numeric_value"], errors="coerce")
    return df


def _discovery_signature() -> tuple[int, int]:
    if not DISCOVERY_PATH.exists():
        return (0, 0)
    stat = DISCOVERY_PATH.stat()
    return (stat.st_mtime_ns, stat.st_size)


@st.cache_data
def load_discovery_candidates(sig: tuple[int, int] | None = None) -> pd.DataFrame:
    _ = sig  # cache key only
    if not DISCOVERY_PATH.exists():
        return pd.DataFrame()
    return pd.read_csv(DISCOVERY_PATH, dtype=str)


@st.cache_data
def load_review_state() -> pd.DataFrame:
    if not REVIEW_PATH.exists():
        return pd.DataFrame(
            columns=[
                "review_entry_id",
                "candidate_id",
                "decision",
                "edited_value",
                "edited_numeric_value",
                "edited_currency",
                "edited_unit",
                "edited_effective_date",
                "edited_end_date",
                "edited_variable",
                "edited_year",
                "edited_ghg",
                "edited_product",
                "edited_ipcc",
                "edited_jurisdiction",
                "reviewer",
                "reviewed_at",
                "comment",
            ]
        )
    df = pd.read_csv(REVIEW_PATH, dtype=str)
    if "review_entry_id" not in df.columns:
        df["review_entry_id"] = ""
    df["review_entry_id"] = df["review_entry_id"].fillna("")
    if not df.empty:
        missing = df["review_entry_id"] == ""
        if missing.any():
            df.loc[missing, "review_entry_id"] = [
                f"{cid}-legacy-{i}"
                for i, cid in enumerate(df.loc[missing, "candidate_id"].fillna(""))
            ]
    return df


@st.cache_data
def load_meta() -> pd.DataFrame:
    meta_paths = list(RAW_ROOT.glob("*/meta/raw_artifacts.csv"))
    if not meta_paths:
        return pd.DataFrame()
    frames = []
    for path in meta_paths:
        try:
            frames.append(pd.read_csv(path, dtype=str))
        except Exception:
            continue
    if not frames:
        return pd.DataFrame()
    return pd.concat(frames, ignore_index=True)


def _meta_paths() -> list[Path]:
    return list(RAW_ROOT.glob("*/meta/raw_artifacts.csv"))


@st.cache_data
def load_sources() -> pd.DataFrame:
    if SOURCES_PATH.exists():
        df = pd.read_csv(SOURCES_PATH, dtype=str)
        if "jurisdiction" not in df.columns and "jurisdiction_code" in df.columns:
            df = df.rename(columns={"jurisdiction_code": "jurisdiction"})
        if "scheme_id" not in df.columns and "instrument_id" in df.columns:
            df = df.rename(columns={"instrument_id": "scheme_id"})
        # ensure all required columns exist
        for col in REQUIRED_SOURCE_COLUMNS:
            if col not in df.columns:
                df[col] = ""
        return df
    return pd.DataFrame(columns=REQUIRED_SOURCE_COLUMNS)


@st.cache_data
def load_schemes() -> pd.DataFrame:
    if SCHEME_PATH.exists():
        return pd.read_csv(SCHEME_PATH, dtype=str)
    return pd.DataFrame()


@st.cache_data
def load_scheme_description() -> pd.DataFrame:
    if SCHEME_PATH.exists():
        return pd.read_csv(SCHEME_PATH, dtype=str)
    return pd.DataFrame()


@st.cache_data
def load_scheme_metadata() -> pd.DataFrame:
    schemes = load_scheme_description()
    sources = load_sources()

    base = schemes.copy()
    if base.empty:
        base = pd.DataFrame(columns=SCHEME_COLUMNS)
    for col in SCHEME_COLUMNS:
        if col not in base.columns:
            base[col] = ""

    meta = base.copy()

    jurisdiction_map: dict[str, set[str]] = {}
    source_counts: dict[str, int] = {}
    if not sources.empty:
        for _, row in sources.iterrows():
            schemes = _split_jurisdictions(row.get("scheme_id", ""))
            jurisdictions = _split_jurisdictions(row.get("jurisdiction", ""))
            if not schemes:
                continue
            for sid in schemes:
                source_counts[sid] = source_counts.get(sid, 0) + 1
                if jurisdictions:
                    jurisdiction_map.setdefault(sid, set()).update(jurisdictions)

    meta["jurisdiction"] = meta["scheme_id"].apply(
        lambda s: ", ".join(sorted(jurisdiction_map.get(str(s).strip(), set())))
    )
    meta["source_count"] = meta["scheme_id"].apply(
        lambda s: source_counts.get(str(s).strip(), 0)
    )
    meta["has_sources"] = meta["source_count"].apply(lambda v: bool(v))
    return meta


def _normalize_gas_token(value: str) -> str:
    token = str(value).strip().upper()
    if token in {"CO2", "CH4", "N2O"}:
        return token
    if "HFC" in token or "PFC" in token or "SF6" in token or "F-GAS" in token or "FGAS" in token:
        return "F-GASES"
    return ""


@st.cache_data
def load_expected_schemes_for_gas(
    gas_label: str, target_year: int | None = None
) -> list[str]:
    schemes = load_scheme_metadata()
    if schemes.empty:
        return []
    gas_key = _normalize_gas_token(gas_label)
    if not gas_key:
        return []
    out: list[str] = []
    for _, row in schemes.iterrows():
        scheme_id = str(row.get("scheme_id", "")).strip()
        if not scheme_id:
            continue
        if target_year is not None:
            raw_year = str(row.get("implementation_year", "")).strip()
            if raw_year and raw_year.replace(".", "").isdigit():
                try:
                    if int(float(raw_year)) > target_year:
                        continue
                except ValueError:
                    pass
        ghg_raw = str(row.get("ghg", "")).strip()
        if not ghg_raw:
            continue
        tokens = [_normalize_gas_token(t) for t in ghg_raw.split(",")]
        if gas_key in tokens:
            out.append(scheme_id)
    return sorted(set(out))


@st.cache_data
def load_scheme_type_map() -> dict[str, str]:
    meta = load_scheme_metadata()
    if meta.empty:
        return {}
    out: dict[str, str] = {}
    for _, row in meta.iterrows():
        scheme_id = str(row.get("scheme_id", "")).strip()
        scheme_type = str(row.get("scheme_type", "")).strip().lower()
        if scheme_id and scheme_type:
            out[scheme_id] = scheme_type
    return out


@st.cache_data
def load_instrument_options() -> list[str]:
    schemes = load_scheme_metadata()
    if schemes.empty or "scheme_id" not in schemes.columns:
        return []
    values = schemes["scheme_id"].dropna().astype(str).tolist()
    return sorted({v.strip() for v in values if v.strip()})


def _normalize_url(url: str) -> str:
    if not url:
        return ""
    parsed = urlparse(url)
    if not parsed.scheme or not parsed.netloc:
        return url.strip()
    normalized = parsed._replace(fragment="").geturl()
    if normalized.endswith("/") and len(normalized) > len(parsed.scheme) + 3:
        normalized = normalized.rstrip("/")
    return normalized


def _candidate_id(url: str, method: str) -> str:
    digest = hashlib.md5(url.encode("utf-8")).hexdigest()[:10]
    return f"{method}-{digest}"


def _doc_type_token(document_type: str) -> str:
    mapping = {
        "legislation": "LEG",
        "official_publication": "GOV",
        "webpage": "WEB",
        "news": "NEWS",
        "report": "REP",
    }
    return mapping.get(document_type, "src")


def _normalize_source_prefix(value: str) -> str:
    if not value:
        return "SRC"
    clean = "".join(ch if ch.isalnum() else "-" for ch in value.upper())
    while "--" in clean:
        clean = clean.replace("--", "-")
    clean = clean.strip("-")
    return clean or "SRC"


def _split_jurisdictions(value: str) -> list[str]:
    if not value:
        return []
    raw = str(value)
    parts: list[str] = []
    for chunk in raw.replace(";", ",").split(","):
        part = chunk.strip()
        if part:
            parts.append(part)
    return parts


def _build_jurisdiction_prefix_map(df: pd.DataFrame) -> dict[str, str]:
    prefix_map: dict[str, dict[str, int]] = {}
    if df.empty or "source_id" not in df.columns or "jurisdiction" not in df.columns:
        return {}
    for _, row in df.iterrows():
        jurisdiction = str(row.get("jurisdiction", "")).strip()
        source_id = str(row.get("source_id", "")).strip()
        if not jurisdiction or not source_id:
            continue
        parts = source_id.split("-")
        if len(parts) < 3:
            continue
        prefix = "-".join(parts[:-2])
        prefix_map.setdefault(jurisdiction, {})
        prefix_map[jurisdiction][prefix] = prefix_map[jurisdiction].get(prefix, 0) + 1
    out: dict[str, str] = {}
    for jurisdiction, counts in prefix_map.items():
        prefix = sorted(counts.items(), key=lambda x: -x[1])[0][0]
        out[jurisdiction] = prefix
    return out


def _suggest_source_id(
    jurisdiction: str,
    document_type: str,
    existing_ids: set[str],
    prefix_map: dict[str, str] | None = None,
) -> str:
    prefix_map = prefix_map or {}
    prefix = prefix_map.get(jurisdiction, _normalize_source_prefix(jurisdiction))
    token = _doc_type_token(document_type)
    base = f"{prefix}-{token}"
    max_n = 0
    for sid in existing_ids:
        if not sid.startswith(f"{base}-"):
            continue
        tail = sid.split("-")[-1]
        if tail.isdigit():
            max_n = max(max_n, int(tail))
    return f"{base}-{max_n + 1:03d}"


def _valid_source_id(source_id: str) -> tuple[bool, str]:
    source_id = str(source_id or "").strip()
    if not source_id:
        return False, "source_id is required."
    parts = source_id.split("-")
    if len(parts) < 3:
        return False, "source_id must have at least three parts separated by '-'"
    token = parts[-2]
    seq = parts[-1]
    valid_tokens = {
        _doc_type_token("legislation"),
        _doc_type_token("official_publication"),
        _doc_type_token("webpage"),
        _doc_type_token("news"),
        _doc_type_token("report"),
    }
    if token not in valid_tokens:
        return False, f"source_id doc type token must be one of: {', '.join(sorted(valid_tokens))}"
    if not (seq.isdigit() and len(seq) == 3):
        return False, "source_id sequence must be a 3-digit number (e.g., 001)"
    prefix = "-".join(parts[:-2])
    if not prefix or any(not seg.isalnum() for seg in prefix.split("-")):
        return False, "source_id prefix must be alphanumeric segments (A-Z/0-9) separated by '-'"
    if source_id.upper() != source_id:
        return False, "source_id must be uppercase"
    return True, ""


def _normalize_source_id(source_id: str) -> str:
    raw = str(source_id or "").strip()
    if not raw:
        return ""
    raw = raw.replace(" ", "-").replace("_", "-")
    while "--" in raw:
        raw = raw.replace("--", "-")
    raw = raw.upper()
    parts = raw.split("-")
    if len(parts) >= 3 and parts[-1].isdigit():
        parts[-1] = parts[-1].zfill(3)
        raw = "-".join(parts)
    return raw


def _build_citation_key(document_type: str, institution: str, year: str) -> str:
    parts = [document_type, institution, year]
    cleaned: list[str] = []
    for part in parts:
        token = str(part).strip()
        if not token:
            continue
        token = token.replace(" ", "")
        cleaned.append(token)
    return "-".join(cleaned)


def _append_discovery_candidates(rows: list[dict[str, str]]) -> int:
    if not rows:
        return 0
    fieldnames = [
        "candidate_id",
        "url",
        "title",
        "year_guess",
        "jurisdiction_code",
        "instrument_id",
        "doc_hint",
        "method",
        "source_seed",
        "discovered_at",
        "score",
    ]
    if DISCOVERY_PATH.exists():
        existing = pd.read_csv(DISCOVERY_PATH, dtype=str)
    else:
        existing = pd.DataFrame(columns=fieldnames)
    existing_urls = {
        _normalize_url(u)
        for u in existing.get("url", pd.Series(dtype=str)).dropna().astype(str)
        if str(u).strip()
    }
    now = dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds")
    new_rows: list[dict[str, str]] = []
    for row in rows:
        url = str(row.get("url", "")).strip()
        if not url:
            continue
        normalized = _normalize_url(url)
        if not normalized or normalized in existing_urls:
            continue
        method = str(row.get("method", "serpapi")).strip() or "serpapi"
        new_rows.append(
            {
                "candidate_id": _candidate_id(url, method),
                "url": url,
                "title": str(row.get("title", "")).strip(),
                "year_guess": str(row.get("year_guess", "")).strip(),
                "jurisdiction_code": str(row.get("jurisdiction_code", "")).strip(),
                "instrument_id": str(row.get("instrument_id", "")).strip(),
                "doc_hint": "pdf" if url.lower().endswith(".pdf") else "html",
                "method": method,
                "source_seed": str(row.get("source_seed", "")).strip(),
                "discovered_at": now,
                "score": str(row.get("score", "")).strip(),
            }
        )
        existing_urls.add(normalized)
    if not new_rows:
        return 0
    combined = pd.concat([existing, pd.DataFrame(new_rows)], ignore_index=True)
    combined = combined[fieldnames]
    DISCOVERY_PATH.parent.mkdir(parents=True, exist_ok=True)
    combined.to_csv(DISCOVERY_PATH, index=False)
    return len(new_rows)


@st.cache_data
def _icap_price_signature() -> tuple[int, int, int]:
    if not RAW_PRICE_DIR.exists():
        return (0, 0, 0)
    icap_dir = RAW_PRICE_DIR / "_icap"
    if not icap_dir.exists():
        return (0, 0, 0)
    csv_files = sorted(icap_dir.glob("*.csv"))
    if not csv_files:
        return (0, 0, 0)
    latest = max(csv_files, key=lambda p: p.stat().st_mtime_ns)
    stat = latest.stat()
    return (stat.st_mtime_ns, stat.st_size, len(csv_files))


@st.cache_data
def load_raw_icap_price_presence(
    target_year: int, gas_label: str, icap_sig: tuple[int, int, int] | None = None
) -> set[str]:
    _ = icap_sig  # cache key only
    present: set[str] = set()
    if not ETS_PRICE_UTIL_PATH.exists():
        return present
    try:
        spec = importlib.util.spec_from_file_location("ets_prices_util", ETS_PRICE_UTIL_PATH)
        if spec is None or spec.loader is None:
            return present
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        if not hasattr(module, "load_ets_prices"):
            return present
        extra_df = module.load_ets_prices(str(RAW_PRICE_DIR))
        if not isinstance(extra_df, pd.DataFrame):
            return present
        if not {"scheme_id", "year"}.issubset(extra_df.columns):
            return present
        target = str(target_year)
        gas_key = str(gas_label).strip().upper()
        year_mask = extra_df["year"].astype(str).str.strip() == target
        if "ghg" in extra_df.columns:
            ghg_mask = (
                extra_df["ghg"]
                .astype(str)
                .str.strip()
                .str.upper()
                == gas_key
            )
        else:
            ghg_mask = pd.Series([True] * len(extra_df), index=extra_df.index)
        if "allowance_price" in extra_df.columns:
            price_mask = extra_df["allowance_price"].notna()
        else:
            price_mask = pd.Series([True] * len(extra_df), index=extra_df.index)
        matches = extra_df.loc[
            year_mask & ghg_mask & price_mask, "scheme_id"
        ].dropna().astype(str)
        for value in matches:
            value = value.strip()
            if value:
                present.add(value)
    except Exception:
        return present
    return present


@st.cache_data
def load_raw_price_presence(
    target_year: int, gas_label: str, icap_sig: tuple[int, int, int] | None = None
) -> set[str]:
    _ = icap_sig  # cache key only
    present: set[str] = set()
    if not RAW_PRICE_DIR.exists():
        return present
    target = str(target_year)
    gas_key = str(gas_label).strip().upper()
    scheme_type_map = load_scheme_type_map()
    # ------------------------------------------------------------------
    # Standard raw price CSVs (flat files under _raw/price)
    # ------------------------------------------------------------------
    for path in RAW_PRICE_DIR.glob("*.csv"):
        try:
            df = pd.read_csv(path, dtype=str)
        except Exception:
            continue
        if not {"scheme_id", "year"}.issubset(df.columns):
            continue
        has_rate = "rate" in df.columns
        has_allowance = "allowance_price" in df.columns
        year_mask = df["year"].astype(str).str.strip() == target
        if not year_mask.any():
            continue
        if "ghg" in df.columns:
            ghg_mask = df["ghg"].astype(str).str.strip().str.upper() == gas_key
        else:
            ghg_mask = pd.Series([True] * len(df), index=df.index)
        matches = df.loc[year_mask & ghg_mask, "scheme_id"].dropna().astype(str)
        for value in matches:
            value = value.strip()
            if value:
                scheme_type = scheme_type_map.get(value)
                if scheme_type == "tax" and not has_rate:
                    continue
                if scheme_type == "ets" and not has_allowance:
                    continue
                if scheme_type is None or scheme_type == "":
                    if has_rate and not has_allowance:
                        present.add(value)
                        continue
                    if has_allowance and not has_rate:
                        present.add(value)
                        continue
                    if has_allowance and has_rate:
                        present.add(value)
                        continue
                else:
                    present.add(value)

    # ------------------------------------------------------------------
    # ICAP ETS prices (processed via compilation utils to assign scheme_id)
    # ------------------------------------------------------------------
    present |= load_raw_icap_price_presence(target_year, gas_label, icap_sig)
    return present


@st.cache_data
def load_raw_coverage_presence(target_year: int, gas_label: str) -> set[str]:
    present: set[str] = set()
    gas_dir = RAW_DB_ROOT / "coverageFactor" / GAS_OPTIONS.get(gas_label, "")
    if not gas_dir.exists():
        return present
    target = str(target_year)
    for path in gas_dir.glob("*.csv"):
        try:
            df = pd.read_csv(path, dtype=str)
        except Exception:
            continue
        if not {"scheme_id", "year"}.issubset(df.columns):
            continue
        year_mask = df["year"].astype(str).str.strip() == target
        if not year_mask.any():
            continue
        matches = df.loc[year_mask, "scheme_id"].dropna().astype(str)
        for value in matches:
            value = value.strip()
            if value:
                present.add(value)
    return present


def _scope_year_present(scope_map: dict, target_year: int) -> bool:
    if not isinstance(scope_map, dict):
        return False
    return target_year in scope_map or str(target_year) in scope_map


@st.cache_data
def load_raw_scope_presence(target_year: int, gas_label: str) -> set[str]:
    present: set[str] = set()
    gas_key = GAS_OPTIONS.get(gas_label, "")
    if not gas_key:
        return present
    scope_files = [
        RAW_SCOPE_DIR / "ets" / f"ets_scope_{gas_key}.py",
        RAW_SCOPE_DIR / "tax" / f"taxes_scope_{gas_key}.py",
    ]
    for path in scope_files:
        if not path.exists():
            continue
        spec = importlib.util.spec_from_file_location(f"scope_{path.stem}", path)
        if spec is None or spec.loader is None:
            continue
        module = importlib.util.module_from_spec(spec)
        try:
            spec.loader.exec_module(module)
        except Exception:
            continue
        if not hasattr(module, "scope"):
            continue
        try:
            data_block = module.scope()
        except Exception:
            continue
        if not isinstance(data_block, dict):
            continue
        scheme_map = data_block.get("data")
        if not isinstance(scheme_map, dict):
            continue
        for scheme_id, block in scheme_map.items():
            if not isinstance(block, dict):
                continue
            if _scope_year_present(block.get("jurisdictions", {}), target_year):
                present.add(str(scheme_id))
                continue
            if _scope_year_present(block.get("sectors", {}), target_year):
                present.add(str(scheme_id))
                continue
            if _scope_year_present(block.get("fuels", {}), target_year):
                present.add(str(scheme_id))
                continue
    return present


@st.cache_data
def load_dataset_presence(target_year: int, gas_label: str) -> set[str]:
    present: set[str] = set()
    gas_dir = DATASET_ROOT / GAS_OPTIONS.get(gas_label, "")
    if not gas_dir.exists():
        return present
    target = str(target_year)
    for subdir in ("national", "subnational"):
        folder = gas_dir / subdir
        if not folder.exists():
            continue
        for path in folder.glob("*.csv"):
            try:
                df = pd.read_csv(path, dtype=str)
            except Exception:
                continue
            if "year" not in df.columns:
                continue
            year_mask = df["year"].astype(str).str.strip() == target
            if not year_mask.any():
                continue
            for col in ("tax_id", "ets_id", "ets_2_id"):
                if col not in df.columns:
                    continue
                values = df.loc[year_mask, col].dropna().astype(str)
                for value in values:
                    value = value.strip()
                    if value and value.upper() not in {"NA", "NAN"}:
                        present.add(value)
    return present


@st.cache_data
def load_dataset_scheme_ids() -> set[str]:
    present: set[str] = set()
    if not DATASET_ROOT.exists():
        return present
    for gas_dir in DATASET_ROOT.iterdir():
        if not gas_dir.is_dir():
            continue
        for subdir in ("national", "subnational"):
            folder = gas_dir / subdir
            if not folder.exists():
                continue
            for path in folder.glob("*.csv"):
                try:
                    df = pd.read_csv(path, dtype=str, usecols=["tax_id", "ets_id", "ets_2_id"])
                except Exception:
                    continue
                for col in ("tax_id", "ets_id", "ets_2_id"):
                    if col not in df.columns:
                        continue
                    values = df[col].dropna().astype(str)
                    for value in values:
                        value = value.strip()
                        if value and value.upper() not in {"NA", "NAN"}:
                            present.add(value)
    return present


def _serpapi_search(
    query: str,
    api_key: str,
    num_results: int,
    hl: str | None,
    gl: str | None,
) -> list[dict[str, str]]:
    params = {
        "engine": "google",
        "q": query,
        "api_key": api_key,
        "num": num_results,
    }
    if hl:
        params["hl"] = hl
    if gl:
        params["gl"] = gl
    resp = httpx.get("https://serpapi.com/search.json", params=params, timeout=30)
    resp.raise_for_status()
    data = resp.json()
    results: list[dict[str, str]] = []
    for item in data.get("organic_results", []) or []:
        link = str(item.get("link", "")).strip()
        if not link:
            continue
        results.append(
            {
                "url": link,
                "title": str(item.get("title", "")).strip(),
                "snippet": str(item.get("snippet", "")).strip(),
            }
        )
    for item in data.get("news_results", []) or []:
        link = str(item.get("link", "")).strip()
        if not link:
            continue
        results.append(
            {
                "url": link,
                "title": str(item.get("title", "")).strip(),
                "snippet": str(item.get("snippet", "")).strip(),
            }
        )
    return results


@st.cache_data
def load_ipcc_codes(gas_label: str) -> list[str]:
    if gas_label == "CO2":
        path = RAW_STRUCTURE_DIR / "wcpd_structure_CO2.csv"
    else:
        path = RAW_STRUCTURE_DIR / "wcpd_structure_nonCO2.csv"
    if not path.exists():
        return []
    df = pd.read_csv(path, dtype=str)
    codes = df.get("ipcc_code")
    if codes is None:
        return []
    return sorted({c for c in codes.dropna().astype(str).tolist()})


@st.cache_data
def load_ipcc_name_map() -> dict[str, str]:
    for path in [IPCC_MAP_PATH, ECP_IPCC_MAP_PATH]:
        if not path.exists():
            continue
        try:
            df = pd.read_csv(path, dtype=str)
        except Exception:
            continue
        if "ipcc_code" not in df.columns:
            continue
        name_map: dict[str, str] = {}
        for _, row in df.iterrows():
            code = str(row.get("ipcc_code", "") or "").strip()
            if not code:
                continue
            fullname = str(row.get("FULLNAME", "") or "").strip()
            codename = str(row.get("CODENAME", "") or "").strip()
            label = fullname or codename
            if label:
                name_map[code] = label
        return name_map
    return {}


@st.cache_data
def load_jurisdiction_groups() -> dict[str, set[str]]:
    if not JURIS_GROUPS_PATH.exists():
        return {}
    try:
        data = json.loads(JURIS_GROUPS_PATH.read_text(encoding="utf-8"))
    except Exception:
        return {}
    if not isinstance(data, dict):
        return {}
    groups: dict[str, set[str]] = {}
    for group, members in data.items():
        if not isinstance(members, list):
            continue
        clean_group = str(group).strip()
        if not clean_group:
            continue
        cleaned = {str(m).strip() for m in members if str(m).strip()}
        if cleaned:
            groups[clean_group] = cleaned
    return groups


def _ipcc_display(code: str, name_map: dict[str, str]) -> str:
    label = name_map.get(str(code).strip(), "")
    if label:
        return f"{code} — {label}"
    return str(code)


def _merge_ipcc_options(options: Iterable[str], defaults: Iterable[str]) -> list[str]:
    merged = {str(o).strip() for o in options if str(o).strip()}
    merged.update({str(d).strip() for d in defaults if str(d).strip()})
    return sorted(merged)


def _expand_jurisdiction_selection(selected: list[str]) -> set[str]:
    group_map = load_jurisdiction_groups()
    expanded: set[str] = set()
    for item in selected:
        if item.startswith("Group: "):
            group = item.replace("Group: ", "", 1)
            expanded.update(group_map.get(group, set()))
        else:
            expanded.add(item)
    return expanded


def _scheme_jurisdiction_map(sources_df: pd.DataFrame) -> dict[str, set[str]]:
    mapping: dict[str, set[str]] = {}
    if sources_df.empty:
        return mapping
    for _, row in sources_df.iterrows():
        schemes = _split_jurisdictions(row.get("scheme_id", ""))
        jurisdictions = set(_split_jurisdictions(row.get("jurisdiction", "")))
        if not schemes or not jurisdictions:
            continue
        for sid in schemes:
            mapping.setdefault(sid, set()).update(jurisdictions)
    return mapping


def _render_manage_sources_shortcut(location: str) -> None:
    if st.button("Go to Manage sources", key=f"manage_sources_{location}"):
        st.session_state["pending_view"] = "Manage sources"
        st.rerun()


def _render_related_discovery_candidates(
    scheme_id: str,
    year: int | None,
    key_prefix: str,
    variable_hint: str | None = None,
) -> None:
    if not scheme_id:
        return
    disc = load_discovery_candidates(_discovery_signature())
    if disc.empty or "instrument_id" not in disc.columns:
        st.caption("No discovery candidates available.")
        return
    q = disc[disc["instrument_id"].astype(str) == str(scheme_id)]
    if year is not None and "year_guess" in q.columns:
        q = q[q["year_guess"].astype(str) == str(year)]
    if q.empty:
        st.caption("No discovery candidates match this scheme/year.")
        return
    st.markdown("**Related discovery candidates**")
    display_cols = [c for c in ["title", "url", "snippet", "year_guess", "source_seed"] if c in q.columns]
    st.dataframe(q[display_cols].head(50), use_container_width=True, height=220)
    if st.button("Open Review candidates with filters", key=f"{key_prefix}_open_review"):
        st.session_state["gap_filter_instrument_id"] = scheme_id
        if year is not None:
            st.session_state["gap_filter_year"] = year
        if variable_hint:
            st.session_state["gap_filter_variable"] = variable_hint
        st.session_state["gap_apply_filters"] = True
        st.session_state["pending_view"] = "Review candidates"
        st.rerun()


def _set_next_actions(message: str, actions: list[str]) -> None:
    st.session_state["next_actions_message"] = message
    st.session_state["next_actions"] = actions


def _run_discovery_action() -> None:
    with st.spinner("Running discovery..."):
        result = subprocess.run(
            ["python3", "-m", "_code._sources_extraction.discover"],
            capture_output=True,
            text=True,
            check=False,
        )
    if result.returncode == 0:
        st.success("Discovery complete. Candidates updated.")
        st.cache_data.clear()
        st.rerun()
    else:
        st.error("Discovery failed. See details below.")
        with st.expander("Discovery error details"):
            st.code((result.stdout or "") + "\n" + (result.stderr or ""))


def _render_next_actions() -> None:
    actions = st.session_state.get("next_actions") or []
    if not actions:
        return
    message = st.session_state.get("next_actions_message", "Next steps")
    st.info(message)
    cols = st.columns(min(3, len(actions)))
    for idx, action in enumerate(actions):
        label = {
            "run_discovery": "Run discovery",
            "open_review": "Open Review candidates",
            "open_manage_sources": "Open Manage sources",
            "open_raw_editor": "Open Raw editor",
        }.get(action, action)
        with cols[idx % len(cols)]:
            if st.button(label, key=f"next_action_{action}_{idx}"):
                if action == "run_discovery":
                    _run_discovery_action()
                elif action == "open_review":
                    st.session_state["pending_view"] = "Review candidates"
                    st.rerun()
                elif action == "open_manage_sources":
                    st.session_state["pending_view"] = "Manage sources"
                    st.rerun()
                elif action == "open_raw_editor":
                    st.session_state["pending_view"] = "Raw editor"
                    st.rerun()
    if st.button("Dismiss next steps"):
        st.session_state.pop("next_actions", None)
        st.session_state.pop("next_actions_message", None)


@st.cache_data
def load_jurisdiction_options() -> list[str]:
    path = Path("_code/_compilation/_utils/jurisdictions.json")
    if not path.exists():
        return []
    try:
        with open(path, "r", encoding="utf-8") as handle:
            data = json.load(handle)
    except Exception:
        return []
    countries = []
    subnationals = []
    if isinstance(data, dict):
        countries = data.get("countries", []) if isinstance(data.get("countries"), list) else []
        sub_map = data.get("subnationals", {})
        if isinstance(sub_map, dict):
            for items in sub_map.values():
                if isinstance(items, list):
                    subnationals.extend(items)
    options = sorted({str(x).strip() for x in countries + subnationals if str(x).strip()})
    return options


@st.cache_data
def load_price_products() -> list[str]:
    products: dict[str, str] = {}
    if RAW_PRICE_DIR.exists():
        for path in RAW_PRICE_DIR.glob("*.csv"):
            try:
                df = pd.read_csv(path, dtype=str)
            except Exception:
                continue
            if "product" in df.columns:
                for raw in df["product"].dropna().astype(str).tolist():
                    value = raw.strip()
                    if not value:
                        continue
                    key = value.casefold()
                    if key not in products:
                        products[key] = value
    if not products:
        products = {
            "coal": "Coal",
            "oil": "Oil",
            "natural gas": "Natural gas",
        }
    return sorted(products.values())


@st.cache_data
def load_year_options() -> list[str]:
    years: set[int] = set()
    if RAW_PRICE_DIR.exists():
        for path in RAW_PRICE_DIR.glob("*.csv"):
            try:
                df = pd.read_csv(path, dtype=str)
            except Exception:
                continue
            if "year" in df.columns:
                for raw in df["year"].dropna().astype(str).tolist():
                    raw = raw.strip()
                    if not raw:
                        continue
                    try:
                        years.add(int(float(raw)))
                    except ValueError:
                        continue
    current = dt.datetime.utcnow().year
    years.update(range(current, current + 6))
    if not years:
        years.update(range(current - 30, current + 6))
    return [str(y) for y in sorted(years)]


def _now_stamp() -> str:
    return dt.datetime.utcnow().strftime("%Y%m%d")


def _timestamped_path(path: Path) -> Path:
    return path.with_name(f"{path.stem}_{_now_stamp()}{path.suffix}")


def _temp_path(path: Path) -> Path:
    return path.with_name(f"{path.stem}_temp{path.suffix}")


def _is_nonempty(value: Any) -> bool:
    if value is None:
        return False
    if isinstance(value, (list, tuple, dict, set)) and len(value) == 0:
        return False
    if isinstance(value, float) and pd.isna(value):
        return False
    text = str(value).strip()
    return text not in {"", "NA", "nan", "None"}


def _load_module_from_path(path: Path, name_prefix: str) -> Any:
    if not path.exists():
        raise FileNotFoundError(f"Missing module at {path}")
    module_name = f"{name_prefix}_{path.stem}_{_now_stamp()}"
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise ImportError(f"Unable to load module from {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _resolve_candidate_path(local_path: str) -> Optional[Path]:
    if not local_path:
        return None
    path = Path(str(local_path))
    if path.is_absolute() and path.exists():
        return path
    candidates = [
        path,
        RAW_ROOT / path,
        Path.cwd() / path,
    ]
    for candidate in candidates:
        if candidate.exists():
            return candidate
    return None


def _read_text_preview(path: Path, max_chars: int = 200000) -> str:
    text = path.read_text(errors="ignore")
    if len(text) > max_chars:
        return text[:max_chars] + "\n\n...[truncated]..."
    return text


def render_candidate_document_panel(row: pd.Series) -> None:
    st.markdown("### Candidate document")
    local_path = row.get("local_path", "")
    fetched_url = row.get("fetched_url", "")

    if fetched_url:
        st.markdown(f"[Open original URL]({fetched_url})")

    if not local_path:
        st.info("No local document path found for this candidate.")
        return

    doc_path = _resolve_candidate_path(str(local_path))
    if not doc_path:
        st.warning(f"Document file not found: {local_path}")
        return

    st.caption(f"Local file: {doc_path}")
    ext = doc_path.suffix.lower()

    if ext == ".pdf":
        data = doc_path.read_bytes()
        encoded = base64.b64encode(data).decode("ascii")
        st_html(
            f'<iframe src="data:application/pdf;base64,{encoded}" '
            'width="100%" height="650"></iframe>',
            height=650,
            scrolling=True,
        )
    elif ext in {".html", ".htm"}:
        html_text = _read_text_preview(doc_path)
        st_html(html_text, height=650, scrolling=True)
    else:
        st.code(_read_text_preview(doc_path), language="text")


def apply_wcpd_branding() -> None:
    st.markdown(
        """
        <style>
        :root {
          --wcpd-banner-blue: #002b66;
          --wcpd-brand-50: #f0f9ff;
          --wcpd-brand-600: #0284c7;
          --wcpd-brand-700: #0369a1;
          --wcpd-neutral-50: #f8fafc;
          --wcpd-neutral-200: #e2e8f0;
          --wcpd-neutral-700: #334155;
          --wcpd-neutral-900: #0f172a;
        }

        .stApp {
          background: linear-gradient(180deg, var(--wcpd-brand-50) 0%, #ffffff 40%);
          color: var(--wcpd-neutral-900);
        }

        section[data-testid="stSidebar"] {
          background: var(--wcpd-banner-blue);
        }
        section[data-testid="stSidebar"] * {
          color: #ffffff;
        }
        section[data-testid="stSidebar"] a {
          color: #edf4ff;
        }

        h1, h2, h3, h4 {
          color: var(--wcpd-banner-blue);
        }

        .stButton > button {
          background: var(--wcpd-banner-blue);
          color: #ffffff;
          border: 1px solid #01214f;
        }
        .stButton > button:hover {
          background: #0e3c85;
          color: #ffffff;
        }

        .stDataFrame, .stTable {
          border: 1px solid var(--wcpd-neutral-200);
        }

        .stTabs [data-baseweb="tab"] {
          color: var(--wcpd-neutral-700);
        }
        .stTabs [data-baseweb="tab"][aria-selected="true"] {
          color: var(--wcpd-banner-blue);
          border-bottom: 2px solid var(--wcpd-banner-blue);
        }

        .wcpd-top-banner {
          background: var(--wcpd-banner-blue);
          color: #ffffff;
          padding: 12px 16px;
          border-radius: 8px;
          margin: 4px 0 10px 0;
          font-weight: 600;
          letter-spacing: 0.2px;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def _scope_file_path(gas_label: str, scheme_type: str) -> Path:
    gas_suffix = GAS_OPTIONS[gas_label]
    if scheme_type == "ets":
        return RAW_SCOPE_DIR / "ets" / f"ets_scope_{gas_suffix}.py"
    if scheme_type == "tax":
        return RAW_SCOPE_DIR / "tax" / f"taxes_scope_{gas_suffix}.py"
    raise ValueError(f"Unknown scheme_type: {scheme_type}")


def load_scope_data(gas_label: str, scheme_type: str) -> dict[str, Any]:
    path = _scope_file_path(gas_label, scheme_type)
    module = _load_module_from_path(path, f"scope_{scheme_type}")
    if not hasattr(module, "scope"):
        raise AttributeError(f"Module {path} missing scope()")
    data_and_sources = module.scope()
    return {
        "data": data_and_sources.get("data", {}),
        "sources": data_and_sources.get("sources", {}),
        "path": path,
    }


def load_rebates_data(gas_label: str) -> dict[str, Any]:
    gas_suffix = GAS_OPTIONS[gas_label]
    path = RAW_REBATES_DIR / f"_price_exemptions_tax_{gas_suffix}.py"
    module = _load_module_from_path(path, "tax_rebates")
    tax_exemptions = getattr(module, "tax_exemptions", [])
    tax_exemptions_sources = getattr(module, "tax_exemptions_sources", [])
    return {
        "exemptions": tax_exemptions,
        "sources": tax_exemptions_sources,
        "path": path,
    }


def _price_file_path(scheme_id: str) -> Path:
    return RAW_PRICE_DIR / f"{scheme_id}_prices.csv"


def _render_scope_module(data: dict[str, Any], sources: dict[str, Any]) -> str:
    data_str = pprint.pformat(data, width=120, sort_dicts=True)
    sources_str = pprint.pformat(sources, width=120, sort_dicts=True)
    return "\n".join(
        [
            "# Auto-generated by review_app.py",
            f"# Generated at {dt.datetime.utcnow().isoformat(timespec='seconds')}Z",
            "",
            "data_and_sources = {",
            f"    \"data\": {data_str},",
            f"    \"sources\": {sources_str},",
            "}",
            "",
            "def scope():",
            "    return data_and_sources",
            "",
        ]
    )


def _render_rebates_module(exemptions: list[Any], sources: list[Any]) -> str:
    ex_str = pprint.pformat(exemptions, width=120, sort_dicts=True)
    src_str = pprint.pformat(sources, width=120, sort_dicts=True)
    return "\n".join(
        [
            "# Auto-generated by review_app.py",
            f"# Generated at {dt.datetime.utcnow().isoformat(timespec='seconds')}Z",
            "",
            f"tax_exemptions = {ex_str}",
            "",
            f"tax_exemptions_sources = {src_str}",
            "",
        ]
    )


def _list_timestamped_versions(path: Path) -> list[Path]:
    pattern = f"{path.stem}_*.{path.suffix.lstrip('.')}"
    return sorted(path.parent.glob(pattern))


def _collect_timestamped_canonicals(search_dir: Path) -> list[Path]:
    canonicals: set[Path] = set()
    if not search_dir.exists():
        return []
    for path in search_dir.glob("*.py"):
        stem = path.stem
        if len(stem) < 9:
            continue
        if stem[-9:-8] != "_":
            continue
        stamp = stem[-8:]
        if not stamp.isdigit():
            continue
        canonical = path.with_name(f"{stem[:-9]}.py")
        canonicals.add(canonical)
    return sorted(canonicals)


def _render_pending_changes_panel() -> None:
    st.subheader("Pending changes")

    price_temp_files: list[Path] = []
    if RAW_PRICE_DIR.exists():
        price_temp_files = sorted(RAW_PRICE_DIR.glob("*_prices_temp.csv"))

    scope_canonicals = []
    if RAW_SCOPE_DIR.exists():
        scope_canonicals.extend(_collect_timestamped_canonicals(RAW_SCOPE_DIR / "ets"))
        scope_canonicals.extend(_collect_timestamped_canonicals(RAW_SCOPE_DIR / "tax"))

    rebate_canonicals = _collect_timestamped_canonicals(RAW_REBATES_DIR)

    if not price_temp_files and not scope_canonicals and not rebate_canonicals:
        st.caption("No temp or timestamped files detected.")
        return

    if price_temp_files:
        st.markdown("**Prices (temp files)**")
        for temp_path in price_temp_files:
            stem = temp_path.stem
            canonical_stem = stem[:-5] if stem.endswith("_temp") else stem
            canonical_path = temp_path.with_name(f"{canonical_stem}{temp_path.suffix}")
            with st.expander(f"{temp_path.name}", expanded=False):
                _promote_temp_price_ui(
                    canonical_path,
                    temp_path,
                    key_prefix=f"pending_price_{canonical_stem}",
                )

    if scope_canonicals:
        st.markdown("**Scope (timestamped files)**")
        for canonical in scope_canonicals:
            with st.expander(f"{canonical.name}", expanded=False):
                _promote_file_ui(canonical, key_prefix=f"pending_scope_{canonical.stem}")

    if rebate_canonicals:
        st.markdown("**Price rebates (timestamped files)**")
        for canonical in rebate_canonicals:
            with st.expander(f"{canonical.name}", expanded=False):
                _promote_file_ui(canonical, key_prefix=f"pending_rebates_{canonical.stem}")


def find_schemes_missing_sources() -> list[str]:
    sources_df = load_sources()
    scheme_ids: set[str] = set()

    if RAW_PRICE_DIR.exists():
        for path in RAW_PRICE_DIR.glob("*.csv"):
            try:
                df = pd.read_csv(path, dtype=str)
            except Exception:
                continue
            if "scheme_id" in df.columns:
                for val in df["scheme_id"].dropna().astype(str).tolist():
                    v = val.strip()
                    if v:
                        scheme_ids.add(v)

    for gas_label in GAS_OPTIONS.keys():
        try:
            ets = load_scope_data(gas_label, "ets")["data"]
            tax = load_scope_data(gas_label, "tax")["data"]
        except Exception:
            ets, tax = {}, {}
        scheme_ids.update(ets.keys())
        scheme_ids.update(tax.keys())

        try:
            rebates = load_rebates_data(gas_label)["exemptions"]
            for ex in rebates:
                scheme_map = ex.get("scheme_id", {})
                for sid in scheme_map.values():
                    v = str(sid).strip()
                    if v:
                        scheme_ids.add(v)
        except Exception:
            pass

    missing: list[str] = []
    for sid in sorted(scheme_ids):
        if not _source_options_for_scheme(sid, sources_df):
            missing.append(sid)
    return missing


def _promote_file_ui(canonical_path: Path, key_prefix: str) -> None:
    st.markdown("### Promote temp file")
    versions = _list_timestamped_versions(canonical_path)
    if not versions:
        st.caption("No timestamped files found.")
        return
    selected = st.selectbox(
        "Select timestamped file to promote",
        options=[str(p) for p in versions],
        key=f"{key_prefix}_promote_select",
    )
    try:
        old_text = canonical_path.read_text(encoding="utf-8", errors="ignore")
    except FileNotFoundError:
        old_text = ""
    new_text = Path(selected).read_text(encoding="utf-8", errors="ignore")
    diff_lines = list(
        difflib.unified_diff(
            old_text.splitlines(),
            new_text.splitlines(),
            fromfile=str(canonical_path),
            tofile=str(selected),
            lineterm="",
        )
    )
    if diff_lines:
        st.markdown("**Diff preview**")
        st.code("\n".join(diff_lines[:400]), language="diff")
        if len(diff_lines) > 400:
            st.caption("Diff truncated to 400 lines.")
    else:
        st.caption("No diff (files identical or canonical missing).")
    confirm = st.checkbox(
        f"Confirm replace {canonical_path}",
        value=False,
        key=f"{key_prefix}_promote_confirm",
    )
    discard = st.button("Discard selected file", key=f"{key_prefix}_discard_button")
    if discard:
        try:
            os.remove(selected)
            st.success(f"Discarded {selected}")
            st.rerun()
        except Exception as exc:
            st.error(f"Failed to discard {selected}: {exc}")
    if st.button("Promote file", key=f"{key_prefix}_promote_button"):
        if not confirm:
            st.error("Please confirm promotion before proceeding.")
            return
        if canonical_path.suffix.lower() == ".csv":
            try:
                df_new = pd.read_csv(selected, dtype=str)
                if "record_date" in df_new.columns:
                    df_new = df_new.drop(columns=["record_date"])
                    df_new.to_csv(canonical_path, index=False)
                    os.remove(selected)
                    st.success(f"Promoted {selected} -> {canonical_path} (record_date removed)")
                    return
            except Exception:
                pass
        os.replace(selected, canonical_path)
        st.success(f"Promoted {selected} -> {canonical_path}")


def _promote_temp_price_ui(canonical_path: Path, temp_path: Path, key_prefix: str) -> None:
    st.markdown("### Promote temp file")
    if not temp_path.exists():
        st.caption("No temp file found.")
        return
    if st.button("Discard temp file", key=f"{key_prefix}_discard_temp"):
        try:
            os.remove(temp_path)
            st.success(f"Discarded {temp_path}")
            st.rerun()
        except Exception as exc:
            st.error(f"Failed to discard {temp_path}: {exc}")
    df_new = None
    try:
        old_text = canonical_path.read_text(encoding="utf-8", errors="ignore")
    except FileNotFoundError:
        old_text = ""
    try:
        df_new = pd.read_csv(temp_path, dtype=str)
        df_preview = df_new.copy()
        if "record_date" in df_preview.columns:
            df_preview = df_preview.drop(columns=["record_date"])
        new_text = df_preview.to_csv(index=False)
    except Exception:
        new_text = temp_path.read_text(encoding="utf-8", errors="ignore")
    diff_lines = list(
        difflib.unified_diff(
            old_text.splitlines(),
            new_text.splitlines(),
            fromfile=str(canonical_path),
            tofile=str(temp_path),
            lineterm="",
        )
    )
    if diff_lines:
        st.markdown("**Diff preview**")
        st.code("\n".join(diff_lines[:400]), language="diff")
        if len(diff_lines) > 400:
            st.caption("Diff truncated to 400 lines.")
    else:
        st.caption("No diff (files identical or canonical missing).")
    confirm = st.checkbox(
        f"Confirm replace {canonical_path}",
        value=False,
        key=f"{key_prefix}_promote_confirm",
    )
    if st.button("Promote file", key=f"{key_prefix}_promote_button"):
        if not confirm:
            st.error("Please confirm promotion before proceeding.")
            return
        if df_new is not None:
            if "record_date" in df_new.columns:
                df_new = df_new.drop(columns=["record_date"])
            df_new.to_csv(canonical_path, index=False)
        else:
            canonical_path.write_text(new_text, encoding="utf-8")
        os.remove(temp_path)
        st.success(f"Promoted {temp_path} -> {canonical_path} (record_date removed)")

def _file_status(path: Path) -> str:
    """Return a short status string for a file."""
    if not path.exists():
        return "❌ missing"
    size = path.stat().st_size
    if size < 1024:
        sz = f"{size} B"
    elif size < 1024 * 1024:
        sz = f"{size / 1024:.1f} KB"
    else:
        sz = f"{size / (1024 * 1024):.2f} MB"
    mtime = dt.datetime.fromtimestamp(path.stat().st_mtime).isoformat(timespec="seconds")
    return f"✅ {sz}, modified {mtime}"

def render_run_status() -> None:
    """Show a small checklist of key upstream files in the sidebar."""
    st.sidebar.markdown("### Run status")

    # Basic file existence/size
    st.sidebar.markdown("**cp_candidates.csv**")
    st.sidebar.caption(_file_status(CAND_PATH))
    if CAND_PATH.exists():
        st.sidebar.caption(str(CAND_PATH.resolve()))

    st.sidebar.markdown("**cp_review_state.csv**")
    st.sidebar.caption(_file_status(REVIEW_PATH))

    st.sidebar.markdown("**raw_artifacts.csv**")
    meta_paths = _meta_paths()
    if not meta_paths:
        st.sidebar.caption("❌ missing")
    else:
        st.sidebar.caption(f"✅ {len(meta_paths)} file(s)")

    st.sidebar.markdown("**sources_with_instruments.csv**")
    st.sidebar.caption(_file_status(SOURCES_PATH))

    st.sidebar.markdown("**scheme_description.csv**")
    st.sidebar.caption(_file_status(SCHEME_PATH))

    # Row counts where possible
    try:
        cand = load_candidates(_candidates_signature())
        if not cand.empty:
            st.sidebar.markdown(f"- Candidates: **{len(cand)}** rows")
    except Exception:
        pass

    try:
        rev = load_review_state()
        if not rev.empty:
            st.sidebar.markdown(f"- Reviewed decisions: **{len(rev)}** rows")
    except Exception:
        pass
    if st.sidebar.button("Refresh candidates"):
        st.cache_data.clear()
        st.rerun()

    missing_sources = find_schemes_missing_sources()
    if missing_sources:
        st.sidebar.markdown("### Source coverage")
        st.sidebar.caption(
            f"Missing sources for {len(missing_sources)} scheme(s) with raw data."
        )
        preview = ", ".join(missing_sources[:10])
        st.sidebar.caption(f"Examples: {preview}")
        if len(missing_sources) > 10:
            st.sidebar.caption("…")


def render_discovery_button() -> None:
    if st.sidebar.button("Run discovery (update candidates)"):
        _run_discovery_action()


# -------------------------------------------------------------------
# Candidate review helpers
# -------------------------------------------------------------------


def merge_all_candidates() -> pd.DataFrame:
    cand = load_candidates(_candidates_signature())
    if cand.empty:
        return cand
    if "scheme_id" not in cand.columns and "instrument_id" in cand.columns:
        cand["scheme_id"] = cand["instrument_id"]
    if "instrument_id" not in cand.columns and "scheme_id" in cand.columns:
        cand["instrument_id"] = cand["scheme_id"]

    meta = load_meta()
    sources = load_sources()
    schemes = load_schemes()
    review = load_review_state()

    # candidate → artifact meta
    if not meta.empty:
        cand = cand.merge(
            meta[["artifact_id", "local_path", "fetched_url"]],
            on="artifact_id",
            how="left",
        )

    # candidate → source meta
    if not sources.empty:
        cand = cand.merge(
            sources[
                [
                    "source_id",
                    "scheme_id",
                    "document_type",
                    "title",
                    "jurisdiction",
                    "year",
                ]
            ].drop_duplicates("source_id"),
            on="source_id",
            how="left",
            suffixes=("", "_src"),
        )
        for col in ["scheme_id", "year", "jurisdiction"]:
            src_col = f"{col}_src"
            if src_col not in cand.columns:
                continue
            if col not in cand.columns:
                cand[col] = cand[src_col]
            else:
                missing = cand[col].isna() | (cand[col].astype(str).str.strip() == "")
                cand.loc[missing, col] = cand.loc[missing, src_col]
            cand = cand.drop(columns=[src_col])

    # candidate → scheme_name / scheme_type
    if not schemes.empty and "scheme_id" in schemes.columns:
        scheme_cols = ["scheme_id", "scheme_name"]
        if "scheme_type" in schemes.columns:
            scheme_cols.append("scheme_type")
        cand = cand.merge(
            schemes[scheme_cols],
            left_on="scheme_id",
            right_on="scheme_id",
            how="left",
        )

    # merge review state
    if not review.empty:
        cand = cand.merge(
            review,
            on="candidate_id",
            how="left",
            suffixes=("", "_rev"),
        )

    # add empty columns for UI convenience
    for col in [
        "review_entry_id",
        "decision",
        "edited_value",
        "edited_numeric_value",
        "edited_currency",
        "edited_unit",
        "edited_effective_date",
        "edited_end_date",
        "edited_variable",
        "edited_year",
        "edited_ghg",
        "edited_product",
        "edited_ipcc",
        "edited_jurisdiction",
        "comment",
    ]:
        if col not in cand.columns:
            cand[col] = ""
        cand[col] = cand[col].fillna("")

    return cand


def save_review_row(row: dict) -> None:
    """Append/update a row in cp_review_state.csv."""
    if REVIEW_PATH.exists():
        df = pd.read_csv(REVIEW_PATH, dtype=str)
    else:
        df = pd.DataFrame(
            columns=[
                "review_entry_id",
                "candidate_id",
                "decision",
                "edited_value",
                "edited_numeric_value",
                "edited_currency",
                "edited_unit",
                "edited_variable",
                "edited_year",
                "edited_ghg",
                "edited_product",
                "edited_ipcc",
                "edited_jurisdiction",
                "reviewer",
                "reviewed_at",
                "comment",
            ]
        )

    for col in row.keys():
        if col not in df.columns:
            df[col] = ""

    if not row.get("review_entry_id"):
        row["review_entry_id"] = f"{row['candidate_id']}-{uuid.uuid4().hex[:8]}"

    mask = df["review_entry_id"] == row["review_entry_id"]
    if mask.any():
        df.loc[mask, :] = row
    else:
        df = pd.concat([df, pd.DataFrame([row])], ignore_index=True)

    df.to_csv(REVIEW_PATH, index=False)


# -------------------------------------------------------------------
# Source manager helpers
# -------------------------------------------------------------------


def save_sources(df: pd.DataFrame) -> None:
    if "instrument_id" in df.columns and "scheme_id" not in df.columns:
        df = df.rename(columns={"instrument_id": "scheme_id"})
    if "instrument_id" in df.columns and "scheme_id" in df.columns:
        df = df.drop(columns=["instrument_id"])
    df.to_csv(SOURCES_PATH, index=False)


def validate_url(url: str) -> tuple[bool, str]:
    url = url.strip()
    if not url.startswith(("http://", "https://")):
        return False, "URL must start with http:// or https://"
    try:
        resp = httpx.head(url, timeout=10, follow_redirects=True)
        return resp.status_code < 400, f"Status {resp.status_code}"
    except Exception as e:
        return False, f"Error: {e}"


# -------------------------------------------------------------------
# Views
# -------------------------------------------------------------------


def review_view(reviewer: str) -> None:
    st.title("WCPD – Upstream Candidate Review")
    _render_next_actions()

    df = merge_all_candidates()
    if df.empty:
        st.warning("No candidates found at _raw/sources/cp_candidates.csv")
        return

    gap_scheme = st.session_state.get("gap_filter_instrument_id")
    gap_year = st.session_state.get("gap_filter_year")
    gap_variable = st.session_state.get("gap_filter_variable")
    apply_gap_filters = bool(st.session_state.get("gap_apply_filters"))

    if gap_scheme or gap_year or gap_variable:
        st.info(
            "Gap dashboard filters applied. Use the sidebar to adjust or clear below."
        )
        if st.button("Clear gap filters"):
            st.session_state.pop("gap_filter_instrument_id", None)
            st.session_state.pop("gap_filter_year", None)
            st.session_state.pop("gap_filter_variable", None)
            st.session_state.pop("gap_apply_filters", None)
            st.rerun()

    # Sidebar filters
    schemes = []
    scheme_meta = load_scheme_metadata()
    if not scheme_meta.empty and "scheme_id" in scheme_meta.columns:
        schemes.extend(
            scheme_meta["scheme_id"].dropna().astype(str).tolist()
        )
    schemes = sorted({s.strip() for s in schemes if str(s).strip()})
    scheme_key = "review_filter_schemes"
    if apply_gap_filters:
        st.session_state[scheme_key] = (
            [gap_scheme] if gap_scheme and gap_scheme in schemes else []
        )
    sel_schemes = st.sidebar.multiselect(
        "Carbon pricing mechanism (instrument_id)", schemes, key=scheme_key
    )
    if len(sel_schemes) == 1:
        st.session_state["current_scheme_id"] = sel_schemes[0]

    # Apply filters
    q = df.copy()
    if sel_schemes:
        q = q[q["instrument_id"].isin(sel_schemes)]

    def variable_label(row: pd.Series) -> str:
        edited = str(row.get("edited_variable", "")).strip()
        if edited:
            return edited
        name = str(row.get("field_name", "")).strip()
        scheme_type = str(row.get("scheme_type", "")).strip().lower()
        if name == "rate":
            return "Tax rate" if scheme_type == "tax" else "Allowance price"
        if name in {"ipcc_category", "start_date"}:
            return "Scope"
        return "Scope"

    q["variable_label"] = q.apply(variable_label, axis=1)

    variable_options = [
        "Tax rate",
        "Allowance price",
        "Coverage factor",
        "Price rebate",
        "Scope",
    ]
    variable_key = "review_filter_variables"
    if apply_gap_filters:
        st.session_state[variable_key] = (
            [gap_variable]
            if gap_variable and gap_variable in variable_options
            else variable_options
        )
    sel_variables = st.sidebar.multiselect(
        "Variable", variable_options, key=variable_key
    )
    st.sidebar.caption(
        "Variable filter only changes which candidate entries are shown, not what a document can contain."
    )
    if sel_variables:
        q = q[q["variable_label"].isin(sel_variables)]

    years = (
        sorted(
            y
            for y in df["year"].dropna().astype(str).unique().tolist()
            if y.strip()
        )
        if "year" in df.columns
        else []
    )
    year_key = "review_filter_years"
    if apply_gap_filters:
        st.session_state[year_key] = (
            [str(gap_year)] if gap_year and str(gap_year) in years else []
        )
    sel_years = st.sidebar.multiselect("Year", years, key=year_key)
    if sel_years and "year" in q.columns:
        q = q[q["year"].astype(str).isin(sel_years)]

    # Jurisdiction filter
    juris_options = (
        sorted({j for v in df["jurisdiction"].dropna().astype(str).tolist() for j in _split_jurisdictions(v)})
        if "jurisdiction" in df.columns
        else []
    )
    group_map = load_jurisdiction_groups()
    group_labels = [f"Group: {g}" for g in sorted(group_map.keys())] if group_map else []
    juris_options = ["All"] + group_labels + juris_options if juris_options else []
    sel_juris = st.sidebar.multiselect(
        "Jurisdiction / group",
        juris_options,
        default=["All"] if juris_options else [],
    )
    if sel_juris and "jurisdiction" in q.columns:
        if "All" not in sel_juris:
            expanded = _expand_jurisdiction_selection(sel_juris)
            q = q[
                q["jurisdiction"]
                .astype(str)
                .apply(lambda v: bool(set(_split_jurisdictions(v)) & expanded))
            ]

    def status_of(row):
        if row.get("decision") in ("accepted", "rejected", "skipped"):
            return row["decision"]
        return "unreviewed"

    q["status"] = q.apply(status_of, axis=1)

    status_options = ["unreviewed", "accepted", "rejected", "skipped"]
    sel_status = st.sidebar.multiselect(
        "Status", status_options, default=["unreviewed"]
    )
    if sel_status:
        q = q[q["status"].isin(sel_status)]

    # Confidence
    min_conf, max_conf = st.sidebar.slider(
        "Confidence range", 0.0, 1.0, (0.0, 1.0), step=0.05
    )
    if "confidence" in q.columns:
        conf = pd.to_numeric(q["confidence"], errors="coerce")
        q = q[(conf >= min_conf - 1e-9) & (conf <= max_conf + 1e-9)]

    # Sorting
    sort_options = []
    for col in ["jurisdiction", "instrument_id", "year", "confidence", "candidate_id"]:
        if col in q.columns:
            sort_options.append(col)
    if sort_options:
        sort_by = st.sidebar.selectbox("Sort by", options=sort_options, index=0)
        sort_order = st.sidebar.radio("Sort order", options=["asc", "desc"], index=0, horizontal=True)
        ascending = sort_order == "asc"
        q = q.sort_values(by=sort_by, ascending=ascending, kind="mergesort")

    st.sidebar.markdown(f"**{len(q)} candidates** after filters")
    st.sidebar.markdown("---")
    _render_manage_sources_shortcut("review_sidebar")

    if apply_gap_filters:
        st.session_state["gap_apply_filters"] = False
        if q.empty:
            st.warning(
                "No review candidates match the selected gap. "
                "Try Manage sources to add a source, or adjust filters."
            )
            return
    if q.empty:
        st.warning(
            "No review candidates match the current filters. "
            "Adjust filters or add sources."
        )
        return

    def _safe_text(value: Any) -> str:
        if value is None or (isinstance(value, float) and pd.isna(value)):
            return ""
        return str(value).strip()

    q["carbon_pricing_mechanism"] = q.apply(
        lambda r: (
            f"{_safe_text(r.get('scheme_name'))} – {_safe_text(r.get('instrument_id'))}"
            if _safe_text(r.get("scheme_name"))
            else _safe_text(r.get("instrument_id"))
        ),
        axis=1,
    )

    # Layout: candidates table then selector
    st.subheader("Candidates")
    show_all_cols = st.checkbox("Show all columns", value=True)
    display_cols = [
        "candidate_id",
        "status",
        "carbon_pricing_mechanism",
        "variable_label",
        "value",
        "numeric_value",
        "currency",
        "unit",
        "confidence",
        "source_id",
    ]
    if show_all_cols:
        display_cols = q.columns.tolist()
    else:
        display_cols = [c for c in display_cols if c in q.columns]
    st.dataframe(
        q[display_cols].reset_index(drop=True),
        height=380,
        use_container_width=True,
    )

    review_entry_container = None
    review_entry_choice = "New entry"
    st.subheader("Select candidate")
    selected_id = st.selectbox(
        "Candidate ID",
        options=q["candidate_id"].tolist(),
    )
    review_entry_container = st.container()

    candidate_rows = q[q["candidate_id"] == selected_id]
    if candidate_rows.empty:
        st.warning("Selected candidate has no rows after filtering.")
        return
    review_entries = [
        r for r in candidate_rows["review_entry_id"].dropna().unique().tolist() if r
    ]
    if review_entry_container is not None:
        options = ["New entry"] + review_entries if review_entries else ["New entry"]
        with review_entry_container:
            review_entry_choice = st.selectbox(
                "Review entry",
                options=options,
            )

    if review_entries and review_entry_choice and review_entry_choice != "New entry":
        row = candidate_rows[candidate_rows["review_entry_id"] == review_entry_choice].iloc[0]
    else:
        row = candidate_rows.iloc[0].copy()
        for col in [
            "review_entry_id",
            "decision",
            "edited_value",
            "edited_numeric_value",
            "edited_currency",
            "edited_unit",
            "edited_effective_date",
            "edited_end_date",
            "edited_variable",
            "edited_year",
            "edited_ghg",
            "edited_product",
            "edited_ipcc",
            "edited_jurisdiction",
            "reviewer",
            "reviewed_at",
            "comment",
        ]:
            if col in row:
                row[col] = ""
    detail_left, detail_right = st.columns([3, 2])
    if row.get("instrument_id"):
        st.session_state["current_scheme_id"] = row.get("instrument_id")

    with detail_left:
        st.subheader("Details & Review")
        st.caption(
            "A single document can include information about multiple variables. Save one entry per variable you confirm or extract."
        )

        st.markdown(
            f"**Candidate:** `{row['candidate_id']}`  |  "
            f"**Carbon pricing mechanism:** `{row.get('instrument_id', '')}` – {row.get('scheme_name', '')}"
        )
        raw_field = str(row.get("field_name", "") or "")
        if raw_field == "ipcc_category":
            raw_field = "ipcc_code"
        st.markdown(f"**Field (raw):** `{raw_field}`")

        field_name = row.get("field_name", "")
        scheme_type = str(row.get("scheme_type", "")).strip().lower()
        ghg_options = list(GAS_OPTIONS.keys())
        fuel_options = load_price_products()
        ipcc_options = sorted(
            set(load_ipcc_codes("CO2")) | set(load_ipcc_codes("CH4"))
        )
        year_options = load_year_options()
        juris_options = sorted(
            {j for v in df["jurisdiction"].dropna().astype(str).tolist() for j in _split_jurisdictions(v)}
        )

        def split_list(value: str) -> list[str]:
            if not value:
                return []
            items: list[str] = []
            for chunk in str(value).split(";"):
                items.extend([p.strip() for p in chunk.split(",")])
            return [p for p in items if p]
        value_default = row.get("edited_value") or row.get("value", "")
        numeric_default = row.get("edited_numeric_value") or row.get(
            "numeric_value", ""
        )
        currency_default = row.get("edited_currency") or row.get("currency", "")
        unit_default = row.get("edited_unit") or row.get("unit", "")
        variable_default = row.get("edited_variable") or ""
        year_default = split_list(row.get("edited_year") or "")
        ghg_default = split_list(row.get("edited_ghg") or "")
        product_default = split_list(row.get("edited_product") or "")
        ipcc_default = split_list(row.get("edited_ipcc") or "")
        jurisdiction_default = split_list(row.get("edited_jurisdiction") or "")
        if field_name == "ipcc_category" and not ipcc_default:
            ipcc_default = split_list(row.get("value") or "")
        ipcc_options = _merge_ipcc_options(ipcc_options, ipcc_default)
        ipcc_name_map = load_ipcc_name_map()
        year_options_all = sorted(set(year_options) | set(year_default))

        def field_ui_config(name: str) -> dict[str, bool]:
            if name == "rate":
                return {
                    "value": True,
                    "numeric": True,
                    "currency": True,
                    "unit": True,
                }
            if name in {"ipcc_category", "start_date"}:
                return {
                    "value": True,
                    "numeric": False,
                    "currency": False,
                    "unit": False,
                }
            return {
                "value": True,
                "numeric": False,
                "currency": False,
                "unit": True,
            }

        cfg = field_ui_config(str(field_name))

        edited_value = str(value_default or "")
        edited_numeric_value = str(numeric_default or "")
        edited_currency = str(currency_default or "")
        edited_unit = str(unit_default or "")
        edited_effective_date = str(row.get("edited_effective_date") or "")
        edited_end_date = str(row.get("edited_end_date") or "")

        rate_label = "Tax rate" if scheme_type == "tax" else "Allowance price"
        variable_options = [rate_label, "Coverage factor", "Price rebate", "Scope"]
        if variable_default and variable_default not in variable_options:
            variable_options.append(variable_default)
        edited_variable = st.selectbox(
            "Variable",
            options=variable_options,
            index=variable_options.index(variable_default)
            if variable_default in variable_options
            else 0,
        )

        if cfg["value"] and cfg["unit"] and not (cfg["numeric"] or cfg["currency"]):
            col1, col2 = st.columns(2)
            with col1:
                edited_value = st.text_input("Value", value=edited_value)
            with col2:
                edited_unit = st.text_input("Unit", value=edited_unit)
        elif cfg["value"] and not (cfg["numeric"] or cfg["currency"] or cfg["unit"]):
            edited_value = st.text_input("Value", value=edited_value)
        else:
            cols = st.columns(4)
            if cfg["value"]:
                with cols[0]:
                    edited_value = st.text_input("Value", value=edited_value)
            if cfg["numeric"]:
                with cols[1]:
                    edited_numeric_value = st.text_input(
                        "Numeric value", value=edited_numeric_value
                    )
            if cfg["currency"]:
                with cols[2]:
                    edited_currency = st.text_input("Currency", value=edited_currency)
            if cfg["unit"]:
                with cols[3]:
                    edited_unit = st.text_input("Unit", value=edited_unit)

        if field_name == "rate" and scheme_type == "tax":
            st.markdown("**Rate change period (optional)**")
            col_dates = st.columns(2)
            with col_dates[0]:
                edited_effective_date = st.text_input(
                    "Effective date (YYYY-MM-DD)",
                    value=edited_effective_date,
                )
            with col_dates[1]:
                edited_end_date = st.text_input(
                    "End date (YYYY-MM-DD)",
                    value=edited_end_date,
                )

        st.markdown("**Applies to**")
        if edited_variable == "Scope":
            if not jurisdiction_default and row.get("jurisdiction"):
                jurisdiction_default = _split_jurisdictions(row.get("jurisdiction"))
            col5, col6 = st.columns(2)
            with col5:
                edited_jurisdiction = st.multiselect(
                    "Jurisdiction",
                    options=juris_options,
                    default=[j for j in jurisdiction_default if j in juris_options],
                )
            with col6:
                edited_year = st.multiselect(
                    "Year",
                    options=year_options_all,
                    default=[y for y in year_default if y in year_options_all],
                )
            col7, col8, col9 = st.columns(3)
            with col7:
                edited_ghg = st.multiselect(
                    "GHG", options=ghg_options, default=ghg_default
                )
            with col8:
                edited_product = st.multiselect(
                    "Fuel / product", options=fuel_options, default=product_default
                )
            with col9:
                edited_ipcc = st.multiselect(
                    "IPCC category",
                    options=ipcc_options,
                    default=ipcc_default,
                    format_func=lambda c: _ipcc_display(c, ipcc_name_map),
                )
        else:
            if not jurisdiction_default and row.get("jurisdiction"):
                jurisdiction_default = _split_jurisdictions(row.get("jurisdiction"))
            col5, col6 = st.columns(2)
            with col5:
                edited_jurisdiction = st.multiselect(
                    "Jurisdiction",
                    options=juris_options,
                    default=[j for j in jurisdiction_default if j in juris_options],
                )
            with col6:
                edited_year = st.multiselect(
                    "Year",
                    options=year_options_all,
                    default=[y for y in year_default if y in year_options_all],
                )
            col7, col8, col9 = st.columns(3)
            with col7:
                edited_ghg = st.multiselect(
                    "GHG", options=ghg_options, default=ghg_default
                )
            with col8:
                edited_product = st.multiselect(
                    "Fuel / product", options=fuel_options, default=product_default
                )
            with col9:
                edited_ipcc = st.multiselect(
                    "IPCC category",
                    options=ipcc_options,
                    default=ipcc_default,
                    format_func=lambda c: _ipcc_display(c, ipcc_name_map),
                )

        st.markdown("**Snippet (context)**")
        st.code(row.get("snippet", ""), language="text")

        comment = st.text_area("Comment", value=row.get("comment") or "", height=80)

        decision = st.radio(
            "Decision",
            options=["accepted", "rejected", "skipped"],
            index={"accepted": 0, "rejected": 1, "skipped": 2}.get(
                row.get("decision"), 0
            ),
            horizontal=True,
        )

        if st.button("Save decision", type="primary"):
            now = dt.datetime.utcnow().isoformat(timespec="seconds")
            review_row = {
                "review_entry_id": row.get("review_entry_id", ""),
                "candidate_id": row["candidate_id"],
                "decision": decision,
                "edited_value": edited_value,
                "edited_numeric_value": edited_numeric_value,
                "edited_currency": edited_currency,
                "edited_unit": edited_unit,
                "edited_effective_date": edited_effective_date,
                "edited_end_date": edited_end_date,
                "edited_variable": edited_variable,
                "edited_year": ";".join(edited_year),
                "edited_ghg": ";".join(edited_ghg),
                "edited_product": ";".join(edited_product),
                "edited_ipcc": ";".join(edited_ipcc),
                "edited_jurisdiction": ";".join(edited_jurisdiction),
                "reviewer": reviewer,
                "reviewed_at": now,
                "comment": comment,
            }
            save_review_row(review_row)
            st.success("Saved.")
            st.rerun()

    with detail_right:
        st.subheader("Context & Files")
        _render_manage_sources_shortcut("review_context")
        scheme_for_sources = str(row.get("instrument_id", "") or "").strip()
        if scheme_for_sources:
            st.markdown("**Source lookup**")
            sources_df = load_sources()
            _render_source_picker(
                "Source",
                scheme_id=scheme_for_sources,
                sources_df=sources_df,
                existing_value="",
                key=f"review_source_lookup_{row.get('candidate_id','')}",
            )
            if st.button("Open Raw editor for this scheme"):
                st.session_state["current_scheme_id"] = scheme_for_sources
                st.session_state["pending_view"] = "Raw editor"
                st.rerun()
        render_candidate_document_panel(row)


def source_manager_view() -> None:
    st.title("WCPD – Source Manager")

    st.markdown(
        "Use this page to **add** or **edit** upstream sources used by the fetcher."
    )
    _render_next_actions()

    df = load_sources()
    schemes = load_schemes()

    # Sidebar filters
    st.sidebar.markdown("---")
    st.sidebar.header("Source filters")

    juris_values = (
        df["jurisdiction"].dropna().astype(str).tolist()
        if "jurisdiction" in df.columns
        else []
    )
    juris_options = sorted({j for v in juris_values for j in _split_jurisdictions(v)})
    juris_filter = st.sidebar.multiselect(
        "Jurisdiction", juris_options, default=juris_options
    )

    doc_types = sorted(df["document_type"].dropna().unique().tolist())
    doc_filter = st.sidebar.multiselect(
        "Document type", doc_types, default=doc_types or []
    )

    active_filter = st.sidebar.selectbox(
        "Active flag",
        options=["all", "active only", "inactive only"],
        index=0,
    )

    q = df.copy()
    if juris_filter:
        q = q[
            q["jurisdiction"]
            .astype(str)
            .apply(lambda v: bool(set(_split_jurisdictions(v)) & set(juris_filter)))
        ]
    if doc_filter:
        q = q[q["document_type"].isin(doc_filter)]
    if active_filter == "active only":
        q = q[q["active"].astype(str).isin(["1", "True", "true"])]
    elif active_filter == "inactive only":
        q = q[~q["active"].astype(str).isin(["1", "True", "true"])]

    st.subheader("Existing sources")
    st.dataframe(
        q[
            [
                "source_id",
                "scheme_id",
                "jurisdiction",
                "document_type",
                "source_type",
                "active",
                "title",
                "url",
            ]
        ].reset_index(drop=True),
        height=300,
    )

    st.markdown("---")
    st.subheader("Add or edit a source")

    mode = st.radio("Mode", ["Add new", "Edit existing"], horizontal=True)
    st.caption("Source ID format: PREFIX-DOC-### (e.g., CAN-AB-LEG-001)")

    if mode == "Edit existing" and not q.empty:
        selected_source_id = st.selectbox(
            "Select source_id to edit", options=q["source_id"].tolist()
        )
        row = df[df["source_id"] == selected_source_id].iloc[0]
    else:
        selected_source_id = None
        row = pd.Series({col: "" for col in REQUIRED_SOURCE_COLUMNS})

    schemes_for_juris = pd.DataFrame()
    if not schemes.empty:
        schemes_for_juris = schemes.copy()

    scheme_options = []
    if not schemes.empty and "scheme_id" in schemes.columns:
        if "scheme_name" in schemes.columns:
            scheme_options = (
                schemes["scheme_id"].astype(str)
                + " – "
                + schemes["scheme_name"].astype(str)
            ).tolist()
        else:
            scheme_options = schemes["scheme_id"].astype(str).tolist()
    current_inst = str(row.get("scheme_id", "") or "").strip()
    default_idx = 0
    if current_inst:
        for i, s in enumerate(scheme_options):
            if s.startswith(current_inst + " –") or s == current_inst:
                default_idx = i
                break
    scheme_choice = st.selectbox(
        "Scheme ID",
        options=[""] + scheme_options,
        index=0 if not current_inst else default_idx + 1,
    )
    scheme_id = scheme_choice.split(" – ", 1)[0] if scheme_choice else ""

    jurisdiction_options = load_jurisdiction_options()
    current_jurisdictions = _split_jurisdictions(row.get("jurisdiction", ""))
    jurisdiction = st.multiselect(
        "Jurisdiction",
        options=jurisdiction_options,
        default=[j for j in current_jurisdictions if j in jurisdiction_options],
    )
    juris_for_form = ", ".join(jurisdiction)

    col1, col2, col3 = st.columns(3)
    with col1:
        doc_type_options = [
            "legislation",
            "official_publication",
            "news",
            "report",
        ]
        current_doc_type = str(row.get("document_type", "news") or "").strip()
        if current_doc_type and current_doc_type not in doc_type_options:
            doc_type_options = [current_doc_type] + doc_type_options
        document_type = st.selectbox(
            "Document type",
            options=doc_type_options,
            index=doc_type_options.index(current_doc_type)
            if current_doc_type in doc_type_options
            else 0,
        )
        existing_ids = {
            _normalize_source_id(v)
            for v in df["source_id"].dropna().astype(str).tolist()
        }
        prefix_map = _build_jurisdiction_prefix_map(df)
        auto_mode = st.checkbox(
            "Auto-generate Source ID", value=True, key="source_id_auto_mode"
        )
        source_id_value = row.get("source_id", "") if mode == "Edit existing" else ""
        if auto_mode and mode != "Edit existing":
            primary_jurisdiction = jurisdiction[0] if jurisdiction else ""
            auto_source_id = _suggest_source_id(
                primary_jurisdiction, document_type, existing_ids, prefix_map
            )
            source_id = st.text_input(
                "Source ID",
                value=auto_source_id,
                help="Auto-generated from jurisdiction and document type.",
                disabled=True,
            )
        else:
            source_id = st.text_input(
                "Source ID",
                value=source_id_value,
                help="Unique identifier, e.g. CAN-AB-LEG-005",
            )
    with col2:
        source_type = st.selectbox(
            "Source type",
            options=["html_page", "pdf_direct", "html_index_pdf_links"],
            index=["html_page", "pdf_direct", "html_index_pdf_links"].index(
                row.get("source_type", "html_page")
            )
            if row.get("source_type", "") in [
                "html_page",
                "pdf_direct",
                "html_index_pdf_links",
            ]
            else 0,
        )
        access_method_options = ["requests"]
        current_access = str(row.get("access_method", "requests") or "requests").strip()
        if current_access and current_access not in access_method_options:
            access_method_options = [current_access] + access_method_options
        access_method = st.selectbox(
            "Access method",
            options=access_method_options,
            index=access_method_options.index(current_access)
            if current_access in access_method_options
            else 0,
        )
    with col3:
        change_frequency = st.selectbox(
            "Change frequency",
            options=["ad_hoc", "annual", "monthly", "continuous"],
            index=["ad_hoc", "annual", "monthly", "continuous"].index(
                row.get("change_frequency", "ad_hoc")
            )
            if row.get("change_frequency", "") in [
                "ad_hoc",
                "annual",
                "monthly",
                "continuous",
            ]
            else 0,
        )
        active = st.checkbox(
            "Active (include in fetch-all)",
            value=str(row.get("active", "1")) in ["1", "True", "true"],
        )

    url = st.text_input("URL", value=row.get("url", ""))
    if st.button("Validate URL"):
        ok, msg = validate_url(url)
        if ok:
            st.success(f"URL looks good: {msg}")
        else:
            st.error(f"URL problem: {msg}")

    title = st.text_input("Title / description", value=row.get("title", ""))
    doc_pattern_options = ["", "(20\\d{2})"]
    current_pattern = str(row.get("doc_pattern", "") or "").strip()
    if current_pattern and current_pattern not in doc_pattern_options:
        doc_pattern_options = [current_pattern] + doc_pattern_options
    doc_pattern = st.selectbox(
        "doc_pattern (optional)",
        options=doc_pattern_options,
        index=doc_pattern_options.index(current_pattern)
        if current_pattern in doc_pattern_options
        else 0,
    )

    parsing_options = ["generic_html", "generic_pdf"]
    suggested_parsing = "generic_pdf" if source_type == "pdf_direct" else "generic_html"
    current_parsing = str(row.get("parsing_strategy", suggested_parsing) or suggested_parsing).strip()
    if current_parsing and current_parsing not in parsing_options:
        parsing_options = [current_parsing] + parsing_options
    parsing_strategy = st.selectbox(
        "Parsing strategy",
        options=parsing_options,
        index=parsing_options.index(current_parsing)
        if current_parsing in parsing_options
        else 0,
    )

    institution = st.text_input("Institution", value=row.get("institution", ""))
    year = st.text_input("Year", value=row.get("year", ""))
    auto_citation = st.checkbox(
        "Auto-generate citation key",
        value=not bool(str(row.get("citation_key", "")).strip()),
        key="citation_key_auto",
    )
    suggested_citation = _build_citation_key(document_type, institution, year)
    if auto_citation:
        citation_key = st.text_input(
            "Citation key",
            value=suggested_citation,
            disabled=True,
        )
    else:
        citation_key = st.text_input("Citation key", value=row.get("citation_key", ""))
    notes = st.text_area("Notes", value=row.get("notes", ""), height=80)

    if st.button("Save source", type="primary"):
        source_id = _normalize_source_id(source_id)
        ok, err = _valid_source_id(source_id)
        if not ok:
            st.error(err)
        elif not url:
            st.error("URL is required.")
        elif not jurisdiction:
            st.error("At least one jurisdiction is required.")
        else:
            if auto_mode and mode != "Edit existing":
                source_id = auto_source_id
            new_row = {
                "source_id": source_id,
                "jurisdiction": juris_for_form,
                "scheme_id": scheme_id,
                "document_type": document_type,
                "url": url,
                "source_type": source_type,
                "doc_pattern": doc_pattern,
                "access_method": access_method,
                "parsing_strategy": parsing_strategy,
                "change_frequency": change_frequency,
                "active": "1" if active else "0",
                "title": title,
                "institution": institution,
                "year": year,
                "citation_key": citation_key,
                "notes": notes,
            }

            df_cur = load_sources()
            if source_id in df_cur["source_id"].values:
                df_cur.loc[df_cur["source_id"] == source_id, :] = new_row
                st.success(f"Updated existing source {source_id}")
            else:
                df_cur = pd.concat(
                    [df_cur, pd.DataFrame([new_row])], ignore_index=True
                )
                st.success(f"Added new source {source_id}")

            save_sources(df_cur)
            _set_next_actions(
                "Source saved. Next steps:",
                ["run_discovery", "open_review"],
            )
            st.cache_data.clear()  # refresh cached views
            st.rerun()

    st.caption("Save the source before fetching so the fetcher can resolve the source_id.")
    normalized_source_id = _normalize_source_id(source_id)
    if st.button("Fetch this source now"):
        df_cur = load_sources()
        existing_ids = {
            _normalize_source_id(v)
            for v in df_cur["source_id"].dropna().astype(str).tolist()
        }
        if normalized_source_id not in existing_ids:
            st.error("Save the source before fetching.")
        else:
            with st.spinner("Fetching source..."):
                result = subprocess.run(
                    [
                        "python3",
                        "-m",
                        "_code._sources_extraction.cli",
                        "fetch-one",
                        "--source-id",
                        normalized_source_id,
                    ],
                    capture_output=True,
                    text=True,
                    check=False,
                )
            if result.returncode == 0:
                st.success(f"Fetched {normalized_source_id}")
                st.cache_data.clear()
                st.rerun()
            else:
                st.error("Fetch failed. See details below.")
                st.code((result.stdout or "") + "\n" + (result.stderr or ""))

    st.markdown("---")
    st.subheader("Discovery candidates")
    disc = load_discovery_candidates(_discovery_signature())
    if disc.empty:
        st.caption(
            "No discovery candidates found. Run `python3 -m _code._sources_extraction.discover` "
            "to populate _raw/sources/discovery_candidates.csv."
        )
    else:
        known_urls = set(
            u.strip().lower()
            for u in df.get("url", pd.Series(dtype=str)).dropna().astype(str).tolist()
            if u.strip()
        )
        dq = disc.copy()
        search_query = st.text_input(
            "Search discovery candidates", value="", help="Search across visible columns."
        ).strip()
        if "year_guess" in dq.columns:
            year_options = sorted(
                y for y in dq["year_guess"].dropna().astype(str).unique().tolist() if y
            )
            sel_years = st.multiselect("Discovery year", year_options)
            if sel_years:
                dq = dq[dq["year_guess"].astype(str).isin(sel_years)]
        if "method" in dq.columns:
            method_options = sorted(
                m for m in dq["method"].dropna().astype(str).unique().tolist() if m
            )
            sel_methods = st.multiselect("Discovery method", method_options)
            if sel_methods:
                dq = dq[dq["method"].astype(str).isin(sel_methods)]
        if "jurisdiction_code" in dq.columns:
            juris_opts = sorted(
                j
                for j in dq["jurisdiction_code"].dropna().astype(str).unique().tolist()
                if j
            )
            sel_juris = st.multiselect("Discovery jurisdiction", juris_opts)
            if sel_juris:
                dq = dq[dq["jurisdiction_code"].astype(str).isin(sel_juris)]

        if search_query:
            cols = [c for c in dq.columns if c not in {"score"}]
            mask = pd.Series(False, index=dq.index)
            needle = search_query.lower()
            for col in cols:
                series = dq[col].astype(str).str.lower()
                mask = mask | series.str.contains(needle, na=False)
            dq = dq[mask]

        display_disc_cols = [
            "promoted",
            "candidate_id",
            "url",
            "title",
            "year_guess",
            "jurisdiction_code",
            "scheme_id",
            "method",
            "score",
        ]
        dq["promoted"] = dq.get("url", pd.Series(dtype=str)).apply(
            lambda u: str(u).strip().lower() in known_urls if pd.notna(u) else False
        )
        display_disc_cols = [c for c in display_disc_cols if c in dq.columns]
        display_df = dq[display_disc_cols].reset_index(drop=True)
        column_config = {}
        if "promoted" in display_df.columns:
            column_config["promoted"] = st.column_config.CheckboxColumn(
                "promoted", width="small", help="Already in sources.csv"
            )
        if "title" in display_df.columns:
            column_config["title"] = st.column_config.TextColumn(
                "title", width="large"
            )
        selection = st.dataframe(
            display_df,
            height=260,
            use_container_width=True,
            column_config=column_config or None,
            on_select="rerun",
            selection_mode="single-row",
            key="discovery_candidates_table",
        )

        def _suggest_disc_source_id(
            jurisdiction_code: str,
            document_type: str,
            existing_ids: set[str],
        ) -> str:
            prefix = _normalize_source_prefix(jurisdiction_code) if jurisdiction_code else "SRC"
            token = _doc_type_token(document_type)
            base = f"{prefix}-{token}"
            max_n = 0
            for sid in existing_ids:
                if not sid.startswith(f"{base}-"):
                    continue
                tail = sid.split("-")[-1]
                if tail.isdigit():
                    max_n = max(max_n, int(tail))
            return f"{base}-{max_n + 1:03d}"

        def _default_doc_type(url: str) -> str:
            return "official_publication" if url.lower().endswith(".pdf") else "news"

        def _default_source_type(url: str) -> str:
            return "pdf_direct" if url.lower().endswith(".pdf") else "html_page"

        if "candidate_id" in dq.columns and not dq.empty:
            selected_rows = []
            try:
                selected_rows = selection.selection.rows
            except Exception:
                selected_rows = []
            if not selected_rows:
                st.info("Select a discovery candidate row above to promote.")
                return
            selected_disc_id = display_df.iloc[selected_rows[0]]["candidate_id"]
            cand = dq[dq["candidate_id"] == selected_disc_id].iloc[0]
            existing_ids = {
                _normalize_source_id(v)
                for v in df["source_id"].dropna().astype(str).tolist()
            }
            new_instrument = st.checkbox(
                "New scheme", value=False, key="promote_new_instrument"
            )
            with st.form("promote_discovery_candidate"):
                st.markdown("**Promote candidate to sources.csv**")
                source_id = st.text_input(
                    "New source_id",
                    value=_suggest_disc_source_id(
                        str(cand.get("jurisdiction_code", "")).strip(),
                        _default_doc_type(str(cand.get("url", ""))),
                        existing_ids,
                    ),
                )
                jurisdiction_options = ["All", ""] + load_jurisdiction_options()
                default_juris = str(cand.get("jurisdiction_code", "")).strip()
                try:
                    default_index = (
                        jurisdiction_options.index(default_juris)
                        if default_juris in jurisdiction_options
                        else 0
                    )
                except Exception:
                    default_index = 0
                juris_for_form = st.selectbox(
                    "Jurisdiction",
                    options=jurisdiction_options,
                    index=default_index,
                )
                instrument_options = [""] + load_instrument_options()
                default_instrument = str(cand.get("instrument_id", "")).strip()
                if new_instrument:
                    scheme_id = st.text_input(
                        "Scheme ID",
                        value=default_instrument,
                        key="promote_instrument_input",
                    )
                else:
                    try:
                        default_inst_index = (
                            instrument_options.index(default_instrument)
                            if default_instrument in instrument_options
                            else 0
                        )
                    except Exception:
                        default_inst_index = 0
                    scheme_id = st.selectbox(
                        "Scheme ID",
                        options=instrument_options,
                        index=default_inst_index,
                        key="promote_instrument_select",
                    )
                url = st.text_input("URL", value=str(cand.get("url", "")).strip())
                title = st.text_input(
                    "Title / description",
                    value=str(cand.get("title", "")).strip(),
                )
                year = st.text_input(
                    "Year", value=str(cand.get("year_guess", "")).strip()
                )
                document_type = st.selectbox(
                    "Document type",
                    options=[
                        "legislation",
                        "official_publication",
                        "news",
                        "report",
                    ],
                    index=[
                        "legislation",
                        "official_publication",
                        "news",
                        "report",
                    ].index(_default_doc_type(str(cand.get("url", "")))),
                )
                source_type = st.selectbox(
                    "Source type",
                    options=["html_page", "pdf_direct", "html_index_pdf_links"],
                    index=["html_page", "pdf_direct", "html_index_pdf_links"].index(
                        _default_source_type(str(cand.get("url", "")))
                    ),
                )
                active = st.checkbox("Active (include in fetch-all)", value=False)
                submitted = st.form_submit_button("Add to sources")
                if submitted:
                    source_id = _normalize_source_id(source_id)
                    ok, err = _valid_source_id(source_id)
                    if not ok:
                        st.error(err)
                    elif not url:
                        st.error("URL is required.")
                    elif not juris_for_form:
                        st.error("Jurisdiction is required.")
                    elif source_id in existing_ids:
                        st.error("source_id already exists in sources.csv.")
                    else:
                        new_row = {
                            "source_id": source_id,
                            "jurisdiction": juris_for_form,
                            "scheme_id": scheme_id,
                            "document_type": document_type,
                            "url": url,
                            "source_type": source_type,
                            "doc_pattern": "",
                            "access_method": "requests",
                            "parsing_strategy": "generic_html",
                            "change_frequency": "ad_hoc",
                            "active": "1" if active else "0",
                            "title": title,
                            "institution": "",
                            "year": year,
                            "citation_key": "",
                            "notes": (
                                f"discovery candidate {cand.get('candidate_id', '')} "
                                f"(method={cand.get('method', '')}, seed={cand.get('source_seed', '')})"
                            ),
                        }
                        df_cur = load_sources()
                        df_cur = pd.concat(
                            [df_cur, pd.DataFrame([new_row])], ignore_index=True
                        )
                        save_sources(df_cur)
                        st.success(f"Added new source {source_id}")
                        _set_next_actions(
                            "Source added from discovery candidate. Next steps:",
                            ["run_discovery", "open_review"],
                        )
                        st.cache_data.clear()
                        st.rerun()


# -------------------------------------------------------------------
# Scheme intake
# -------------------------------------------------------------------


def scheme_intake_view() -> None:
    st.title("WCPD – Scheme Intake")
    st.caption("Identify new schemes and run targeted web discovery queries.")
    _render_next_actions()

    st.subheader("Current dataset schemes")
    schemes = load_scheme_metadata()
    dataset_scheme_ids = load_dataset_scheme_ids()
    if schemes.empty:
        st.info("No scheme_description.csv found or empty.")
    else:
        schemes_view = schemes.copy()
        schemes_view["in_dataset"] = schemes_view["scheme_id"].apply(
            lambda s: str(s).strip() in dataset_scheme_ids
        )
        display_cols = [
            "scheme_id",
            "scheme_name",
            "scheme_type",
            "implementation_year",
            "in_dataset",
            "jurisdiction",
            "source_count",
        ]
        display_cols = [c for c in display_cols if c in schemes_view.columns]
        st.dataframe(
            schemes_view[display_cols].sort_values(
                by=["in_dataset", "implementation_year"], ascending=[True, False]
            ),
            height=280,
            use_container_width=True,
        )
        scheme_ids = sorted(
            s for s in schemes_view["scheme_id"].dropna().astype(str).tolist() if s.strip()
        )
        if scheme_ids:
            current = st.session_state.get("current_scheme_id", "")
            if current and current not in scheme_ids:
                scheme_ids.append(current)
            selected_scheme = st.selectbox(
                "Set current scheme context",
                options=scheme_ids,
                index=scheme_ids.index(current) if current in scheme_ids else 0,
            )
            st.session_state["current_scheme_id"] = selected_scheme

    st.markdown("---")
    st.subheader("Search for new schemes (SerpAPI)")
    api_key = os.environ.get(SERPAPI_KEY_ENV, "").strip()
    if not api_key:
        st.warning(
            f"SerpAPI key not found. Set `{SERPAPI_KEY_ENV}` in your environment."
        )

    current_year = dt.datetime.utcnow().year
    target_year = st.number_input(
        "Target year for query templates",
        min_value=1990,
        max_value=current_year + 2,
        value=current_year,
        step=1,
    )
    default_queries = [
        "new emissions trading system {year}",
        "emissions trading system launched {year}",
        "cap-and-trade program launched {year}",
        "cap-and-invest program launched {year}",
        "carbon tax introduced {year}",
        "carbon pricing scheme launched {year}",
        "national ETS launched {year}",
        "subnational ETS launched {year}",
    ]
    query_text = st.text_area(
        "Queries (one per line, {year} supported)",
        value="\n".join(default_queries),
        height=160,
    )
    results_per_query = st.slider("Results per query", 5, 20, 10, step=1)
    hl = st.text_input("Language (hl)", value="")
    gl = st.text_input("Country (gl)", value="")
    if st.button("Run scheme discovery search", type="primary", disabled=not api_key):
        queries = [
            q.strip().format(year=target_year)
            for q in query_text.splitlines()
            if q.strip()
        ]
        rows: list[dict[str, str]] = []
        with st.spinner("Running SerpAPI queries..."):
            for q in queries:
                try:
                    hits = _serpapi_search(
                        query=q,
                        api_key=api_key,
                        num_results=results_per_query,
                        hl=hl or None,
                        gl=gl or None,
                    )
                except Exception as exc:
                    st.error(f"Query failed: {q} ({exc})")
                    continue
                for hit in hits:
                    rows.append(
                        {
                            "query": q,
                            "title": hit.get("title", ""),
                            "url": hit.get("url", ""),
                            "snippet": hit.get("snippet", ""),
                        }
                    )
        st.session_state["scheme_intake_results"] = rows

    rows = st.session_state.get("scheme_intake_results", [])
    if rows:
        results_df = pd.DataFrame(rows)
        st.dataframe(results_df, use_container_width=True, height=320)
        if st.button("Save results to discovery_candidates.csv"):
            save_rows: list[dict[str, str]] = []
            for row in rows:
                save_rows.append(
                    {
                        "url": row.get("url", ""),
                        "title": row.get("title", ""),
                        "year_guess": str(target_year),
                        "jurisdiction_code": "",
                        "instrument_id": "",
                        "method": "serpapi",
                        "source_seed": f"scheme_intake:{row.get('query', '')}",
                        "score": "",
                    }
                )
            added = _append_discovery_candidates(save_rows)
            if added:
                st.success(f"Saved {added} new discovery candidates.")
            else:
                st.info("No new candidates to save (all URLs already present).")
    elif st.session_state.get("scheme_intake_results") is not None:
        st.info("No results returned.")

    st.markdown("---")
    st.subheader("Edit scheme_description.csv")
    st.caption("Update scheme characteristics for new or existing schemes.")
    scheme_df = load_scheme_description()
    if scheme_df.empty:
        scheme_df = pd.DataFrame(columns=SCHEME_COLUMNS)
    for col in SCHEME_COLUMNS:
        if col not in scheme_df.columns:
            scheme_df[col] = ""
    scheme_df = scheme_df[SCHEME_COLUMNS]
    edited_df = st.data_editor(
        scheme_df,
        use_container_width=True,
        height=320,
        num_rows="dynamic",
        key="scheme_description_editor",
    )
    if st.button("Save scheme_description.csv"):
        clean = edited_df.copy().fillna("")
        for col in SCHEME_COLUMNS:
            if col not in clean.columns:
                clean[col] = ""
        clean = clean[SCHEME_COLUMNS]
        clean["scheme_id"] = clean["scheme_id"].astype(str).str.strip()
        nonempty_mask = clean.apply(
            lambda row: any(str(v).strip() for v in row.tolist()), axis=1
        )
        clean = clean[nonempty_mask]
        if clean["scheme_id"].eq("").any():
            st.error("Scheme ID is required for all rows.")
        elif clean["scheme_id"].duplicated().any():
            st.error("Duplicate scheme_id values detected. Please make them unique.")
        else:
            SCHEME_PATH.parent.mkdir(parents=True, exist_ok=True)
            clean.to_csv(SCHEME_PATH, index=False)
            st.cache_data.clear()
            st.success(f"Saved {len(clean)} schemes to {SCHEME_PATH}.")

    st.markdown("---")
    st.subheader("Generate targeted discovery queries")
    st.caption(
        "Create a discovery_queries.csv with queries tied to known scheme names."
    )
    include_missing_only = st.checkbox(
        "Only schemes not yet in dataset", value=True
    )
    keyword_text = st.text_area(
        "Keywords (one per line)",
        value="emissions trading\ncarbon tax\ncap-and-trade",
        height=100,
    )
    if st.button("Write discovery_queries.csv"):
        if schemes.empty:
            st.warning("No schemes available to build queries.")
        else:
            keywords = [k.strip() for k in keyword_text.splitlines() if k.strip()]
            if not keywords:
                st.warning("Please provide at least one keyword.")
            else:
                schemes_view = schemes.copy()
                schemes_view["in_dataset"] = schemes_view["scheme_id"].apply(
                    lambda s: str(s).strip() in dataset_scheme_ids
                )
                if include_missing_only:
                    schemes_view = schemes_view[~schemes_view["in_dataset"]]
                queries: list[dict[str, str]] = []
                for _, row in schemes_view.iterrows():
                    scheme_id = str(row.get("scheme_id", "")).strip()
                    scheme_name = str(row.get("scheme_name", "")).strip()
                    year = str(row.get("implementation_year", "")).strip()
                    base = scheme_name or scheme_id
                    if not base:
                        continue
                    for kw in keywords:
                        queries.append(
                            {
                                "query": f"\"{base}\" {kw}",
                                "jurisdiction_code": "",
                                "instrument_id": scheme_id,
                                "source_seed": "scheme_intake",
                                "year": year,
                            }
                        )
                out_path = RAW_ROOT / "discovery_queries.csv"
                pd.DataFrame(queries).to_csv(out_path, index=False)
                st.success(f"Wrote {len(queries)} queries to {out_path}.")
                _set_next_actions(
                    "Discovery queries written. Next steps:",
                    ["run_discovery", "open_review"],
                )

# -------------------------------------------------------------------
# Raw editor views
# -------------------------------------------------------------------


def prices_editor_view(reviewer: str) -> None:
    st.subheader("Prices")

    scheme_options: set[str] = set()
    existing_price_schemes: set[str] = set()
    scheme_desc = load_scheme_description()
    if not scheme_desc.empty and "scheme_id" in scheme_desc.columns:
        scheme_options.update(
            s for s in scheme_desc["scheme_id"].dropna().astype(str).tolist() if s
        )
    if RAW_PRICE_DIR.exists():
        for path in RAW_PRICE_DIR.glob("*_prices.csv"):
            scheme_id = path.stem.replace("_prices", "")
            scheme_options.add(scheme_id)
            existing_price_schemes.add(scheme_id)

    if not scheme_options:
        st.warning("No scheme_id values found for price editing.")
        return

    ghg_options = ["CO2", "CH4", "N2O", "F-GASES"]
    products = load_price_products()

    scheme_labels: dict[str, str] = {}
    for sid in scheme_options:
        label = sid
        if sid not in existing_price_schemes:
            label = f"{label} (new)"
        scheme_labels[label] = sid

    current_scheme = st.session_state.get("current_scheme_id", "")
    scheme_label_options = sorted(scheme_labels.keys())
    preferred_label = None
    if current_scheme:
        for label, sid in scheme_labels.items():
            if sid == current_scheme:
                preferred_label = label
                break
    scheme_label = st.selectbox(
        "Scheme ID",
        scheme_label_options,
        index=scheme_label_options.index(preferred_label)
        if preferred_label in scheme_label_options
        else 0,
    )
    scheme_id = scheme_labels[scheme_label]
    st.session_state["current_scheme_id"] = scheme_id
    scheme_type_map = load_scheme_type_map()
    scheme_type = scheme_type_map.get(scheme_id, "")
    variable_hint = None
    if scheme_type == "tax":
        variable_hint = "Tax rate"
    elif scheme_type == "ets":
        variable_hint = "Allowance price"
    price_path = _price_file_path(scheme_id)
    temp_path = _temp_path(price_path)

    existing_df = pd.DataFrame(
        columns=[
            "scheme_id",
            "year",
            "ghg",
            "product",
            "rate",
            "currency_code",
            "source",
            "comment",
        ]
    )
    if price_path.exists():
        existing_df = pd.read_csv(price_path, dtype=str)

    if not existing_df.empty:
        st.caption(f"Existing prices in {price_path}")
        st.dataframe(existing_df.tail(20), height=200)
    if temp_path.exists():
        st.caption(f"Temp file detected: {temp_path}")

    last_year = None
    last_ghg: list[str] = []
    last_product: list[str] = []
    if not existing_df.empty and "year" in existing_df.columns:
        years = [
            int(float(y))
            for y in existing_df["year"].dropna().astype(str).tolist()
            if str(y).replace(".", "").isdigit()
        ]
        if years:
            last_year = max(years)
            last_mask = existing_df["year"].astype(str) == str(last_year)
            if last_mask.any():
                if "ghg" in existing_df.columns:
                    last_ghg = (
                        existing_df.loc[last_mask, "ghg"]
                        .dropna()
                        .astype(str)
                        .str.strip()
                        .tolist()
                    )
                    last_ghg = sorted({g for g in last_ghg if g})
                if "product" in existing_df.columns:
                    last_product = (
                        existing_df.loc[last_mask, "product"]
                        .dropna()
                        .astype(str)
                        .str.strip()
                        .tolist()
                    )
                    last_product = sorted({p for p in last_product if p})

    col1, col2, col3 = st.columns(3)
    with col1:
        year = int(
            st.number_input(
                "Year",
                min_value=1990,
                max_value=2100,
                value=last_year or 2024,
            )
        )
    with col2:
        ghg = st.multiselect(
            "GHG", ghg_options, default=last_ghg or ["CO2"]
        )
    with col3:
        product = st.multiselect(
            "Product / fuel",
            products,
            default=last_product or products[:1],
        )

    ghg_sel = [g for g in ghg if g]
    product_sel = [p for p in product if p]

    icap_sig = _icap_price_signature()
    icap_schemes = set()
    for gas_label in ghg_sel:
        icap_schemes |= load_raw_icap_price_presence(year, gas_label, icap_sig)
    if scheme_id in icap_schemes:
        st.markdown(
            "<span style='color:#999'>Prices for this scheme/year appear to be ICAP-derived.</span>",
            unsafe_allow_html=True,
        )

    with st.expander("Related discovery candidates", expanded=False):
        _render_related_discovery_candidates(
            scheme_id,
            year,
            key_prefix=f"price_disc_{scheme_id}_{year}",
            variable_hint=variable_hint,
        )

    default_currency = ""
    if not existing_df.empty and ghg_sel and product_sel:
        mask = (
            (existing_df["year"].astype(str) == str(year))
            & (existing_df["ghg"].astype(str).isin(ghg_sel))
            & (existing_df["product"].astype(str).isin(product_sel))
        )
        if mask.any() and "currency_code" in existing_df.columns:
            values = (
                existing_df.loc[mask, "currency_code"]
                .dropna()
                .astype(str)
                .str.strip()
                .tolist()
            )
            values = [v for v in values if v]
            if values:
                unique_vals = sorted(set(values))
                if len(unique_vals) == 1:
                    default_currency = unique_vals[0]

    col5, col6, col7 = st.columns(3)
    with col5:
        currency_code = st.text_input("Currency code", value=default_currency)
    with col6:
        rate = st.text_input("Rate", value="NA")
    with col7:
        sources_df = load_sources()
        source = _render_source_picker(
            "Source",
            scheme_id=scheme_id,
            sources_df=sources_df,
            existing_value="",
            key=f"price_source_{scheme_id}",
        )

    comment = st.text_area("Comment", value="", height=80)

    conflict = False
    conflict_details: list[str] = []
    check_df = existing_df
    if temp_path.exists():
        try:
            check_df = pd.read_csv(temp_path, dtype=str)
        except Exception:
            check_df = existing_df
    product_sel = [p for p in product if p]
    if not ghg_sel or not product_sel:
        st.warning("Select at least one GHG and one product.")
    if not check_df.empty and ghg_sel and product_sel:
        mask = (
            (check_df["year"].astype(str) == str(year))
            & (check_df["ghg"].astype(str).isin(ghg_sel))
            & (check_df["product"].astype(str).isin(product_sel))
        )
        if mask.any():
            existing_rows = check_df[mask]
            for _, existing_row in existing_rows.iterrows():
                for field, new_value in [
                    ("rate", rate),
                    ("currency_code", currency_code),
                    ("source", source),
                    ("comment", comment),
                ]:
                    old_value = existing_row.get(field, "")
                    if _is_nonempty(old_value) and str(old_value).strip() != str(new_value).strip():
                        conflict = True
                        conflict_details.append(
                            f"{existing_row.get('ghg','')} {existing_row.get('product','')}: "
                            f"{field} existing '{old_value}' vs new '{new_value}'"
                        )

    confirm = True
    if conflict:
        st.warning("Conflict with existing non-empty price entry:")
        for detail in conflict_details:
            st.write(f"- {detail}")
        confirm = st.checkbox("Confirm overwrite despite conflict", value=False)

    if st.button("Write price entry", type="primary"):
        if conflict and not confirm:
            st.error("Resolve conflict confirmation before writing.")
            return
        if not ghg_sel or not product_sel:
            st.error("Select at least one GHG and one product before writing.")
            return

        record_date = dt.datetime.utcnow().date().isoformat()
        df_out = check_df.copy()
        mask = None
        new_rows: list[dict[str, str]] = []
        for g in ghg_sel:
            for p in product_sel:
                new_rows.append(
                    {
                        "scheme_id": scheme_id,
                        "year": str(year),
                        "ghg": g,
                        "product": p,
                        "rate": rate,
                        "currency_code": currency_code,
                        "source": source,
                        "comment": comment,
                        "record_date": record_date,
                    }
                )
        if df_out.empty:
            df_out = pd.DataFrame(new_rows)
        else:
            mask = (
                (df_out["year"].astype(str) == str(year))
                & (df_out["ghg"].astype(str).isin(ghg_sel))
                & (df_out["product"].astype(str).isin(product_sel))
            )
            if mask.any():
                for row in new_rows:
                    row_mask = (
                        (df_out["year"].astype(str) == str(year))
                        & (df_out["ghg"].astype(str) == row["ghg"])
                        & (df_out["product"].astype(str) == row["product"])
                    )
                    if row_mask.any():
                        df_out.loc[row_mask, :] = row
                    else:
                        df_out = pd.concat([df_out, pd.DataFrame([row])], ignore_index=True)
            else:
                df_out = pd.concat([df_out, pd.DataFrame(new_rows)], ignore_index=True)

        if "record_date" not in df_out.columns:
            df_out["record_date"] = ""
        if mask is not None and mask.any():
            df_out.loc[mask, "record_date"] = record_date
        df_out = df_out[
            [
                "scheme_id",
                "year",
                "ghg",
                "product",
                "rate",
                "currency_code",
                "source",
                "comment",
                "record_date",
            ]
        ]
        df_out = df_out.sort_values(by=["year", "ghg", "product"])

        temp_path.parent.mkdir(parents=True, exist_ok=True)
        df_out.to_csv(temp_path, index=False)
        st.success(f"Wrote temp price file: {temp_path}")
        st.info("Use the promote section below to replace the canonical file.")

    _promote_temp_price_ui(price_path, temp_path, key_prefix=f"price_{scheme_id}")


def _coerce_year_key(year: int, mapping: dict[Any, Any]) -> Any:
    if year in mapping:
        return year
    if str(year) in mapping:
        return str(year)
    return year


def _source_options_for_scheme(scheme_id: str, sources_df: pd.DataFrame) -> list[str]:
    if sources_df.empty or "source_id" not in sources_df.columns:
        return []
    scheme_id = str(scheme_id).strip()
    if not scheme_id:
        return []
    multi_tokens = {"_multi_jurisdiction", "_multi_jurisdictions"}

    scheme_jurisdictions: set[str] = set()
    for _, row in sources_df.iterrows():
        row_schemes = _split_jurisdictions(row.get("scheme_id", ""))
        if scheme_id in row_schemes:
            scheme_jurisdictions.update(_split_jurisdictions(row.get("jurisdiction", "")))

    group_map = load_jurisdiction_groups()
    member_to_groups: dict[str, set[str]] = {}
    for group, members in group_map.items():
        for member in members:
            member_to_groups.setdefault(member, set()).add(group)

    expanded_scheme_jurisdictions = set(scheme_jurisdictions)
    for j in list(expanded_scheme_jurisdictions):
        expanded_scheme_jurisdictions.update(member_to_groups.get(j, set()))
        expanded_scheme_jurisdictions.update(group_map.get(j, set()))

    options: set[str] = set()
    for _, row in sources_df.iterrows():
        source_id = str(row.get("source_id", "")).strip()
        if not source_id:
            continue
        row_schemes = _split_jurisdictions(row.get("scheme_id", ""))
        row_jurisdictions = set(_split_jurisdictions(row.get("jurisdiction", "")))
        if multi_tokens & set(row_schemes + list(row_jurisdictions)):
            options.add(source_id)
            continue
        if scheme_id in row_schemes:
            options.add(source_id)
            continue
        if expanded_scheme_jurisdictions and row_jurisdictions & expanded_scheme_jurisdictions:
            options.add(source_id)
    return sorted(options)


def _render_source_picker(
    label: str,
    scheme_id: str,
    sources_df: pd.DataFrame,
    existing_value: str = "",
    key: str | None = None,
) -> str:
    def _title_for(source_id: str) -> str:
        if sources_df.empty or not source_id:
            return ""
        match = sources_df[sources_df["source_id"].astype(str) == str(source_id)]
        if match.empty:
            return ""
        raw = str(match.iloc[0].get("title", "") or "").strip()
        if not raw:
            return ""
        return raw[:80] + ("…" if len(raw) > 80 else "")

    def _details_for(source_id: str) -> tuple[str, str]:
        if sources_df.empty or not source_id:
            return "", ""
        match = sources_df[sources_df["source_id"].astype(str) == str(source_id)]
        if match.empty:
            return "", ""
        row = match.iloc[0].to_dict()
        parts = []
        for field in [
            "jurisdiction",
            "scheme_id",
            "document_type",
            "source_type",
            "year",
            "institution",
            "title",
            "url",
        ]:
            val = str(row.get(field, "") or "").strip()
            if val:
                parts.append(f"{field}: {val}")
        detail = " | ".join(parts)
        short = (
            f"{row.get('document_type','') or ''} "
            f"{row.get('institution','') or ''} "
            f"{row.get('year','') or ''}"
        ).strip()
        return short, detail

    options = _source_options_for_scheme(scheme_id, sources_df)
    existing_value = str(existing_value or "").strip()
    if existing_value and existing_value not in options:
        options = [existing_value] + options
        st.caption(
            "Existing source is not in sources.csv for this scheme. "
            "Consider adding it in Manage sources."
        )

    if not options:
        st.warning("No sources found for this scheme in sources.csv.")
        if st.button("Go to Manage sources", key=f"{key}_manage_sources"):
            st.session_state["pending_view"] = "Manage sources"
            st.rerun()
        return st.text_input(label, value=existing_value, key=key)

    options = [""] + options
    idx = options.index(existing_value) if existing_value in options else 0
    selection = st.selectbox(
        label,
        options=options,
        index=idx,
        key=key,
        format_func=lambda s: f"{s} — {_title_for(s)}" if s else s,
    )
    if not selection:
        if st.button("Go to Manage sources", key=f"{key}_manage_sources"):
            st.session_state["pending_view"] = "Manage sources"
            st.rerun()
    short, detail = _details_for(selection)
    if detail:
        st.markdown(
            f"<span title='{detail}'>Selected source details: {short or selection}</span>",
            unsafe_allow_html=True,
        )
    return selection


def scope_editor_view(reviewer: str) -> None:
    st.subheader("Scope")

    gas_label = st.session_state.get("scope_gas", list(GAS_OPTIONS.keys())[0])

    ets_data = load_scope_data(gas_label, "ets")
    tax_data = load_scope_data(gas_label, "tax")

    scheme_types: dict[str, set[str]] = {}
    for scheme_id in ets_data["data"].keys():
        scheme_types.setdefault(scheme_id, set()).add("ets")
    for scheme_id in tax_data["data"].keys():
        scheme_types.setdefault(scheme_id, set()).add("tax")

    scheme_desc = load_scheme_description()
    if not scheme_desc.empty and "scheme_id" in scheme_desc.columns:
        known_ids = set(scheme_types.keys())
        for scheme_id in scheme_desc["scheme_id"].dropna().astype(str).tolist():
            scheme_id = scheme_id.strip()
            if scheme_id and scheme_id not in known_ids:
                scheme_types.setdefault(scheme_id, set()).add("new")

    if not scheme_types:
        st.warning("No schemes found for scope editing.")
        return

    scheme_labels: dict[str, str] = {}
    for sid, types in scheme_types.items():
        label = f"{sid} (new)" if types == {"new"} else sid
        scheme_labels[label] = sid
    current_scheme = st.session_state.get("current_scheme_id", "")
    scheme_label_options = sorted(scheme_labels.keys())
    preferred_label = None
    if current_scheme:
        for label, sid in scheme_labels.items():
            if sid == current_scheme:
                preferred_label = label
                break
    scheme_label = st.selectbox(
        "Scheme ID",
        scheme_label_options,
        index=scheme_label_options.index(preferred_label)
        if preferred_label in scheme_label_options
        else 0,
    )
    scheme_id = scheme_labels[scheme_label]
    st.session_state["current_scheme_id"] = scheme_id
    types_for_scheme = scheme_types.get(scheme_id, set())
    scheme_type = ""
    if "new" in types_for_scheme or len(types_for_scheme) > 1:
        scheme_type = st.selectbox(
            "Scheme type",
            ["ets", "tax"],
            help="Choose the scope file this entry should write to.",
        )
        if "new" in types_for_scheme:
            st.info(
                "This will create the first scope entry for this scheme in the selected scope file."
            )
    else:
        scheme_type = next(iter(types_for_scheme)) if types_for_scheme else "tax"

    gas_label = st.selectbox("Gas", list(GAS_OPTIONS.keys()), key="scope_gas")

    if scheme_type == "ets":
        data_block = ets_data["data"]
        sources_block = ets_data["sources"]
        scope_path = ets_data["path"]
    else:
        data_block = tax_data["data"]
        sources_block = tax_data["sources"]
        scope_path = tax_data["path"]

    scheme_data = copy.deepcopy(data_block.get(scheme_id, {}))
    scheme_sources = copy.deepcopy(sources_block.get(scheme_id, {}))

    jur_dict = scheme_data.get("jurisdictions", {})
    sector_dict = scheme_data.get("sectors", {})
    fuel_dict = scheme_data.get("fuels", {})

    all_years = sorted(
        {
            int(y)
            for y in list(jur_dict.keys())
            + list(sector_dict.keys())
            + list(fuel_dict.keys())
            if str(y).isdigit()
        }
    )

    year_choice = st.selectbox("Year", options=all_years + ["New year"])
    if year_choice == "New year":
        year = int(st.number_input("New year", min_value=1990, max_value=2100, value=2025))
        prev_year = max([y for y in all_years if y < year], default=None)
    else:
        year = int(year_choice)
        prev_year = None

    year_key = _coerce_year_key(year, jur_dict)
    existing_jur = jur_dict.get(year_key, [])
    existing_sectors = sector_dict.get(_coerce_year_key(year, sector_dict), [])
    existing_fuels = fuel_dict.get(_coerce_year_key(year, fuel_dict), [])
    existing_source = scheme_sources.get(_coerce_year_key(year, scheme_sources), "")

    if prev_year is not None:
        prev_jur = jur_dict.get(_coerce_year_key(prev_year, jur_dict), [])
        prev_sectors = sector_dict.get(_coerce_year_key(prev_year, sector_dict), [])
        prev_fuels = fuel_dict.get(_coerce_year_key(prev_year, fuel_dict), [])
        if not existing_jur and prev_jur:
            existing_jur = prev_jur
        if not existing_sectors and prev_sectors:
            existing_sectors = prev_sectors
        if scheme_type == "tax" and not existing_fuels and prev_fuels:
            existing_fuels = prev_fuels

    jur_options = sorted({j for years in jur_dict.values() for j in years})
    ipcc_options = load_ipcc_codes(gas_label)
    ipcc_name_map = load_ipcc_name_map()
    fuel_options = load_price_products()

    jurisdictions = st.multiselect(
        "Jurisdictions", options=jur_options, default=existing_jur
    )
    ipcc_options = _merge_ipcc_options(ipcc_options, existing_sectors)
    ipcc_codes = st.multiselect(
        "IPCC codes",
        options=ipcc_options,
        default=existing_sectors,
        format_func=lambda c: _ipcc_display(c, ipcc_name_map),
    )
    fuels: list[str] = []
    if scheme_type == "tax":
        fuels = st.multiselect("Fuels", options=fuel_options, default=existing_fuels)

    sources_df = load_sources()
    source = _render_source_picker(
        "Source (for this year)",
        scheme_id=scheme_id,
        sources_df=sources_df,
        existing_value=str(existing_source or ""),
        key=f"scope_source_{scheme_id}_{scheme_type}_{year}",
    )

    with st.expander("Related discovery candidates", expanded=False):
        _render_related_discovery_candidates(
            scheme_id,
            year,
            key_prefix=f"scope_disc_{scheme_id}_{year}",
            variable_hint="Scope",
        )

    conflict = False
    conflict_details: list[str] = []

    if _is_nonempty(existing_jur) and set(existing_jur) != set(jurisdictions):
        conflict = True
        conflict_details.append("jurisdictions differ from existing values")
    if _is_nonempty(existing_sectors) and set(existing_sectors) != set(ipcc_codes):
        conflict = True
        conflict_details.append("IPCC codes differ from existing values")
    if scheme_type == "tax" and _is_nonempty(existing_fuels) and set(existing_fuels) != set(fuels):
        conflict = True
        conflict_details.append("fuels differ from existing values")
    if _is_nonempty(existing_source) and str(existing_source).strip() != str(source).strip():
        conflict = True
        conflict_details.append("source differs from existing value")

    confirm = True
    if conflict:
        st.warning("Conflict with existing non-empty scope data:")
        for detail in conflict_details:
            st.write(f"- {detail}")
        confirm = st.checkbox("Confirm overwrite despite conflict", value=False)

    if st.button("Write scope update", type="primary"):
        if conflict and not confirm:
            st.error("Resolve conflict confirmation before writing.")
            return

        new_data_block = copy.deepcopy(data_block)
        new_sources_block = copy.deepcopy(sources_block)

        scheme_entry = new_data_block.get(scheme_id, {})
        scheme_entry.setdefault("jurisdictions", {})
        scheme_entry.setdefault("sectors", {})
        if scheme_type == "tax":
            scheme_entry.setdefault("fuels", {})

        scheme_entry["jurisdictions"][year] = sorted(jurisdictions)
        scheme_entry["sectors"][year] = sorted(ipcc_codes)
        if scheme_type == "tax":
            scheme_entry["fuels"][year] = sorted(fuels)

        new_data_block[scheme_id] = scheme_entry

        scheme_sources_entry = new_sources_block.get(scheme_id, {})
        scheme_sources_entry[year] = source
        new_sources_block[scheme_id] = scheme_sources_entry

        out_path = _timestamped_path(scope_path)
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(
            _render_scope_module(new_data_block, new_sources_block), encoding="utf-8"
        )
        st.success(f"Wrote new scope file: {out_path}")
        st.info("Use the promote section below to replace the canonical file.")

    _promote_file_ui(scope_path, key_prefix=f"scope_{scheme_type}_{gas_label}")


def _flatten_rebates(exemptions: list[Any], sources: list[Any]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for idx, exemption in enumerate(exemptions):
        source_map = sources[idx] if idx < len(sources) else {}
        jur_map = exemption.get("jurisdiction", {})
        ipcc_map = exemption.get("ipcc", {})
        fuel_map = exemption.get("fuel", {})
        val_map = exemption.get("value", {})
        scheme_map = exemption.get("scheme_id", {})
        for year_key, jurisdictions in jur_map.items():
            year = int(year_key) if str(year_key).isdigit() else year_key
            rows.append(
                {
                    "year": year,
                    "jurisdictions": jurisdictions or [],
                    "ipcc": ipcc_map.get(year_key, []),
                    "fuels": fuel_map.get(year_key, []),
                    "value": val_map.get(year_key, ""),
                    "source": source_map.get(year_key, ""),
                    "scheme_id": scheme_map.get(year_key, ""),
                }
            )
    return rows


def rebates_editor_view(reviewer: str) -> None:
    st.subheader("Price rebates / exemptions")

    gas_label = st.selectbox("Gas (rebates)", list(GAS_OPTIONS.keys()), key="rebates_gas")
    rebates_data = load_rebates_data(gas_label)
    exemptions = list(rebates_data["exemptions"])
    sources = list(rebates_data["sources"])
    rebates_path = rebates_data["path"]

    flattened = _flatten_rebates(exemptions, sources)
    if flattened:
        st.caption("Existing exemptions (sample)")
        st.dataframe(pd.DataFrame(flattened).head(20), height=200)

    scheme_type_map = load_scheme_type_map()
    scheme_options = sorted(
        [sid for sid, stype in scheme_type_map.items() if stype == "tax"]
    )
    scheme_options = [""] + scheme_options if scheme_options else [""]
    current_scheme = st.session_state.get("current_scheme_id", "")
    index = scheme_options.index(current_scheme) if current_scheme in scheme_options else 0
    scheme_id = st.selectbox(
        "Scheme ID (rebate)",
        options=scheme_options,
        index=index,
        key="rebate_scheme_id",
    )
    if scheme_id:
        st.session_state["current_scheme_id"] = scheme_id

    year = int(
        st.number_input(
            "Year (rebate)", min_value=1990, max_value=2100, value=2024, key="rebate_year"
        )
    )

    scope_jur_options: set[str] = set()
    try:
        ets_scope = load_scope_data(gas_label, "ets")["data"]
        tax_scope = load_scope_data(gas_label, "tax")["data"]
        for data in [ets_scope, tax_scope]:
            for entry in data.values():
                for years in entry.get("jurisdictions", {}).values():
                    scope_jur_options.update(years)
    except Exception:
        pass
    jur_options = sorted(scope_jur_options)

    jurisdictions = st.multiselect("Jurisdictions (rebate)", jur_options)
    rebate_ipcc_options = load_ipcc_codes(gas_label)
    rebate_ipcc_options = _merge_ipcc_options(rebate_ipcc_options, [])
    ipcc_name_map = load_ipcc_name_map()
    ipcc_codes = st.multiselect(
        "IPCC codes (rebate)",
        rebate_ipcc_options,
        key="rebate_ipcc",
        format_func=lambda c: _ipcc_display(c, ipcc_name_map),
    )
    fuels = st.multiselect(
        "Fuels (rebate)", load_price_products(), key="rebate_fuels"
    )
    value = st.number_input("Rebate value (0-1)", min_value=0.0, max_value=1.0, value=0.0)
    sources_df = load_sources()
    source = _render_source_picker(
        "Source (rebate)",
        scheme_id=scheme_id,
        sources_df=sources_df,
        existing_value="",
        key=f"rebate_source_{scheme_id}_{year}",
    )

    with st.expander("Related discovery candidates", expanded=False):
        _render_related_discovery_candidates(
            scheme_id,
            year,
            key_prefix=f"rebate_disc_{scheme_id}_{year}",
            variable_hint="Price rebate",
        )

    conflict = False
    conflict_details: list[str] = []
    for row in flattened:
        if row["year"] != year:
            continue
        if scheme_id and row.get("scheme_id") and str(row.get("scheme_id")).strip() != scheme_id:
            continue
        if not (set(row["jurisdictions"]) & set(jurisdictions)):
            continue
        if not (set(row["ipcc"]) & set(ipcc_codes)):
            continue
        if not (set(row["fuels"]) & set(fuels)):
            continue
        if _is_nonempty(row["value"]) and str(row["value"]).strip() != str(value).strip():
            conflict = True
            conflict_details.append(
                f"Existing value {row['value']} for overlapping rebate entry"
            )
            break

    confirm = True
    if conflict:
        st.warning("Conflict with existing non-empty rebate entry.")
        for detail in conflict_details:
            st.write(f"- {detail}")
        confirm = st.checkbox("Confirm overwrite despite conflict", value=False, key="rebate_confirm")

    if st.button("Write rebate entry", type="primary"):
        if conflict and not confirm:
            st.error("Resolve conflict confirmation before writing.")
            return
        if not scheme_id:
            st.error("Select a Scheme ID before writing.")
            return

        new_exemption = {
            "scheme_id": {year: scheme_id},
            "jurisdiction": {year: jurisdictions},
            "ipcc": {year: ipcc_codes},
            "fuel": {year: fuels},
            "value": {year: value},
        }
        new_source = {year: source}

        exemptions.append(new_exemption)
        sources.append(new_source)

        out_path = _timestamped_path(rebates_path)
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(
            _render_rebates_module(exemptions, sources), encoding="utf-8"
        )
        st.success(f"Wrote new rebate file: {out_path}")

    _promote_file_ui(rebates_path, key_prefix=f"rebates_{gas_label}")


def coverage_factors_view() -> None:
    st.subheader("Coverage factors (review-only)")

    gas_label = st.selectbox("Gas (coverage factors)", list(GAS_OPTIONS.keys()), key="cf_gas")
    cf_dir = RAW_DB_ROOT / "coverageFactor" / GAS_OPTIONS[gas_label]
    if not cf_dir.exists():
        st.warning(f"Missing coverageFactor dir: {cf_dir}")
        return

    files = sorted(cf_dir.glob("*.csv"))
    if not files:
        st.warning(f"No coverage factor files in {cf_dir}")
        return

    file_choice = st.selectbox(
        "Coverage factor file", options=[str(p) for p in files], key="cf_file"
    )
    try:
        df = pd.read_csv(file_choice, dtype=str)
    except Exception as exc:
        st.error(f"Failed to read {file_choice}: {exc}")
        return

    st.dataframe(df.head(200), height=300)
    st.caption("Coverage factor edits are derived from scope/CF logic; no edits here.")


def overlaps_view() -> None:
    st.subheader("Overlaps (review-only)")

    gas_label = st.selectbox("Gas (overlaps)", list(GAS_OPTIONS.keys()), key="ov_gas")
    overlap_path = RAW_DB_ROOT / "overlap" / f"overlap_mechanisms_{gas_label}.csv"
    if not overlap_path.exists():
        st.warning(f"Missing overlap file: {overlap_path}")
        return

    try:
        df = pd.read_csv(overlap_path, dtype=str)
    except Exception as exc:
        st.error(f"Failed to read {overlap_path}: {exc}")
        return

    st.dataframe(df.head(200), height=300)
    st.caption("Overlap files are generated from scope/coverage factors; review only.")


def gap_dashboard_view() -> None:
    st.title("WCPD – Data Gaps Dashboard")
    st.caption("Raw inputs and final dataset.")
    _render_next_actions()
    _render_manage_sources_shortcut("gap_top")

    gas_label = st.selectbox("Gas", options=list(GAS_OPTIONS.keys()), index=0)
    current = dt.datetime.utcnow().year
    target_year = int(
        st.number_input("Target year", min_value=1990, max_value=current + 2, value=current)
    )

    expected = set(load_expected_schemes_for_gas(gas_label, target_year=target_year))

    icap_sig = _icap_price_signature()
    raw_price = load_raw_price_presence(target_year, gas_label, icap_sig)
    raw_icap_price = load_raw_icap_price_presence(target_year, gas_label, icap_sig)
    raw_scope = load_raw_scope_presence(target_year, gas_label)
    raw_cf = load_raw_coverage_presence(target_year, gas_label)
    raw_observed = set().union(raw_price, raw_scope, raw_cf)

    if not expected:
        expected = set(raw_observed)

    st.subheader("Raw data")
    st.caption("Checks _raw/price, _raw/scope, _raw/coverageFactor for the target year.")
    if raw_icap_price:
        st.caption(f"ICAP-derived ETS price schemes detected: {len(raw_icap_price)}")

    raw_rows: list[dict[str, Any]] = []
    for data_type, present in [
        ("price", raw_price),
        ("scope", raw_scope),
        ("coverageFactor", raw_cf),
    ]:
        missing = sorted(expected - present)
        for scheme_id in missing:
            raw_rows.append(
                {
                    "gas": gas_label,
                    "data_type": data_type,
                    "scheme_id": scheme_id,
                    "year": target_year,
                }
            )

    if raw_rows:
        sources_df = load_sources()
        scheme_juris_map = _scheme_jurisdiction_map(sources_df)
        group_map = load_jurisdiction_groups()
        group_labels = [f"Group: {g}" for g in sorted(group_map.keys())] if group_map else []
        juris_options = sorted(
            {j for v in scheme_juris_map.values() for j in v}
        )
        filter_options = group_labels + juris_options
        if filter_options:
            selected = st.multiselect(
                "Filter by jurisdiction / group (optional)",
                options=filter_options,
                default=[],
            )
            if selected:
                expanded = _expand_jurisdiction_selection(selected)
                raw_rows = [
                    row
                    for row in raw_rows
                    if scheme_juris_map.get(row["scheme_id"], set()) & expanded
                ]
                if not raw_rows:
                    st.warning("No gaps match the selected jurisdiction / group filter.")
                    return
        raw_df = pd.DataFrame(raw_rows)
        st.dataframe(raw_df, height=360)
        st.caption(
            f"Missing counts — price: {len(expected - raw_price)}, "
            f"scope: {len(expected - raw_scope)}, "
            f"coverageFactor: {len(expected - raw_cf)}"
        )
        st.subheader("Investigate a gap")
        row_labels = [
            f"{r['scheme_id']} | {r['data_type']} | {r['year']} | {r['gas']}"
            for r in raw_rows
        ]
        selected_label = st.selectbox(
            "Select missing row to investigate", options=row_labels
        )
        selected_row = raw_rows[row_labels.index(selected_label)]
        st.session_state["current_scheme_id"] = selected_row["scheme_id"]

        def _gap_variable(data_type: str) -> str:
            if data_type == "price":
                return "Allowance price"
            if data_type == "coverageFactor":
                return "Coverage factor"
            if data_type == "scope":
                return "Scope"
            return "Scope"

        if st.button("Open in Review candidates"):
            st.session_state["gap_filter_instrument_id"] = selected_row["scheme_id"]
            st.session_state["gap_filter_year"] = selected_row["year"]
            st.session_state["gap_filter_variable"] = _gap_variable(
                selected_row["data_type"]
            )
            st.session_state["gap_apply_filters"] = True
            st.session_state["pending_view"] = "Review candidates"
            st.rerun()

        st.markdown("---")
        st.subheader("Generate discovery queries from raw gaps")
        st.caption(
            "Writes _raw/sources/discovery_queries.csv with queries including scheme name and year."
        )
        extra_keywords = st.text_area(
            "Optional keywords (one per line)",
            value="",
            height=80,
            help="If provided, each keyword will be appended to the base query.",
        )
        if st.button("Write discovery_queries.csv from gaps"):
            scheme_desc = load_scheme_description()
            scheme_name_map = {}
            if not scheme_desc.empty:
                for _, row in scheme_desc.iterrows():
                    sid = str(row.get("scheme_id", "")).strip()
                    sname = str(row.get("scheme_name", "")).strip()
                    if sid:
                        scheme_name_map[sid] = sname
            keywords = [k.strip() for k in extra_keywords.splitlines() if k.strip()]
            queries: list[dict[str, str]] = []
            for row in raw_rows:
                scheme_id = str(row.get("scheme_id", "")).strip()
                scheme_name = scheme_name_map.get(scheme_id, "") or scheme_id
                year = str(row.get("year", "")).strip()
                data_type = str(row.get("data_type", "")).strip()
                if not scheme_name or not year:
                    continue
                base = f"\"{scheme_name}\" {year}"
                hint = data_type.replace("coverageFactor", "coverage factor").strip()
                if hint:
                    base = f"{base} {hint}"
                if keywords:
                    for kw in keywords:
                        queries.append(
                            {
                                "query": f"{base} {kw}",
                                "jurisdiction_code": "",
                                "instrument_id": scheme_id,
                                "source_seed": "gap_dashboard",
                                "year": year,
                            }
                        )
                else:
                    queries.append(
                        {
                            "query": base,
                            "jurisdiction_code": "",
                            "instrument_id": scheme_id,
                            "source_seed": "gap_dashboard",
                            "year": year,
                        }
                    )
            out_path = RAW_ROOT / "discovery_queries.csv"
            if queries:
                df_out = pd.DataFrame(queries).drop_duplicates()
                df_out.to_csv(out_path, index=False)
                st.success(f"Wrote {len(df_out)} queries to {out_path}.")
                _set_next_actions(
                    "Discovery queries written. Next steps:",
                    ["run_discovery", "open_review"],
                )
            else:
                st.info("No queries generated from current gaps.")
    else:
        st.success("No raw data gaps detected for the selected gas/year.")

    st.subheader("Final dataset")
    st.caption("Checks _dataset/data for tax/ETS IDs in the target year.")

    final_present = load_dataset_presence(target_year, gas_label)
    final_missing = sorted(expected - final_present)
    if final_missing:
        final_df = pd.DataFrame(
            [
                {
                    "gas": gas_label,
                    "data_type": "final_dataset",
                    "scheme_id": scheme_id,
                    "year": target_year,
                }
                for scheme_id in final_missing
            ]
        )
        st.dataframe(final_df, height=360)
        st.caption(f"Missing count — final dataset: {len(final_missing)}")
    else:
        st.success("No final dataset gaps detected for the selected gas/year.")


def raw_editor_view(reviewer: str) -> None:
    st.title("WCPD – Raw Editor")
    st.caption(
        "Writes temp or timestamped files for safety; original raw files remain unchanged."
    )
    _render_next_actions()
    _render_manage_sources_shortcut("raw_editor_top")
    _render_pending_changes_panel()
    tabs = st.tabs(["Prices", "Scope", "Price Rebates", "Coverage Factors", "Overlaps"])
    with tabs[0]:
        prices_editor_view(reviewer=reviewer)
    with tabs[1]:
        scope_editor_view(reviewer=reviewer)
    with tabs[2]:
        rebates_editor_view(reviewer=reviewer)
    with tabs[3]:
        coverage_factors_view()
    with tabs[4]:
        overlaps_view()


# -------------------------------------------------------------------
# Main
# -------------------------------------------------------------------


def main():
    st.set_page_config(page_title="WCPD – Upstream Workbench", layout="wide")
    apply_wcpd_branding()

    st.markdown(
        '<div class="wcpd-top-banner">WCPD – Upstream Workbench</div>',
        unsafe_allow_html=True,
    )

    with st.expander("How to use this app", expanded=False):
        st.graphviz_chart(
            """
digraph WCPD {
  rankdir=LR;
  node [shape=box, style=rounded, fontsize=11];
  A [label="Scheme intake"];
  B [label="Gap dashboard"];
  C [label="Manage sources"];
  D [label="Review candidates"];
  E [label="Raw editor"];
  F [label="Run discovery"];
  A -> B -> C -> D -> E;
  C -> F [style=dashed, label="discovery queries"];
  F -> C;
}
"""
        )
        st.markdown(
            """
**Recommended flow**
1. **Scheme intake**: review current schemes, set the current scheme context, and run targeted discovery queries.
2. **Gap dashboard**: identify missing data by scheme/year/variable and generate discovery queries.
3. **Manage sources**: add or edit sources; follow the suggested next steps to run discovery and review candidates.
4. **Review candidates**: use filtered candidates, open related source lookup, and jump to Raw editor.
5. **Raw editor**: apply edits to raw inputs and promote pending temp/timestamped files.

**Notes**
- **Current scheme context** is shared across views and defaults Raw editor selections.
- Use the **Related discovery candidates** expander in Raw editor tabs for fast evidence review.
- Jurisdiction **groups** can be used in filters where available.
- After adding sources or writing queries, use the **Next steps** panel to run discovery and review.
"""
        )

    # Choose view
    if WCPD_DASHBOARD_LOGO and WCPD_DASHBOARD_LOGO.exists():
        st.sidebar.image(str(WCPD_DASHBOARD_LOGO), width=220)
    st.sidebar.title("Upstream Workbench")
    pending_view = st.session_state.pop("pending_view", None)
    if pending_view:
        st.session_state["view"] = pending_view
    if "view" not in st.session_state:
        st.session_state["view"] = "Scheme intake"
    view = st.sidebar.radio(
        "View",
        options=[
            "Scheme intake",
            "Gap dashboard",
            "Manage sources",
            "Review candidates",
            "Raw editor",
        ],
        index=0,
        key="view",
    )

    reviewer = st.sidebar.text_input("Reviewer name/initials", value="GD")

    if view == "Review candidates":
        review_view(reviewer=reviewer)
    elif view == "Scheme intake":
        scheme_intake_view()
    elif view == "Manage sources":
        source_manager_view()
    elif view == "Gap dashboard":
        gap_dashboard_view()
    else:
        raw_editor_view(reviewer=reviewer)

    # Run quick actions + checklist in sidebar (last)
    render_discovery_button()
    render_run_status()


if __name__ == "__main__":
    main()
