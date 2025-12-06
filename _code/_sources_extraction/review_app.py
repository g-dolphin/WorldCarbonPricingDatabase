# _code/upstream/review_app.py

from __future__ import annotations

import datetime as dt
from pathlib import Path

import httpx
import pandas as pd
import streamlit as st

# -------------------------------------------------------------------
# Paths / constants
# -------------------------------------------------------------------

RAW_ROOT = Path("_raw/sources")
CAND_PATH = RAW_ROOT / "cp_candidates.csv"
REVIEW_PATH = RAW_ROOT / "cp_review_state.csv"
META_PATH = RAW_ROOT / "meta" / "raw_artifacts.csv"
SOURCES_PATH = RAW_ROOT / "sources.csv"  # or sources_master.csv later
SCHEME_PATH = Path("scheme_description.csv")  # adjust if needed

REQUIRED_SOURCE_COLUMNS = [
    "source_id",
    "jurisdiction_code",
    "instrument_id",
    "document_type",
    "url",
    "source_type",
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
]

# -------------------------------------------------------------------
# Shared loaders (cached)
# -------------------------------------------------------------------


@st.cache_data
def load_candidates() -> pd.DataFrame:
    if not CAND_PATH.exists():
        return pd.DataFrame()
    df = pd.read_csv(CAND_PATH, dtype=str)
    if "numeric_value" in df.columns:
        df["numeric_value"] = pd.to_numeric(df["numeric_value"], errors="coerce")
    return df


@st.cache_data
def load_review_state() -> pd.DataFrame:
    if not REVIEW_PATH.exists():
        return pd.DataFrame(
            columns=[
                "candidate_id",
                "decision",
                "edited_value",
                "edited_numeric_value",
                "edited_currency",
                "edited_unit",
                "reviewer",
                "reviewed_at",
                "comment",
            ]
        )
    return pd.read_csv(REVIEW_PATH, dtype=str)


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
        cand = load_candidates()
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


# -------------------------------------------------------------------
# Candidate review helpers
# -------------------------------------------------------------------


