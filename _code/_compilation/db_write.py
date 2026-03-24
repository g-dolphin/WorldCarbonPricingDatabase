from __future__ import annotations

import os
from datetime import datetime
from pathlib import Path

try:
    from _code._compilation import db_qa as dataset_qa
    from _code._compilation import db_build as build
except ImportError:
    import db_qa as dataset_qa  # type: ignore
    import db_build as build  # type: ignore


def standardize_name(name: str) -> str:
    return name.replace(".", "").replace(",", "").replace(" ", "_")


def save_jurisdiction_files(
    df, jurisdictions, std_names, gas: str, level: str, base_dir: Path
) -> None:
    for jur, std_name in zip(jurisdictions, std_names):
        subset = df[df.jurisdiction == jur]
        filename = f"wcpd_{gas.lower()}_{std_name}.csv"
        out_path = Path(base_dir) / gas / level / filename
        out_path.parent.mkdir(parents=True, exist_ok=True)
        subset.to_csv(out_path, index=False)


ROOT_DIR = Path(build.ROOT_DIR)
RAW_DIR = Path(build.RAW_DIR)
DATASET_VERSION = os.environ.get(
    "WCPD_DATASET_VERSION",
    f"v{datetime.now().year}.1",
)
DATASET_DATA_DIR = ROOT_DIR / "_dataset" / "data" / DATASET_VERSION
DATASET_SOURCES_DIR = ROOT_DIR / "_dataset" / "sources" / DATASET_VERSION
DATASET_QA_DIR = ROOT_DIR / "_dataset" / "qa"
GAS = build.GAS
BUILD_RESULT = build.build(GAS)

# Standardized names
std_country_names = [standardize_name(x) for x in BUILD_RESULT["ctries"]]
std_subnat_names = [standardize_name(x) for x in BUILD_RESULT["subnats"]]

# Snapshot current gas outputs before overwriting them so QA can compare builds.
baseline_dir = dataset_qa.create_dataset_snapshot(DATASET_DATA_DIR, GAS, DATASET_QA_DIR)

# Save national and subnational data files
save_jurisdiction_files(
    BUILD_RESULT["wcpd_all_jur"],
    BUILD_RESULT["ctries"],
    std_country_names,
    GAS,
    "national",
    DATASET_DATA_DIR,
)
save_jurisdiction_files(
    BUILD_RESULT["wcpd_all_jur"],
    BUILD_RESULT["subnats"],
    std_subnat_names,
    GAS,
    "subnational",
    DATASET_DATA_DIR,
)
save_jurisdiction_files(
    BUILD_RESULT["wcpd_all_jur_sources"],
    BUILD_RESULT["ctries"],
    std_country_names,
    GAS,
    "national",
    DATASET_SOURCES_DIR,
)
save_jurisdiction_files(
    BUILD_RESULT["wcpd_all_jur_sources"],
    BUILD_RESULT["subnats"],
    std_subnat_names,
    GAS,
    "subnational",
    DATASET_SOURCES_DIR,
)

# Coverage factors
coverage_dir = RAW_DIR / "coverageFactor" / GAS
coverage_dir.mkdir(parents=True, exist_ok=True)
for scheme in (
    BUILD_RESULT["taxes_1_list"]
    + BUILD_RESULT["tax_2_list"]
    + BUILD_RESULT["ets_1_list"]
    + BUILD_RESULT["ets_2_list"]
):
    BUILD_RESULT["cf"][BUILD_RESULT["cf"].scheme_id == scheme].to_csv(
        coverage_dir / f"{scheme}_cf.csv", index=False
    )

# Scheme overlap
overlap_dir = RAW_DIR / "overlap"
overlap_dir.mkdir(parents=True, exist_ok=True)
overlap_path = overlap_dir / f"overlap_{GAS}.csv"
if "overlap" in BUILD_RESULT:
    BUILD_RESULT["overlap"].to_csv(overlap_path, index=False)
else:
    print("Overlap export skipped: build result does not include overlap output.")

# Dataset QA
qa_summary = dataset_qa.run_postprocess_qa(
    dataset_root=DATASET_DATA_DIR,
    qa_root=DATASET_QA_DIR,
    gas=GAS,
    baseline_dir=baseline_dir,
    price_change_threshold=0.05,
)
print(
    "Dataset QA complete:",
    f"version={DATASET_VERSION}",
    f"odd_entries={qa_summary['odd_entry_count']}",
    f"significant_changes={qa_summary['significant_change_count']}",
)
