from __future__ import annotations

from functools import lru_cache
from pathlib import Path

import pandas as pd

DATASET_PATH = Path(__file__).resolve().parents[3] / "DFC_FACILITY.csv"
VALID_SURVIVAL_CODES = {"001"}
MONTH_LABELS = {
    1: "January",
    2: "February",
    3: "March",
    4: "April",
    5: "May",
    6: "June",
    7: "July",
    8: "August",
    9: "September",
    10: "October",
    11: "November",
    12: "December",
}


def _safe_int(series: pd.Series) -> pd.Series:
    numeric = pd.to_numeric(series, errors="coerce")
    return numeric.astype("Int64")


def _extract_period_columns(df: pd.DataFrame) -> pd.DataFrame:
    df["certificationDate"] = pd.to_datetime(df["Certification Date"], errors="coerce")
    df["year"] = df["certificationDate"].dt.year.astype("Int64")
    df["month"] = df["certificationDate"].dt.month.astype("Int64")
    df["periodLabel"] = df["certificationDate"].dt.strftime("%Y-%m").fillna("Unknown")
    return df


@lru_cache(maxsize=1)
def get_dataset() -> pd.DataFrame:
    df = pd.read_csv(
        DATASET_PATH,
        dtype={
            "CMS Certification Number (CCN)": "string",
            "ZIP Code": "string",
            "Patient Survival data availability code": "string",
        },
    )

    df = df.rename(
        columns={
            "CMS Certification Number (CCN)": "ccn",
            "Facility Name": "facilityName",
            "State": "state",
            "ZIP Code": "zipCode",
            "City/Town": "city",
            "SMR Date": "SMR Date",
            "Mortality Rate (Facility)": "mortalityRateRaw",
            "Patient Survival Category Text": "mortalityCategory",
            "Patient Survival data availability code": "mortalityAvailabilityCode",
            "Number of Patients included in survival summary": "patientsInSummary",
        }
    )

    df = _extract_period_columns(df)
    df["ccn"] = df["ccn"].fillna("").str.strip()
    df["facilityName"] = df["facilityName"].fillna("").str.strip()
    df["state"] = df["state"].fillna("").str.strip()
    df["zipCode"] = df["zipCode"].fillna("").str.strip()
    df["city"] = df["city"].fillna("").str.strip()
    df["mortalityCategory"] = df["mortalityCategory"].fillna("Unknown").str.strip()
    df["mortalityAvailabilityCode"] = (
        df["mortalityAvailabilityCode"]
        .fillna("")
        .astype("string")
        .str.strip()
        .str.zfill(3)
    )
    df["patientsInSummary"] = _safe_int(df["patientsInSummary"])
    df["mortalityRate"] = pd.to_numeric(df["mortalityRateRaw"], errors="coerce")
    df["hasValidMortality"] = df["mortalityAvailabilityCode"].isin(VALID_SURVIVAL_CODES) & df[
        "mortalityRate"
    ].notna()
    df["monthLabel"] = df["month"].map(MONTH_LABELS)

    return df[
        [
            "ccn",
            "facilityName",
            "state",
            "zipCode",
            "city",
            "mortalityRate",
            "mortalityCategory",
            "mortalityAvailabilityCode",
            "patientsInSummary",
            "year",
            "month",
            "monthLabel",
            "periodLabel",
            "hasValidMortality",
        ]
    ].copy()


@lru_cache(maxsize=1)
def get_filter_options() -> dict[str, list]:
    df = get_dataset()

    years = sorted(int(year) for year in df["year"].dropna().unique().tolist())
    months = sorted(
        (
            {"value": int(month), "label": MONTH_LABELS.get(int(month), str(month))}
            for month in df["month"].dropna().unique().tolist()
        ),
        key=lambda item: item["value"],
    )
    states = sorted(state for state in df["state"].dropna().unique().tolist() if state)

    return {"years": years, "months": months, "states": states}
