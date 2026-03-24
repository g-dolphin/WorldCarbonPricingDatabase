from __future__ import annotations

import json
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import pandas as pd

KEY_COLUMNS = ["jurisdiction", "year", "ipcc_code", "Product"]
NUMERIC_COLUMNS = [
    "tax_rate_excl_ex_clcu",
    "tax_ex_rate",
    "tax_base_relief_rate",
    "tax_rate_incl_ex_clcu",
    "tax_rate_effective_clcu",
    "ets_price",
    "ets_2_price",
]
TEXT_COLUMNS = [
    "tax",
    "ets",
    "tax_id",
    "ets_id",
    "ets_2_id",
    "tax_curr_code",
    "ets_curr_code",
    "ets_2_curr_code",
]
LATEST_DIRNAME = "latest"
HISTORY_DIRNAME = "history"
SNAPSHOT_DIRNAME = "snapshots"


def _timestamp() -> str:
    return datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")


def _normalize_text(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, float) and pd.isna(value):
        return ""
    text = str(value).strip()
    if text.lower() in {"na", "nan", "none"}:
        return ""
    return text


def _to_numeric(series: pd.Series) -> pd.Series:
    return pd.to_numeric(series, errors="coerce")


def _dataset_dir(dataset_root: Path, gas: str) -> Path:
    return Path(dataset_root) / gas


def create_dataset_snapshot(
    dataset_root: Path, gas: str, qa_root: Path, keep: int = 3
) -> Path | None:
    src = _dataset_dir(dataset_root, gas)
    if not src.exists():
        return None
    snapshots_dir = Path(qa_root) / gas / SNAPSHOT_DIRNAME
    snapshots_dir.mkdir(parents=True, exist_ok=True)
    dest = snapshots_dir / _timestamp()
    shutil.copytree(src, dest)
    _prune_old_snapshots(snapshots_dir, keep=keep)
    return dest


def _prune_old_snapshots(snapshots_dir: Path, keep: int) -> None:
    snapshots = sorted([p for p in snapshots_dir.iterdir() if p.is_dir()])
    stale = snapshots[:-keep] if keep > 0 else snapshots
    for path in stale:
        shutil.rmtree(path, ignore_errors=True)


def load_dataset_rows(dataset_root: Path, gas: str) -> pd.DataFrame:
    gas_dir = _dataset_dir(dataset_root, gas)
    return load_dataset_rows_from_dir(gas_dir)


def load_dataset_rows_from_dir(gas_dir: Path) -> pd.DataFrame:
    gas_dir = Path(gas_dir)
    frames: list[pd.DataFrame] = []
    for level in ("national", "subnational"):
        level_dir = gas_dir / level
        if not level_dir.exists():
            continue
        for path in sorted(level_dir.glob("*.csv")):
            try:
                df = pd.read_csv(path, dtype=str)
            except Exception:
                continue
            if df.empty:
                continue
            df["level"] = level
            df["source_file"] = path.name
            frames.append(df)
    if not frames:
        return pd.DataFrame()
    df_all = pd.concat(frames, ignore_index=True)
    for col in KEY_COLUMNS + NUMERIC_COLUMNS + TEXT_COLUMNS + ["level", "source_file"]:
        if col not in df_all.columns:
            df_all[col] = ""
    return df_all


