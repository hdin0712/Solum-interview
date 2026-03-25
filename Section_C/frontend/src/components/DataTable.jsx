function formatMortality(value) {
  return value === null || value === undefined ? "N/A" : value.toFixed(2);
}

export default function DataTable({ rows, page, pageSize, total, onPageChange }) {
  const totalPages = Math.max(1, Math.ceil(total / pageSize));

  return (
    <section className="panel">
      <div className="table-header">
        <h3>Facility Table</h3>
        <div className="pagination-controls">
          <button type="button" disabled={page <= 1} onClick={() => onPageChange(page - 1)}>
            Previous
          </button>
          <span>
            Page {page} of {totalPages}
          </span>
          <button type="button" disabled={page >= totalPages} onClick={() => onPageChange(page + 1)}>
            Next
          </button>
        </div>
      </div>

      {rows.length === 0 ? (
        <p className="empty-state">No facilities match the current filters.</p>
      ) : (
        <div className="table-scroll">
          <table>
            <thead>
              <tr>
                <th>Facility</th>
                <th>CCN</th>
                <th>State</th>
                <th>ZIP</th>
                <th>City</th>
                <th>Mortality</th>
                <th>Category</th>
                <th>Patients</th>
                <th>Period</th>
              </tr>
            </thead>
            <tbody>
              {rows.map((row) => (
                <tr key={row.ccn}>
                  <td>{row.facilityName}</td>
                  <td>{row.ccn}</td>
                  <td>{row.state}</td>
                  <td>{row.zipCode}</td>
                  <td>{row.city}</td>
                  <td>{formatMortality(row.mortalityRate)}</td>
                  <td>{row.mortalityCategory}</td>
                  <td>{row.patientsInSummary ?? "N/A"}</td>
                  <td>{row.periodLabel}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </section>
  );
}
