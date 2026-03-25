from __future__ import annotations

import pandas as pd


def apply_filters(
    df: pd.DataFrame,
    *,
    year: int | None = None,
    month: int | None = None,
    state: str | None = None,
    zip_code: str | None = None,
    facility_name: str | None = None,
) -> pd.DataFrame:
    filtered = df.copy()

    if year is not None:
        filtered = filtered[filtered["year"] == year]

    if month is not None:
        filtered = filtered[filtered["month"] == month]

    if state:
        filtered = filtered[filtered["state"].str.upper() == state.strip().upper()]

    if zip_code:
        zip_code = zip_code.strip()
        filtered = filtered[filtered["zipCode"].fillna("").str.startswith(zip_code)]

    if facility_name:
        filtered = filtered[
            filtered["facilityName"].str.contains(facility_name.strip(), case=False, na=False)
        ]

    return filtered
