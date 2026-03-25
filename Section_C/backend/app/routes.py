from __future__ import annotations

from typing import Any

import pandas as pd
from fastapi import APIRouter, Query

from .data_loader import get_dataset, get_filter_options
from .filters import apply_filters
from .schemas import AnalysisResponse, FilterOptionsResponse, SummaryResponse, TableResponse

router = APIRouter(prefix="/api")


def _clean_number(value: Any) -> float | None:
    if value is None or pd.isna(value):
        return None
    return round(float(value), 2)


def _int_or_none(value: Any) -> int | None:
    if value is None or pd.isna(value):
        return None
    return int(value)


def _serialize_records(df: pd.DataFrame) -> list[dict[str, Any]]:
    records: list[dict[str, Any]] = []
    for row in df.to_dict(orient="records"):
        records.append(
            {
                "ccn": row["ccn"],
                "facilityName": row["facilityName"],
                "state": row["state"],
                "zipCode": row["zipCode"],
                "city": row["city"],
                "mortalityRate": _clean_number(row["mortalityRate"]),
                "mortalityCategory": row["mortalityCategory"],
                "mortalityAvailabilityCode": row["mortalityAvailabilityCode"],
                "patientsInSummary": _int_or_none(row["patientsInSummary"]),
                "year": _int_or_none(row["year"]),
                "month": _int_or_none(row["month"]),
                "periodLabel": row["periodLabel"],
            }
        )
    return records


def _serialize_ranking(df: pd.DataFrame) -> list[dict[str, Any]]:
    return [
        {
            "ccn": row["ccn"],
            "facilityName": row["facilityName"],
            "state": row["state"],
            "zipCode": row["zipCode"],
            "mortalityRate": round(float(row["mortalityRate"]), 2),
            "mortalityCategory": row["mortalityCategory"],
            "patientsInSummary": _int_or_none(row["patientsInSummary"]),
        }
        for row in df.to_dict(orient="records")
    ]


def _empty_summary(total: int) -> dict[str, Any]:
    return {
        "total": total,
        "avgMortality": None,
        "minMortality": None,
        "maxMortality": None,
        "top10Highest": [],
        "top10Lowest": [],
    }


@router.get("/filters", response_model=FilterOptionsResponse)
def get_filters() -> FilterOptionsResponse:
    return FilterOptionsResponse(**get_filter_options())


@router.get("/summary", response_model=SummaryResponse)
def get_summary(
    year: int | None = Query(default=None),
    month: int | None = Query(default=None),
    state: str | None = Query(default=None),
    zipCode: str | None = Query(default=None),
    facilityName: str | None = Query(default=None),
) -> SummaryResponse:
    filtered = apply_filters(
        get_dataset(),
        year=year,
        month=month,
        state=state,
        zip_code=zipCode,
        facility_name=facilityName,
    )

    valid = filtered[filtered["hasValidMortality"]].copy()
    total = int(len(filtered))

    if valid.empty:
        return SummaryResponse(**_empty_summary(total))

    highest = valid.sort_values(["mortalityRate", "facilityName"], ascending=[False, True]).head(10)
    lowest = valid.sort_values(["mortalityRate", "facilityName"], ascending=[True, True]).head(10)

    return SummaryResponse(
        total=total,
        avgMortality=_clean_number(valid["mortalityRate"].mean()),
        minMortality=_clean_number(valid["mortalityRate"].min()),
        maxMortality=_clean_number(valid["mortalityRate"].max()),
        top10Highest=_serialize_ranking(highest),
        top10Lowest=_serialize_ranking(lowest),
    )


@router.get("/table", response_model=TableResponse)
def get_table(
    year: int | None = Query(default=None),
    month: int | None = Query(default=None),
    state: str | None = Query(default=None),
    zipCode: str | None = Query(default=None),
    facilityName: str | None = Query(default=None),
    page: int = Query(default=1, ge=1),
    pageSize: int = Query(default=25, ge=1, le=200),
) -> TableResponse:
    filtered = apply_filters(
        get_dataset(),
        year=year,
        month=month,
        state=state,
        zip_code=zipCode,
        facility_name=facilityName,
    ).sort_values(["facilityName", "ccn"], ascending=[True, True])

    total = int(len(filtered))
    start = (page - 1) * pageSize
    end = start + pageSize
    page_df = filtered.iloc[start:end]

    return TableResponse(data=_serialize_records(page_df), page=page, pageSize=pageSize, total=total)


def _group_average(df: pd.DataFrame, field: str, top_n: int | None = None) -> list[dict[str, Any]]:
    valid = df[df["hasValidMortality"]]
    if valid.empty:
        return []

    grouped = (
        valid.groupby(field, dropna=False)
        .agg(avgMortality=("mortalityRate", "mean"), facilityCount=("ccn", "count"))
        .reset_index()
        .sort_values(["avgMortality", field], ascending=[False, True])
    )

    if top_n is not None:
        grouped = grouped.head(top_n)

    results = []
    for row in grouped.to_dict(orient="records"):
        label = row[field] if row[field] not in (None, "") else "Unknown"
        results.append(
            {
                "label": label,
                "avgMortality": _clean_number(row["avgMortality"]),
                "facilityCount": int(row["facilityCount"]),
            }
        )
    return results


@router.get("/analysis", response_model=AnalysisResponse)
def get_analysis(
    year: int | None = Query(default=None),
    month: int | None = Query(default=None),
    state: str | None = Query(default=None),
    zipCode: str | None = Query(default=None),
    facilityName: str | None = Query(default=None),
) -> AnalysisResponse:
    filtered = apply_filters(
        get_dataset(),
        year=year,
        month=month,
        state=state,
        zip_code=zipCode,
        facility_name=facilityName,
    )
    valid = filtered[filtered["hasValidMortality"]].copy()

    if valid.empty:
        return AnalysisResponse(
            monthlyTrend=[],
            byState=[],
            byZip=[],
            distribution=[],
            facilityRanking=[],
        )

    monthly = (
        valid.groupby(["year", "month", "periodLabel"], dropna=False)
        .agg(avgMortality=("mortalityRate", "mean"), facilityCount=("ccn", "count"))
        .reset_index()
        .sort_values(["year", "month"])
    )
    monthly_trend = [
        {
            "year": _int_or_none(row["year"]),
            "month": _int_or_none(row["month"]),
            "label": row["periodLabel"],
            "avgMortality": _clean_number(row["avgMortality"]),
            "facilityCount": int(row["facilityCount"]),
        }
        for row in monthly.to_dict(orient="records")
    ]

    bins = [0, 10, 15, 20, 25, 30, 40, float("inf")]
    labels = ["0-10", "10-15", "15-20", "20-25", "25-30", "30-40", "40+"]
    distribution = (
        pd.cut(valid["mortalityRate"], bins=bins, labels=labels, right=False, include_lowest=True)
        .value_counts(sort=False)
        .reset_index()
    )
    distribution.columns = ["bucket", "count"]
    distribution_points = [
        {"bucket": row["bucket"], "count": int(row["count"])}
        for row in distribution.to_dict(orient="records")
    ]

    ranking = valid.sort_values(["mortalityRate", "facilityName"], ascending=[False, True]).head(25)

    return AnalysisResponse(
        monthlyTrend=monthly_trend,
        byState=_group_average(filtered, "state", top_n=15),
        byZip=_group_average(filtered, "zipCode", top_n=15),
        distribution=distribution_points,
        facilityRanking=_serialize_ranking(ranking),
    )
