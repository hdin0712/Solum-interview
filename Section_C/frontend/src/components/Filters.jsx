const EMPTY_FILTERS = {
  year: "",
  month: "",
  state: "",
  zipCode: "",
  facilityName: "",
};

export default function Filters({ filters, onChange, options }) {
  function handleInputChange(event) {
    const { name, value } = event.target;
    onChange({ ...filters, [name]: value });
  }

  return (
    <section className="panel">
      <div className="filters-grid">
        <label>
          Year
          <select name="year" value={filters.year} onChange={handleInputChange}>
            <option value="">All</option>
            {options.years.map((year) => (
              <option key={year} value={year}>
                {year}
              </option>
            ))}
          </select>
        </label>

        <label>
          Month
          <select name="month" value={filters.month} onChange={handleInputChange}>
            <option value="">All</option>
            {options.months.map((month) => (
              <option key={month.value} value={month.value}>
                {month.label}
              </option>
            ))}
          </select>
        </label>

        <label>
          State
          <select name="state" value={filters.state} onChange={handleInputChange}>
            <option value="">All</option>
            {options.states.map((state) => (
              <option key={state} value={state}>
                {state}
              </option>
            ))}
          </select>
        </label>

        <label>
          ZIP Code
          <input
            name="zipCode"
            value={filters.zipCode}
            onChange={handleInputChange}
            placeholder="e.g. 900"
          />
        </label>

        <label>
          Facility Name
          <input
            name="facilityName"
            value={filters.facilityName}
            onChange={handleInputChange}
            placeholder="Search by facility"
          />
        </label>

        <div className="filter-actions">
          <button type="button" className="secondary-button" onClick={() => onChange(EMPTY_FILTERS)}>
            Reset Filters
          </button>
        </div>
      </div>
    </section>
  );
}
