# _code/upstream/review_app.py

from __future__ import annotations

import copy
import datetime as dt
import difflib
import importlib.util
import os
import pprint
import base64
import uuid
from pathlib import Path
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
META_PATH = RAW_ROOT / "meta" / "raw_artifacts.csv"
SOURCES_PATH = RAW_ROOT / "sources.csv"  # or sources_master.csv later
SCHEME_PATH = Path("_raw/_aux_files/scheme_description.csv")
RAW_DB_ROOT = Path("_raw")
RAW_PRICE_DIR = RAW_DB_ROOT / "price"
RAW_SCOPE_DIR = RAW_DB_ROOT / "scope"
RAW_REBATES_DIR = RAW_DB_ROOT / "priceRebates" / "tax"
RAW_STRUCTURE_DIR = RAW_DB_ROOT / "_aux_files" / "wcpd_structure"
DATASET_ROOT = Path("_dataset/data")

GAS_OPTIONS = {
    "CO2": "CO2",
    "CH4": "CH4",
    "N2O": "N2O",
    "F-GASES": "Fgases",
}

REQUIRED_SOURCE_COLUMNS = [
    "source_id",
    "jurisdiction_code",
    "instrument_id",
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

WCPD_DASHBOARD_LOGO = Path(
    "/Users/geoffroydolphin/GitHub/wcpd_dashboard/frontend/public/wcpd_new_2_tm.png"
)

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
    if not META_PATH.exists():
        return pd.DataFrame()
    return pd.read_csv(META_PATH, dtype=str)


@st.cache_data
def load_sources() -> pd.DataFrame:
    if SOURCES_PATH.exists():
        df = pd.read_csv(SOURCES_PATH, dtype=str)
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


def _normalize_gas_token(value: str) -> str:
    token = str(value).strip().upper()
    if token in {"CO2", "CH4", "N2O"}:
        return token
    if "HFC" in token or "PFC" in token or "SF6" in token or "F-GAS" in token or "FGAS" in token:
        return "F-GASES"
    return ""


@st.cache_data
def load_expected_schemes_for_gas(gas_label: str) -> list[str]:
    schemes = load_scheme_description()
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
        ghg_raw = str(row.get("ghg", "")).strip()
        if not ghg_raw:
            continue
        tokens = [_normalize_gas_token(t) for t in ghg_raw.split(",")]
        if gas_key in tokens:
            out.append(scheme_id)
    return sorted(set(out))


@st.cache_data
def load_scheme_type_map() -> dict[str, str]:
    schemes = load_scheme_description()
    if schemes.empty:
        return {}
    out: dict[str, str] = {}
    for _, row in schemes.iterrows():
        scheme_id = str(row.get("scheme_id", "")).strip()
        scheme_type = str(row.get("scheme_type", "")).strip().lower()
        if scheme_id and scheme_type:
            out[scheme_id] = scheme_type
    return out


@st.cache_data
def load_raw_price_presence(target_year: int, gas_label: str) -> set[str]:
    present: set[str] = set()
    if not RAW_PRICE_DIR.exists():
        return present
    target = str(target_year)
    gas_key = str(gas_label).strip().upper()
    scheme_type_map = load_scheme_type_map()
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


def _promote_file_ui(canonical_path: Path, key_prefix: str) -> None:
    st.markdown("### Promote timestamped file")
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
    if st.button("Promote file", key=f"{key_prefix}_promote_button"):
        if not confirm:
            st.error("Please confirm promotion before proceeding.")
            return
        os.replace(selected, canonical_path)
        st.success(f"Promoted {selected} -> {canonical_path}")

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
    st.sidebar.caption(_file_status(META_PATH))

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


# -------------------------------------------------------------------
# Candidate review helpers
# -------------------------------------------------------------------


def merge_all_candidates() -> pd.DataFrame:
    cand = load_candidates(_candidates_signature())
    if cand.empty:
        return cand
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
                    "instrument_id",
                    "document_type",
                    "title",
                    "jurisdiction_code",
                    "year",
                ]
            ].drop_duplicates("source_id"),
            on="source_id",
            how="left",
            suffixes=("", "_src"),
        )
        for col in ["instrument_id", "year", "jurisdiction_code"]:
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
            left_on="instrument_id",
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

    df = merge_all_candidates()
    if df.empty:
        st.warning("No candidates found at _raw/sources/cp_candidates.csv")
        return

    # Sidebar filters
    schemes = (
        sorted(df["instrument_id"].dropna().unique().tolist())
        if "instrument_id" in df.columns
        else []
    )
    sel_schemes = st.sidebar.multiselect("Carbon pricing mechanism (instrument_id)", schemes)

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
    sel_variables = st.sidebar.multiselect(
        "Variable", variable_options, default=variable_options
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
    sel_years = st.sidebar.multiselect("Year", years)
    if sel_years and "year" in q.columns:
        q = q[q["year"].astype(str).isin(sel_years)]

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

    st.sidebar.markdown(f"**{len(q)} candidates** after filters")

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

    # Layout: top row (candidates + selector), then details + document
    top_left, top_right = st.columns([3, 2])
    with top_left:
        st.subheader("Candidates")
        show_all_cols = st.checkbox("Show all columns", value=False)
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
        st.dataframe(q[display_cols].reset_index(drop=True), height=320)

    review_entry_container = None
    review_entry_choice = "New entry"
    with top_right:
        st.subheader("Select candidate")
        selected_id = st.selectbox(
            "Candidate ID",
            options=q["candidate_id"].tolist(),
        )
        review_entry_container = st.container()

    candidate_rows = q[q["candidate_id"] == selected_id]
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
        juris_options = sorted(df["jurisdiction_code"].dropna().unique().tolist())

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

        st.markdown("**Applies to**")
        if edited_variable == "Scope":
            if not jurisdiction_default and row.get("jurisdiction_code"):
                jurisdiction_default = [str(row.get("jurisdiction_code"))]
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
                    "IPCC category", options=ipcc_options, default=ipcc_default
                )
        else:
            if not jurisdiction_default and row.get("jurisdiction_code"):
                jurisdiction_default = [str(row.get("jurisdiction_code"))]
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
                    "IPCC category", options=ipcc_options, default=ipcc_default
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
        render_candidate_document_panel(row)