def merge_all_candidates() -> pd.DataFrame:
    cand = load_candidates()
    if cand.empty:
        return cand

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
                ]
            ].drop_duplicates("source_id"),
            on="source_id",
            how="left",
            suffixes=("", "_src"),
        )

    # candidate → scheme_name
    if not schemes.empty and "scheme_id" in schemes.columns:
        cand = cand.merge(
            schemes[["scheme_id", "scheme_name"]],
            on="scheme_id",
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
    else:
        # add empty columns for UI convenience
        cand["decision"] = ""
        cand["edited_value"] = ""
        cand["edited_numeric_value"] = ""
        cand["edited_currency"] = ""
        cand["edited_unit"] = ""
        cand["comment"] = ""

    return cand


def save_review_row(row: dict) -> None:
    """Append/update a row in cp_review_state.csv."""
    if REVIEW_PATH.exists():
        df = pd.read_csv(REVIEW_PATH, dtype=str)
    else:
        df = pd.DataFrame(
            columns=[
                "candidate_id",
                "decision",
                "edited_value",
                "edited_numeric_value",
                "edited_currency",
                "edited_unit",
                "reviewer",
                "reviewed_at",
                "comment",
            ]
        )

    mask = df["candidate_id"] == row["candidate_id"]
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
    jurisdictions = sorted(df["jurisdiction_code"].dropna().unique().tolist())
    sel_juris = st.sidebar.multiselect(
        "Jurisdiction", jurisdictions, default=jurisdictions
    )

    schemes = sorted(df["scheme_id"].dropna().unique().tolist()) if "scheme_id" in df.columns else []
    sel_schemes = st.sidebar.multiselect("Scheme (instrument_id)", schemes)

    fields = sorted(df["field_name"].dropna().unique().tolist())
    sel_fields = st.sidebar.multiselect("Field", fields, default=fields)

    status_options = ["unreviewed", "accepted", "rejected", "skipped"]
    sel_status = st.sidebar.multiselect(
        "Status", status_options, default=["unreviewed"]
    )

    # Confidence
    min_conf, max_conf = st.sidebar.slider(
        "Confidence range", 0.0, 1.0, (0.0, 1.0), step=0.05
    )

    # Apply filters
    q = df.copy()
    if sel_juris:
        q = q[q["jurisdiction_code"].isin(sel_juris)]
    if sel_schemes:
        q = q[q["scheme_id"].isin(sel_schemes)]
    if sel_fields:
        q = q[q["field_name"].isin(sel_fields)]

    def status_of(row):
        if row.get("decision") in ("accepted", "rejected", "skipped"):
            return row["decision"]
        return "unreviewed"

    q["status"] = q.apply(status_of, axis=1)

    if sel_status:
        q = q[q["status"].isin(sel_status)]

    if "confidence" in q.columns:
        conf = pd.to_numeric(q["confidence"], errors="coerce")
        q = q[(conf >= min_conf - 1e-9) & (conf <= max_conf + 1e-9)]

    st.sidebar.markdown(f"**{len(q)} candidates** after filters")

    # Layout: table + detail
    left, right = st.columns([2, 3])

    with left:
        st.subheader("Candidates")
        display_cols = [
            "candidate_id",
            "status",
            "scheme_id",
            "scheme_name",
            "jurisdiction_code",
            "field_name",
            "value",
            "numeric_value",
            "currency",
            "unit",
            "confidence",
            "source_id",
        ]
        display_cols = [c for c in display_cols if c in q.columns]
        st.dataframe(q[display_cols].reset_index(drop=True), height=400)

        st.markdown("### Select candidate")
        selected_id = st.selectbox(
            "Candidate ID",
            options=q["candidate_id"].tolist(),
        )

    with right:
        st.subheader("Details & Review")
        row = q[q["candidate_id"] == selected_id].iloc[0]

        st.markdown(
            f"**Candidate:** `{row['candidate_id']}`  |  "
            f"**Scheme:** `{row.get('scheme_id', '')}` – {row.get('scheme_name', '')}  |  "
            f"**Jurisdiction:** {row.get('jurisdiction_code', '')}"
        )
        st.markdown(f"**Field:** `{row['field_name']}`")

        col1, col2, col3, col4 = st.columns(4)
        with col1:
            edited_value = st.text_input(
                "Value", value=row.get("edited_value") or row["value"]
            )
        with col2:
            current_numeric = row.get("edited_numeric_value") or row.get(
                "numeric_value", ""
            )
            edited_numeric_value = st.text_input(
                "Numeric value", value=str(current_numeric or "")
            )
        with col3:
            edited_currency = st.text_input(
                "Currency",
                value=row.get("edited_currency") or row.get("currency", "") or "",
            )
        with col4:
            edited_unit = st.text_input(
                "Unit", value=row.get("edited_unit") or row.get("unit", "") or ""
            )

        st.markdown("**Snippet (context)**")
        st.code(row.get("snippet", ""), language="text")

        if "fetched_url" in row and isinstance(row["fetched_url"], str):
            st.markdown(f"[Open original URL]({row['fetched_url']})")

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
                "candidate_id": row["candidate_id"],
                "decision": decision,
                "edited_value": edited_value,
                "edited_numeric_value": edited_numeric_value,
                "edited_currency": edited_currency,
                "edited_unit": edited_unit,
                "reviewer": reviewer,
                "reviewed_at": now,
                "comment": comment,
            }
            save_review_row(review_row)
            st.success("Saved.")
            st.rerun()


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
# Main
# -------------------------------------------------------------------


def main():
    st.set_page_config(page_title="WCPD – Upstream Workbench", layout="wide")

    # Run checklist in sidebar
    render_run_status()

    # Choose view
    st.sidebar.title("Upstream Workbench")
    view = st.sidebar.radio(
        "View",
        options=["Review candidates", "Manage sources"],
        index=0,
    )

    reviewer = st.sidebar.text_input("Reviewer name/initials", value="GD")

    if view == "Review candidates":
        review_view(reviewer=reviewer)
    else:
        source_manager_view()


if __name__ == "__main__":
    main()
