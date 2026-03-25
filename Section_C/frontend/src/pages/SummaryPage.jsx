import { useEffect, useState } from "react";

import { fetchSummary, fetchTable } from "../api";
import DataTable from "../components/DataTable";

function formatMetric(value) {
  return value === null || value === undefined ? "N/A" : value.toFixed(2);
}

function RankingList({ title, items }) {
  return (
    <section className="panel">
      <h3>{title}</h3>
      {items.length === 0 ? (
        <p className="empty-state">No facilities to display.</p>
      ) : (
        <ol className="ranking-list">
          {items.map((item) => (
            <li key={`${title}-${item.ccn}`}>
              <span>{item.facilityName}</span>
              <strong>{formatMetric(item.mortalityRate)}</strong>
            </li>
          ))}
        </ol>
      )}
    </section>
  );
}

export default function SummaryPage({ filters }) {
  const [summary, setSummary] = useState(null);
  const [table, setTable] = useState({ data: [], page: 1, pageSize: 25, total: 0 });
  const [page, setPage] = useState(1);
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    setPage(1);
  }, [filters]);

  useEffect(() => {
    let cancelled = false;

    async function loadData() {
      try {
        setLoading(true);
        setError("");
        const [summaryPayload, tablePayload] = await Promise.all([
          fetchSummary(filters),
          fetchTable(filters, page, table.pageSize),
        ]);
        if (!cancelled) {
          setSummary(summaryPayload);
          setTable(tablePayload);
        }
      } catch (requestError) {
        if (!cancelled) {
          setError(requestError.message);
        }
      } finally {
        if (!cancelled) {
          setLoading(false);
        }
      }
    }

    loadData();
    return () => {
      cancelled = true;
    };
  }, [filters, page, table.pageSize]);

  return (
    <div className="page-stack">
      {loading && <p className="status-text">Loading summary data...</p>}
      {error && <p className="error-text">{error}</p>}

      {summary && (
        <>
          <section className="metrics-grid">
            <article className="metric-card">
              <h3>Total Facilities</h3>
              <p>{summary.total}</p>
            </article>
            <article className="metric-card">
              <h3>Average Mortality</h3>
              <p>{formatMetric(summary.avgMortality)}</p>
            </article>
            <article className="metric-card">
              <h3>Min Mortality</h3>
              <p>{formatMetric(summary.minMortality)}</p>
            </article>
            <article className="metric-card">
              <h3>Max Mortality</h3>
              <p>{formatMetric(summary.maxMortality)}</p>
            </article>
          </section>

          <section className="two-column-grid">
            <RankingList title="Top 10 Highest Mortality" items={summary.top10Highest} />
            <RankingList title="Top 10 Lowest Mortality" items={summary.top10Lowest} />
          </section>
        </>
      )}

      <DataTable
        rows={table.data}
        page={table.page}
        pageSize={table.pageSize}
        total={table.total}
        onPageChange={setPage}
      />
    </div>
  );
}