def source_manager_view() -> None:
    st.title("WCPD – Source Manager")

    st.markdown(
        "Use this page to **add** or **edit** upstream sources used by the fetcher."
    )

    df = load_sources()
    schemes = load_schemes()

    # Sidebar filters
    st.sidebar.markdown("---")
    st.sidebar.header("Source filters")

    juris_options = sorted(df["jurisdiction_code"].dropna().unique().tolist())
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
        q = q[q["jurisdiction_code"].isin(juris_filter)]
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
                "jurisdiction_code",
                "instrument_id",
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
    st.subheader("Discovery candidates")
    disc = load_discovery_candidates(_discovery_signature())
    if disc.empty:
        st.caption(
            "No discovery candidates found. Run `python3 -m _code._sources_extraction.discover` "
            "to populate _raw/sources/discovery_candidates.csv."
        )
    else:
        dq = disc.copy()
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

        display_disc_cols = [
            "candidate_id",
            "url",
            "title",
            "year_guess",
            "jurisdiction_code",
            "instrument_id",
            "method",
            "score",
        ]
        display_disc_cols = [c for c in display_disc_cols if c in dq.columns]
        st.dataframe(dq[display_disc_cols].reset_index(drop=True), height=240)

        def _suggest_source_id(
            jurisdiction_code: str, year_guess: str, existing_ids: set[str]
        ) -> str:
            base = "DISC"
            if jurisdiction_code:
                base = f"{jurisdiction_code}-DISC"
            if year_guess:
                base = f"{base}-{year_guess}"
            candidate = f"{base}-001"
            counter = 1
            while candidate in existing_ids:
                counter += 1
                candidate = f"{base}-{counter:03d}"
            return candidate

        def _default_doc_type(url: str) -> str:
            return "official_publication" if url.lower().endswith(".pdf") else "webpage"

        def _default_source_type(url: str) -> str:
            return "pdf_direct" if url.lower().endswith(".pdf") else "html_page"

        if "candidate_id" in dq.columns and not dq.empty:
            selected_disc_id = st.selectbox(
                "Select discovery candidate",
                options=dq["candidate_id"].tolist(),
            )
            cand = dq[dq["candidate_id"] == selected_disc_id].iloc[0]
            existing_ids = set(df["source_id"].dropna().astype(str).tolist())
            with st.form("promote_discovery_candidate"):
                st.markdown("**Promote candidate to sources.csv**")
                source_id = st.text_input(
                    "New source_id",
                    value=_suggest_source_id(
                        str(cand.get("jurisdiction_code", "")).strip(),
                        str(cand.get("year_guess", "")).strip(),
                        existing_ids,
                    ),
                )
                juris_for_form = st.text_input(
                    "Jurisdiction code", value=str(cand.get("jurisdiction_code", "")).strip()
                )
                instrument_id = st.text_input(
                    "Instrument ID (scheme_id)",
                    value=str(cand.get("instrument_id", "")).strip(),
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
                    options=["legislation", "official_publication", "webpage", "report"],
                    index=["legislation", "official_publication", "webpage", "report"].index(
                        _default_doc_type(str(cand.get("url", "")))
                    ),
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
                    if not source_id:
                        st.error("source_id is required.")
                    elif not url:
                        st.error("URL is required.")
                    elif not juris_for_form:
                        st.error("Jurisdiction code is required.")
                    elif source_id in existing_ids:
                        st.error("source_id already exists in sources.csv.")
                    else:
                        new_row = {
                            "source_id": source_id,
                            "jurisdiction_code": juris_for_form,
                            "instrument_id": instrument_id,
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
                        st.cache_data.clear()
                        st.rerun()

    st.markdown("---")
    st.subheader("Add or edit a source")

    mode = st.radio("Mode", ["Add new", "Edit existing"], horizontal=True)

    if mode == "Edit existing" and not q.empty:
        selected_source_id = st.selectbox(
            "Select source_id to edit", options=q["source_id"].tolist()
        )
        row = df[df["source_id"] == selected_source_id].iloc[0]
    else:
        selected_source_id = None
        row = pd.Series({col: "" for col in REQUIRED_SOURCE_COLUMNS})

    juris_for_form = st.text_input(
        "Jurisdiction code", value=row.get("jurisdiction_code", "")
    )

    schemes_for_juris = pd.DataFrame()
    if not schemes.empty and juris_for_form:
        schemes_for_juris = schemes[
            schemes["scheme_name"].str.contains(
                juris_for_form, case=False, na=False
            )
        ]

    col1, col2, col3 = st.columns(3)
    with col1:
        source_id = st.text_input(
            "Source ID",
            value=row.get("source_id", ""),
            help="Unique identifier, e.g. CAN-AB-leg-005",
        )
        document_type = st.selectbox(
            "Document type",
            options=["legislation", "official_publication", "webpage", "report"],
            index=["legislation", "official_publication", "webpage", "report"].index(
                row.get("document_type", "webpage")
            )
            if row.get("document_type", "") in [
                "legislation",
                "official_publication",
                "webpage",
                "report",
            ]
            else 2,
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
        access_method = st.text_input(
            "Access method", value=row.get("access_method", "requests")
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
    doc_pattern = st.text_input(
        "doc_pattern (optional)", value=row.get("doc_pattern", "")
    )
    parsing_strategy = st.text_input(
        "Parsing strategy", value=row.get("parsing_strategy", "generic_html")
    )

    st.markdown("### Instrument / scheme mapping")

    if not schemes_for_juris.empty:
        scheme_options = (
            schemes_for_juris["scheme_id"] + " – " + schemes_for_juris["scheme_name"]
        ).tolist()
        current_inst = row.get("instrument_id", "")
        default_idx = 0
        if current_inst:
            for i, s in enumerate(scheme_options):
                if s.startswith(current_inst + " –"):
                    default_idx = i
                    break

        scheme_choice = st.selectbox(
            "Scheme for this source (filtered by jurisdiction substring)",
            options=[""] + scheme_options,
            index=0 if not current_inst else default_idx + 1,
        )
        if scheme_choice:
            instrument_id = scheme_choice.split(" – ", 1)[0]
        else:
            instrument_id = row.get("instrument_id", "")
    else:
        instrument_id = st.text_input(
            "Instrument ID (scheme_id)", value=row.get("instrument_id", "")
        )

    institution = st.text_input("Institution", value=row.get("institution", ""))
    year = st.text_input("Year", value=row.get("year", ""))
    citation_key = st.text_input("Citation key", value=row.get("citation_key", ""))
    notes = st.text_area("Notes", value=row.get("notes", ""), height=80)

    if st.button("Save source", type="primary"):
        if not source_id:
            st.error("source_id is required.")
        elif not url:
            st.error("URL is required.")
        elif not juris_for_form:
            st.error("Jurisdiction code is required.")
        else:
            new_row = {
                "source_id": source_id,
                "jurisdiction_code": juris_for_form,
                "instrument_id": instrument_id,
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
            st.cache_data.clear()  # refresh cached views
            st.rerun()


# -------------------------------------------------------------------
# Raw editor views
# -------------------------------------------------------------------


def prices_editor_view(reviewer: str) -> None:
    st.subheader("Prices")

    scheme_options: set[str] = set()
    scheme_desc = load_scheme_description()
    if not scheme_desc.empty and "scheme_id" in scheme_desc.columns:
        scheme_options.update(
            s for s in scheme_desc["scheme_id"].dropna().astype(str).tolist() if s
        )
    if RAW_PRICE_DIR.exists():
        for path in RAW_PRICE_DIR.glob("*_prices.csv"):
            scheme_options.add(path.stem.replace("_prices", ""))

    if not scheme_options:
        st.warning("No scheme_id values found for price editing.")
        return

    scheme_id = st.selectbox("Scheme ID", sorted(scheme_options))
    price_path = _price_file_path(scheme_id)

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

    ghg_options = ["CO2", "CH4", "N2O", "F-GASES"]
    products = load_price_products()

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        year = int(st.number_input("Year", min_value=1990, max_value=2100, value=2024))
    with col2:
        ghg = st.selectbox("GHG", ghg_options)
    with col3:
        product = st.selectbox("Product / fuel", products)
    with col4:
        currency_code = st.text_input("Currency code", value="")

    col5, col6 = st.columns(2)
    with col5:
        rate = st.text_input("Rate", value="NA")
    with col6:
        source = st.text_input("Source", value="")

    comment = st.text_area("Comment", value="", height=80)

    conflict = False
    conflict_details: list[str] = []
    if not existing_df.empty:
        mask = (
            (existing_df["year"].astype(str) == str(year))
            & (existing_df["ghg"].astype(str) == ghg)
            & (existing_df["product"].astype(str) == product)
        )
        if mask.any():
            existing_row = existing_df[mask].iloc[0]
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
                        f"{field}: existing '{old_value}' vs new '{new_value}'"
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

        new_row = {
            "scheme_id": scheme_id,
            "year": str(year),
            "ghg": ghg,
            "product": product,
            "rate": rate,
            "currency_code": currency_code,
            "source": source,
            "comment": comment,
        }

        df_out = existing_df.copy()
        if df_out.empty:
            df_out = pd.DataFrame([new_row])
        else:
            mask = (
                (df_out["year"].astype(str) == str(year))
                & (df_out["ghg"].astype(str) == ghg)
                & (df_out["product"].astype(str) == product)
            )
            if mask.any():
                df_out.loc[mask, :] = new_row
            else:
                df_out = pd.concat([df_out, pd.DataFrame([new_row])], ignore_index=True)

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
            ]
        ]
        df_out = df_out.sort_values(by=["year", "ghg", "product"])

        out_path = _timestamped_path(price_path)
        out_path.parent.mkdir(parents=True, exist_ok=True)
        df_out.to_csv(out_path, index=False)
        st.success(f"Wrote new price file: {out_path}")
        st.info("Use the promote section below to replace the canonical file.")

    _promote_file_ui(price_path, key_prefix=f"price_{scheme_id}")


def _coerce_year_key(year: int, mapping: dict[Any, Any]) -> Any:
    if year in mapping:
        return year
    if str(year) in mapping:
        return str(year)
    return year


def scope_editor_view(reviewer: str) -> None:
    st.subheader("Scope")

    gas_label = st.selectbox("Gas", list(GAS_OPTIONS.keys()))

    ets_data = load_scope_data(gas_label, "ets")
    tax_data = load_scope_data(gas_label, "tax")

    scheme_choices: list[tuple[str, str]] = []
    for scheme_id in ets_data["data"].keys():
        scheme_choices.append((scheme_id, "ets"))
    for scheme_id in tax_data["data"].keys():
        scheme_choices.append((scheme_id, "tax"))

    if not scheme_choices:
        st.warning("No schemes found for scope editing.")
        return

    scheme_label = st.selectbox(
        "Scheme",
        sorted({f"{sid} ({stype})" for sid, stype in scheme_choices}),
    )
    scheme_id = scheme_label.split(" (", 1)[0]
    scheme_type = scheme_label.split(" (", 1)[1].rstrip(")")

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
    else:
        year = int(year_choice)

    year_key = _coerce_year_key(year, jur_dict)
    existing_jur = jur_dict.get(year_key, [])
    existing_sectors = sector_dict.get(_coerce_year_key(year, sector_dict), [])
    existing_fuels = fuel_dict.get(_coerce_year_key(year, fuel_dict), [])
    existing_source = scheme_sources.get(_coerce_year_key(year, scheme_sources), "")

    jur_options = sorted({j for years in jur_dict.values() for j in years})
    ipcc_options = load_ipcc_codes(gas_label)
    fuel_options = load_price_products()

    jurisdictions = st.multiselect(
        "Jurisdictions", options=jur_options, default=existing_jur
    )
    ipcc_codes = st.multiselect(
        "IPCC codes", options=ipcc_options, default=existing_sectors
    )
    fuels: list[str] = []
    if scheme_type == "tax":
        fuels = st.multiselect("Fuels", options=fuel_options, default=existing_fuels)

    source = st.text_input("Source (for this year)", value=str(existing_source or ""))

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

    year = int(st.number_input("Year (rebate)", min_value=1990, max_value=2100, value=2024, key="rebate_year"))

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
    ipcc_codes = st.multiselect(
        "IPCC codes (rebate)", load_ipcc_codes(gas_label), key="rebate_ipcc"
    )
    fuels = st.multiselect(
        "Fuels (rebate)", load_price_products(), key="rebate_fuels"
    )
    value = st.number_input("Rebate value (0-1)", min_value=0.0, max_value=1.0, value=0.0)
    source = st.text_input("Source (rebate)", value="")

    conflict = False
    conflict_details: list[str] = []
    for row in flattened:
        if row["year"] != year:
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

        new_exemption = {
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

    gas_label = st.selectbox("Gas", options=list(GAS_OPTIONS.keys()), index=0)
    current = dt.datetime.utcnow().year
    target_year = int(
        st.number_input("Target year", min_value=1990, max_value=current + 2, value=current)
    )

    expected = set(load_expected_schemes_for_gas(gas_label))

    raw_price = load_raw_price_presence(target_year, gas_label)
    raw_scope = load_raw_scope_presence(target_year, gas_label)
    raw_cf = load_raw_coverage_presence(target_year, gas_label)
    raw_observed = set().union(raw_price, raw_scope, raw_cf)

    if not expected:
        expected = set(raw_observed)

    st.subheader("Raw data")
    st.caption("Checks _raw/price, _raw/scope, _raw/coverageFactor for the target year.")

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
        raw_df = pd.DataFrame(raw_rows)
        st.dataframe(raw_df, height=360)
        st.caption(
            f"Missing counts — price: {len(expected - raw_price)}, "
            f"scope: {len(expected - raw_scope)}, "
            f"coverageFactor: {len(expected - raw_cf)}"
        )
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
        "Writes timestamped files for safety; original raw files remain unchanged."
    )
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

    # Choose view
    if WCPD_DASHBOARD_LOGO.exists():
        st.sidebar.image(str(WCPD_DASHBOARD_LOGO), width=220)
    st.sidebar.title("Upstream Workbench")
    view = st.sidebar.radio(
        "View",
        options=["Review candidates", "Manage sources", "Raw editor", "Gap dashboard"],
        index=0,
    )

    reviewer = st.sidebar.text_input("Reviewer name/initials", value="GD")

    if view == "Review candidates":
        review_view(reviewer=reviewer)
    elif view == "Manage sources":
        source_manager_view()
    elif view == "Gap dashboard":
        gap_dashboard_view()
    else:
        raw_editor_view(reviewer=reviewer)

    # Run checklist in sidebar (last)
    render_run_status()


if __name__ == "__main__":
    main()