def find_odd_entries(df: pd.DataFrame, gas: str) -> pd.DataFrame:
    if df.empty:
        return pd.DataFrame()
    issues: list[dict[str, Any]] = []

    dupes = df[df.duplicated(KEY_COLUMNS, keep=False)].sort_values(KEY_COLUMNS)
    for _, row in dupes.iterrows():
        issues.append(
            _issue_record(
                gas,
                "duplicate_key",
                "high",
                row,
                detail="Duplicate dataset row for jurisdiction/year/ipcc_code/Product.",
            )
        )

    for flag_col, id_col, value_col, curr_col in [
        ("tax", "tax_id", "tax_rate_excl_ex_clcu", "tax_curr_code"),
        ("ets", "ets_id", "ets_price", "ets_curr_code"),
    ]:
        flag = _normalize_flag(df[flag_col])
        missing_value = flag & _to_numeric(df[value_col]).isna()
        missing_id = flag & (df[id_col].map(_normalize_text) == "")
        missing_curr = flag & (df[curr_col].map(_normalize_text) == "")
        stray_value = (~flag) & df[value_col].map(_normalize_text).ne("")
        stray_id = (~flag) & df[id_col].map(_normalize_text).ne("")

        issues.extend(
            _issues_from_mask(
                df,
                gas,
                missing_value,
                "missing_value_on_covered_row",
                "high",
                value_col,
                f"{flag_col}=1 but {value_col} is blank.",
            )
        )
        issues.extend(
            _issues_from_mask(
                df,
                gas,
                missing_id,
                "missing_id_on_covered_row",
                "high",
                id_col,
                f"{flag_col}=1 but {id_col} is blank.",
            )
        )
        issues.extend(
            _issues_from_mask(
                df,
                gas,
                missing_curr,
                "missing_currency_on_covered_row",
                "medium",
                curr_col,
                f"{flag_col}=1 but {curr_col} is blank.",
            )
        )
        issues.extend(
            _issues_from_mask(
                df,
                gas,
                stray_value,
                "value_present_when_not_covered",
                "medium",
                value_col,
                f"{flag_col}=0 but {value_col} is populated.",
            )
        )
        issues.extend(
            _issues_from_mask(
                df,
                gas,
                stray_id,
                "id_present_when_not_covered",
                "medium",
                id_col,
                f"{flag_col}=0 but {id_col} is populated.",
            )
        )

    for numeric_col in NUMERIC_COLUMNS:
        values = _to_numeric(df[numeric_col])
        negative_mask = values < 0
        issues.extend(
            _issues_from_mask(
                df,
                gas,
                negative_mask,
                "negative_numeric_value",
                "high",
                numeric_col,
                f"{numeric_col} is negative.",
            )
        )

    if "tax_ex_rate" in df.columns:
        ex_rate = _to_numeric(df["tax_ex_rate"])
        invalid_ex_rate = ex_rate.notna() & ((ex_rate < 0) | (ex_rate > 1))
        issues.extend(
            _issues_from_mask(
                df,
                gas,
                invalid_ex_rate,
                "invalid_tax_exemption_rate",
                "high",
                "tax_ex_rate",
                "tax_ex_rate is outside [0, 1].",
            )
        )

    if "tax_base_relief_rate" in df.columns:
        base_relief_rate = _to_numeric(df["tax_base_relief_rate"])
        invalid_base_relief_rate = base_relief_rate.notna() & (
            (base_relief_rate < 0) | (base_relief_rate > 1)
        )
        issues.extend(
            _issues_from_mask(
                df,
                gas,
                invalid_base_relief_rate,
                "invalid_tax_base_relief_rate",
                "high",
                "tax_base_relief_rate",
                "tax_base_relief_rate is outside [0, 1].",
            )
        )

    if {"tax_rate_excl_ex_clcu", "tax_rate_effective_clcu"}.issubset(df.columns):
        statutory = _to_numeric(df["tax_rate_excl_ex_clcu"])
        effective = _to_numeric(df["tax_rate_effective_clcu"])
        invalid_effective = effective.notna() & statutory.notna() & (effective > statutory)
        issues.extend(
            _issues_from_mask(
                df,
                gas,
                invalid_effective,
                "effective_tax_rate_exceeds_statutory_rate",
                "high",
                "tax_rate_effective_clcu",
                "tax_rate_effective_clcu exceeds tax_rate_excl_ex_clcu.",
            )
        )

    issues_df = pd.DataFrame(issues)
    if issues_df.empty:
        return issues_df
    return issues_df.sort_values(
        by=["severity", "category", "jurisdiction", "year", "ipcc_code", "Product"],
        kind="stable",
    ).reset_index(drop=True)


