import { useEffect, useState } from "react";

import { fetchAnalysis } from "../api";
import ComparisonBarChart from "../components/charts/ComparisonBarChart";
import DistributionChart from "../components/charts/DistributionChart";
import TrendChart from "../components/charts/TrendChart";

function formatMetric(value) {
  return value === null || value === undefined ? "N/A" : value.toFixed(2);
}

export default function AnalysisPage({ filters }) {
  const [analysis, setAnalysis] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    let cancelled = false;

    async function loadData() {
      try {
        setLoading(true);
        setError("");
        const payload = await fetchAnalysis(filters);
        if (!cancelled) {
          setAnalysis(payload);
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
  }, [filters]);

  return (
    <div className="page-stack">
      {loading && <p className="status-text">Loading analysis data...</p>}
      {error && <p className="error-text">{error}</p>}

      {analysis && (
        <>
          <section className="panel">
            <h3>Mortality Trend by Month</h3>
            <TrendChart data={analysis.monthlyTrend} />
          </section>

          <div className="two-column-grid">
            <ComparisonBarChart data={analysis.byState} title="Mortality by State" />
            <ComparisonBarChart data={analysis.byZip} title="Mortality by ZIP Code" color="#b45309" />
          </div>

          <section className="panel">
            <h3>Mortality Distribution</h3>
            <DistributionChart data={analysis.distribution} />
          </section>

          <section className="panel">
            <h3>Facility Ranking</h3>
            {analysis.facilityRanking.length === 0 ? (
              <p className="empty-state">No ranking data for the current filters.</p>
            ) : (
              <div className="table-scroll">
                <table>
                  <thead>
                    <tr>
                      <th>Facility</th>
                      <th>State</th>
                      <th>ZIP</th>
                      <th>Mortality</th>
                      <th>Category</th>
                    </tr>
                  </thead>
                  <tbody>
                    {analysis.facilityRanking.map((facility) => (
                      <tr key={facility.ccn}>
                        <td>{facility.facilityName}</td>
                        <td>{facility.state}</td>
                        <td>{facility.zipCode}</td>
                        <td>{formatMetric(facility.mortalityRate)}</td>
                        <td>{facility.mortalityCategory}</td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            )}
          </section>
        </>
      )}
    </div>
  );
}
