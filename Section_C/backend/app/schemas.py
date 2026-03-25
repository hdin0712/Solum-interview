from __future__ import annotations

from typing import Any

from pydantic import BaseModel


class FacilityRecord(BaseModel):
    ccn: str
    facilityName: str
    state: str
    zipCode: str
    city: str
    mortalityRate: float | None
    mortalityCategory: str
    mortalityAvailabilityCode: str
    patientsInSummary: int | None
    year: int | None
    month: int | None
    periodLabel: str


class RankingRecord(BaseModel):
    ccn: str
    facilityName: str
    state: str
    zipCode: str
    mortalityRate: float
    mortalityCategory: str
    patientsInSummary: int | None


class SummaryResponse(BaseModel):
    total: int
    avgMortality: float | None
    minMortality: float | None
    maxMortality: float | None
    top10Highest: list[RankingRecord]
    top10Lowest: list[RankingRecord]


class TableResponse(BaseModel):
    data: list[FacilityRecord]
    page: int
    pageSize: int
    total: int


class TrendPoint(BaseModel):
    year: int | None
    month: int | None
    label: str
    avgMortality: float | None
    facilityCount: int


class GroupPoint(BaseModel):
    label: str
    avgMortality: float | None
    facilityCount: int


class DistributionPoint(BaseModel):
    bucket: str
    count: int


class AnalysisResponse(BaseModel):
    monthlyTrend: list[TrendPoint]
    byState: list[GroupPoint]
    byZip: list[GroupPoint]
    distribution: list[DistributionPoint]
    facilityRanking: list[RankingRecord]


class FilterOptionsResponse(BaseModel):
    years: list[int]
    months: list[dict[str, Any]]
    states: list[str]
