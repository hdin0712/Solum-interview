const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || "http://localhost:8000";

function buildQueryString(filters = {}, extraParams = {}) {
  const params = new URLSearchParams();
  const merged = { ...filters, ...extraParams };

  Object.entries(merged).forEach(([key, value]) => {
    if (value !== "" && value !== null && value !== undefined) {
      params.set(key, value);
    }
  });

  const query = params.toString();
  return query ? `?${query}` : "";
}

async function request(path, filters = {}, extraParams = {}) {
  const response = await fetch(`${API_BASE_URL}${path}${buildQueryString(filters, extraParams)}`);

  if (!response.ok) {
    throw new Error(`Request failed with status ${response.status}`);
  }

  return response.json();
}

function normalizeRankingItem(item = {}) {
  return {
    ccn: item.ccn ?? item.CCN ?? `${item.facility_name ?? item.facilityName ?? "facility"}-${item.zip_code ?? item.zipCode ?? ""}`,
    facilityName: item.facilityName ?? item.facility_name ?? "",
    state: item.state ?? "",
    zipCode: item.zipCode ?? item.zip_code ?? "",
    mortalityRate: item.mortalityRate ?? item.mortality_rate ?? null,
    mortalityCategory: item.mortalityCategory ?? item.mortality_category ?? "",
    patientsInSummary: item.patientsInSummary ?? item.patients_in_summary ?? null,
    periodLabel: item.periodLabel ?? item.report_date ?? item.period ?? "",
  };
}

function normalizeTableRow(row = {}) {
  return {
    ccn: row.ccn ?? "",
    facilityName: row.facilityName ?? row.facility_name ?? "",
    state: row.state ?? "",
    zipCode: row.zipCode ?? row.zip_code ?? "",
    city: row.city ?? "",
    mortalityRate: row.mortalityRate ?? row.mortality_rate ?? null,
    mortalityCategory: row.mortalityCategory ?? row.mortality_category ?? "",
    mortalityAvailabilityCode:
      row.mortalityAvailabilityCode ?? row.mortality_availability_code ?? "",
    patientsInSummary: row.patientsInSummary ?? row.patients_in_summary ?? null,
    year: row.year ?? null,
    month: row.month ?? null,
    periodLabel: row.periodLabel ?? row.report_date ?? "",
  };
}

export function fetchFilterOptions() {
  return request("/api/filters");
}

export async function fetchSummary(filters) {
  const payload = await request("/api/summary", filters);
  return {
    total: payload.total ?? 0,
    avgMortality: payload.avgMortality ?? payload.avg_mortality ?? null,
    minMortality: payload.minMortality ?? payload.min_mortality ?? null,
    maxMortality: payload.maxMortality ?? payload.max_mortality ?? null,
    top10Highest: (payload.top10Highest ?? payload.top10_highest ?? []).map(normalizeRankingItem),
    top10Lowest: (payload.top10Lowest ?? payload.top10_lowest ?? []).map(normalizeRankingItem),
  };
}

export async function fetchTable(filters, page, pageSize) {
  const payload = await request("/api/table", filters, { page, pageSize });
  return {
    data: (payload.data ?? []).map(normalizeTableRow),
    page: payload.page ?? 1,
    pageSize: payload.pageSize ?? payload.page_size ?? pageSize,
    total: payload.total ?? 0,
  };
}

export async function fetchAnalysis(filters) {
  const payload = await request("/api/analysis", filters);
  return {
    monthlyTrend: (payload.monthlyTrend ?? payload.monthly_trend ?? []).map((item) => ({
      year: item.year ?? null,
      month: item.month ?? null,
      label: item.label ?? item.period ?? item.periodLabel ?? "",
      avgMortality: item.avgMortality ?? item.avg_mortality ?? null,
      facilityCount: item.facilityCount ?? item.facility_count ?? 0,
    })),
    byState: (payload.byState ?? payload.by_state ?? []).map((item) => ({
      label: item.label ?? item.state ?? "",
      avgMortality: item.avgMortality ?? item.avg_mortality ?? null,
      facilityCount: item.facilityCount ?? item.facility_count ?? 0,
    })),
    byZip: (payload.byZip ?? payload.by_zip ?? []).map((item) => ({
      label: item.label ?? item.zip_code ?? item.zipCode ?? "",
      avgMortality: item.avgMortality ?? item.avg_mortality ?? null,
      facilityCount: item.facilityCount ?? item.facility_count ?? 0,
    })),
    distribution: (payload.distribution ?? []).map((item) => ({
      bucket:
        item.bucket ??
        (item.bucketStart !== undefined && item.bucketEnd !== undefined
          ? `${item.bucketStart}-${item.bucketEnd}`
          : ""),
      count: item.count ?? item.facilityCount ?? item.facility_count ?? 0,
    })),
    facilityRanking: (payload.facilityRanking ?? payload.facility_ranking ?? payload.ranking ?? []).map(
      normalizeRankingItem
    ),
  };
}