def _normalize_flag(series: pd.Series) -> pd.Series:
    return series.astype(str).str.strip().eq("1")


def _issues_from_mask(
    df: pd.DataFrame,
    gas: str,
    mask: pd.Series,
    category: str,
    severity: str,
    column_name: str,
    detail: str,
) -> list[dict[str, Any]]:
    out: list[dict[str, Any]] = []
    if not mask.any():
        return out
    for _, row in df.loc[mask].iterrows():
        out.append(
            _issue_record(
                gas,
                category,
                severity,
                row,
                column_name=column_name,
                detail=detail,
            )
        )
    return out


def _issue_record(
    gas: str,
    category: str,
    severity: str,
    row: pd.Series,
    column_name: str = "",
    detail: str = "",
) -> dict[str, Any]:
    return {
        "gas": gas,
        "category": category,
        "severity": severity,
        "jurisdiction": row.get("jurisdiction", ""),
        "year": row.get("year", ""),
        "ipcc_code": row.get("ipcc_code", ""),
        "Product": row.get("Product", ""),
        "column_name": column_name,
        "current_value": row.get(column_name, "") if column_name else "",
        "detail": detail,
        "source_file": row.get("source_file", ""),
    }


def compare_to_baseline(
    current_df: pd.DataFrame,
    baseline_df: pd.DataFrame,
    gas: str,
    price_change_threshold: float = 0.05,
) -> pd.DataFrame:
    if current_df.empty and baseline_df.empty:
        return pd.DataFrame()

    current = current_df.copy()
    baseline = baseline_df.copy()
    current["_row_state"] = "current"
    baseline["_row_state"] = "baseline"

    merged = baseline.merge(
        current,
        on=KEY_COLUMNS,
        how="outer",
        suffixes=("_old", "_new"),
        indicator=True,
    )

    changes: list[dict[str, Any]] = []

    for _, row in merged.iterrows():
        base_context = {
            "gas": gas,
            "jurisdiction": row.get("jurisdiction", ""),
            "year": row.get("year", ""),
            "ipcc_code": row.get("ipcc_code", ""),
            "Product": row.get("Product", ""),
        }
        if row["_merge"] == "left_only":
            changes.append(
                {
                    **base_context,
                    "change_type": "deleted_row",
                    "column_name": "",
                    "old_value": row.get("source_file_old", ""),
                    "new_value": "",
                    "abs_change": "",
                    "pct_change": "",
                    "detail": "Row existed in baseline but not in current build.",
                }
            )
            continue
        if row["_merge"] == "right_only":
            changes.append(
                {
                    **base_context,
                    "change_type": "new_row",
                    "column_name": "",
                    "old_value": "",
                    "new_value": row.get("source_file_new", ""),
                    "abs_change": "",
                    "pct_change": "",
                    "detail": "Row is new in current build.",
                }
            )
            continue

        for col in NUMERIC_COLUMNS:
            old_raw = _normalize_text(row.get(f"{col}_old", ""))
            new_raw = _normalize_text(row.get(f"{col}_new", ""))
            if old_raw == "" and new_raw == "":
                continue
            old_num = pd.to_numeric(pd.Series([old_raw]), errors="coerce").iloc[0]
            new_num = pd.to_numeric(pd.Series([new_raw]), errors="coerce").iloc[0]
            if pd.isna(old_num) or pd.isna(new_num):
                if old_raw != new_raw:
                    changes.append(
                        {
                            **base_context,
                            "change_type": "non_numeric_change",
                            "column_name": col,
                            "old_value": old_raw,
                            "new_value": new_raw,
                            "abs_change": "",
                            "pct_change": "",
                            "detail": f"{col} changed and could not be compared numerically.",
                        }
                    )
                continue
            abs_change = float(new_num - old_num)
            if old_num == 0:
                pct_change = None
                significant = new_num != 0
            else:
                pct_change = abs((new_num - old_num) / old_num)
                significant = pct_change > price_change_threshold
            if significant:
                changes.append(
                    {
                        **base_context,
                        "change_type": "significant_numeric_change",
                        "column_name": col,
                        "old_value": old_num,
                        "new_value": new_num,
                        "abs_change": abs_change,
                        "pct_change": pct_change,
                        "detail": f"{col} changed beyond the configured threshold.",
                    }
                )

        for col in TEXT_COLUMNS:
            old_text = _normalize_text(row.get(f"{col}_old", ""))
            new_text = _normalize_text(row.get(f"{col}_new", ""))
            if old_text == new_text:
                continue
            changes.append(
                {
                    **base_context,
                    "change_type": "categorical_change",
                    "column_name": col,
                    "old_value": old_text,
                    "new_value": new_text,
                    "abs_change": "",
                    "pct_change": "",
                    "detail": f"{col} changed relative to baseline.",
                }
            )

    changes_df = pd.DataFrame(changes)
    if changes_df.empty:
        return changes_df
    return changes_df.sort_values(
        by=["change_type", "column_name", "jurisdiction", "year", "ipcc_code", "Product"],
        kind="stable",
    ).reset_index(drop=True)


