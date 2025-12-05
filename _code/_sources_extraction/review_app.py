# _code/upstream/review_app.py

from __future__ import annotations

import datetime as dt
from pathlib import Path

import pandas as pd
import streamlit as st

RAW_ROOT = Path("_raw/sources")
CAND_PATH = RAW_ROOT / "cp_candidates.csv"
REVIEW_PATH = RAW_ROOT / "cp_review_state.csv"
META_PATH = RAW_ROOT / "meta" / "raw_artifacts.csv"
SOURCES_PATH = RAW_ROOT / "sources_with_instruments.csv"  # or sources.csv
SCHEME_PATH = Path("scheme_description.csv")  # adjust if needed


@st.cache_data
def load_candidates() -> pd.DataFrame:
    df = pd.read_csv(CAND_PATH, dtype=str)
    # ensure numeric_value is float-like where present
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
        return pd.read_csv(SOURCES_PATH, dtype=str)
    return pd.DataFrame()


@st.cache_data
def load_schemes() -> pd.DataFrame:
    if SCHEME_PATH.exists():
        return pd.read_csv(SCHEME_PATH, dtype=str)
    return pd.DataFrame()


def merge_all() -> pd.DataFrame:
    cand = load_candidates()
    meta = load_meta()
    sources = load_sources()
    schemes = load_schemes()
    review = load_review_state()

    # merge candidate → artifact meta
    if not meta.empty:
        cand = cand.merge(
            meta[["artifact_id", "local_path", "fetched_url"]],
            on="artifact_id",
            how="left",
        )
    # merge candidate → source meta
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
    # merge candidate → scheme_name
    if not schemes.empty and "scheme_id" in schemes.columns:
        cand = cand.merge(
            schemes[["scheme_id", "scheme_name"]],
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

    # update or append
    mask = df["candidate_id"] == row["candidate_id"]
    if mask.any():
        df.loc[mask, :] = row
    else:
        df = pd.concat([df, pd.DataFrame([row])], ignore_index=True)

    df.to_csv(REVIEW_PATH, index=False)


def main():
    st.set_page_config(page_title="WCPD – Upstream Review", layout="wide")
    st.title("World Carbon Pricing Database – Upstream Candidate Review")

    reviewer = st.sidebar.text_input("Reviewer name/initials", value="GD")

    df = merge_all()

    # Sidebar filters
    jurisdictions = sorted(df["jurisdiction_code"].dropna().unique().tolist())
    sel_juris = st.sidebar.multiselect("Jurisdiction", jurisdictions, default=jurisdictions)

    schemes = sorted(df["scheme_id"].dropna().unique().tolist())
    sel_schemes = st.sidebar.multiselect("Scheme (instrument_id)", schemes)

    fields = sorted(df["field_name"].dropna().unique().tolist())
    sel_fields = st.sidebar.multiselect("Field", fields, default=fields)

    status_options = ["unreviewed", "accepted", "rejected", "skipped"]
    sel_status = st.sidebar.multiselect("Status", status_options, default=["unreviewed"])

    # Confidence
    min_conf, max_conf = st.sidebar.slider("Confidence range", 0.0, 1.0, (0.0, 1.0), step=0.05)

    # Apply filters
    q = df.copy()
    if sel_juris:
        q = q[q["jurisdiction_code"].isin(sel_juris)]
    if sel_schemes:
        q = q[q["scheme_id"].isin(sel_schemes)]
    if sel_fields:
        q = q[q["field_name"].isin(sel_fields)]

    # Derive status from 'decision' column
    def status_of(row):
        if row.get("decision") in ("accepted", "rejected", "skipped"):
            return row["decision"]
        return "unreviewed"

    q["status"] = q.apply(status_of, axis=1)

    if sel_status:
        q = q[q["status"].isin(sel_status)]

    # Filter by confidence if column exists
    if "confidence" in q.columns:
        conf = pd.to_numeric(q["confidence"], errors="coerce")
        q = q[(conf >= min_conf - 1e-9) & (conf <= max_conf + 1e-9)]

    st.sidebar.markdown(f"**{len(q)} candidates** after filters")

    # Main layout: table + detail panel
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

        # selection
        st.markdown("### Select candidate")
        selected_id = st.selectbox(
            "Candidate ID",
            options=q["candidate_id"].tolist(),
        )

    # Detail / edit panel
    with right:
        st.subheader("Details & Review")

        row = q[q["candidate_id"] == selected_id].iloc[0]

        st.markdown(
            f"**Candidate:** `{row['candidate_id']}`  |  "
            f"**Scheme:** `{row.get('scheme_id', '')}` – {row.get('scheme_name', '')}  |  "
            f"**Jurisdiction:** {row.get('jurisdiction_code', '')}"
        )

        st.markdown(f"**Field:** `{row['field_name']}`")

        # Editable value fields
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            edited_value = st.text_input("Value", value=row.get("edited_value") or row["value"])
        with col2:
            current_numeric = row.get("edited_numeric_value") or row.get("numeric_value", "")
            edited_numeric_value = st.text_input("Numeric value", value=str(current_numeric or ""))
        with col3:
            edited_currency = st.text_input("Currency", value=row.get("edited_currency") or row.get("currency", "") or "")
        with col4:
            edited_unit = st.text_input("Unit", value=row.get("edited_unit") or row.get("unit", "") or "")

        st.markdown("**Snippet (context)**")
        st.code(row.get("snippet", ""), language="text")

        # Optionally show original URL/location
        if "fetched_url" in row and isinstance(row["fetched_url"], str):
            st.markdown(f"[Open original URL]({row['fetched_url']})")

        # Comment & decision
        comment = st.text_area("Comment", value=row.get("comment") or "", height=80)

        decision = st.radio(
            "Decision",
            options=["accepted", "rejected", "skipped"],
            index={"accepted": 0, "rejected": 1, "skipped": 2}.get(row.get("decision"), 0),
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


if __name__ == "__main__":
    main()