def run_postprocess_qa(
    dataset_root: Path,
    qa_root: Path,
    gas: str,
    baseline_dir: Path | None = None,
    price_change_threshold: float = 0.05,
) -> dict[str, Any]:
    current_df = load_dataset_rows(dataset_root, gas)
    odd_entries_df = find_odd_entries(current_df, gas)
    baseline_df = (
        load_dataset_rows_from_dir(Path(baseline_dir))
        if baseline_dir is not None and Path(baseline_dir).exists()
        else pd.DataFrame()
    )
    significant_changes_df = compare_to_baseline(
        current_df=current_df,
        baseline_df=baseline_df,
        gas=gas,
        price_change_threshold=price_change_threshold,
    )

    report = {
        "generated_at": _timestamp(),
        "gas": gas,
        "dataset_root": str(Path(dataset_root).resolve()),
        "baseline_dir": str(Path(baseline_dir).resolve()) if baseline_dir else "",
        "price_change_threshold": price_change_threshold,
        "row_count": int(len(current_df)),
        "odd_entry_count": int(len(odd_entries_df)),
        "significant_change_count": int(len(significant_changes_df)),
        "odd_entry_categories": _value_counts_dict(odd_entries_df, "category"),
        "significant_change_types": _value_counts_dict(significant_changes_df, "change_type"),
    }
    write_qa_report(qa_root, gas, report, odd_entries_df, significant_changes_df)
    return report


def _value_counts_dict(df: pd.DataFrame, column_name: str) -> dict[str, int]:
    if df.empty or column_name not in df.columns:
        return {}
    counts = df[column_name].value_counts(dropna=False)
    return {str(k): int(v) for k, v in counts.items()}


def write_qa_report(
    qa_root: Path,
    gas: str,
    summary: dict[str, Any],
    odd_entries_df: pd.DataFrame,
    significant_changes_df: pd.DataFrame,
) -> None:
    gas_root = Path(qa_root) / gas
    latest_dir = gas_root / LATEST_DIRNAME
    history_dir = gas_root / HISTORY_DIRNAME / summary["generated_at"]
    latest_dir.mkdir(parents=True, exist_ok=True)
    history_dir.mkdir(parents=True, exist_ok=True)

    _write_report_bundle(latest_dir, summary, odd_entries_df, significant_changes_df)
    _write_report_bundle(history_dir, summary, odd_entries_df, significant_changes_df)


def _write_report_bundle(
    out_dir: Path,
    summary: dict[str, Any],
    odd_entries_df: pd.DataFrame,
    significant_changes_df: pd.DataFrame,
) -> None:
    (out_dir / "summary.json").write_text(
        json.dumps(summary, indent=2, sort_keys=True), encoding="utf-8"
    )
    odd_entries_df.to_csv(out_dir / "odd_entries.csv", index=False)
    significant_changes_df.to_csv(out_dir / "significant_changes.csv", index=False)
