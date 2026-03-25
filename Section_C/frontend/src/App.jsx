import { NavLink, Route, Routes } from "react-router-dom";
import { useEffect, useState } from "react";

import { fetchFilterOptions } from "./api";
import Filters from "./components/Filters";
import AnalysisPage from "./pages/AnalysisPage";
import SummaryPage from "./pages/SummaryPage";

const INITIAL_FILTERS = {
  year: "",
  month: "",
  state: "",
  zipCode: "",
  facilityName: "",
};

const EMPTY_OPTIONS = {
  years: [],
  months: [],
  states: [],
};

export default function App() {
  const [filters, setFilters] = useState(INITIAL_FILTERS);
  const [options, setOptions] = useState(EMPTY_OPTIONS);
  const [loadingFilters, setLoadingFilters] = useState(true);
  const [filterError, setFilterError] = useState("");

  useEffect(() => {
    let cancelled = false;

    async function loadFilterOptions() {
      try {
        setLoadingFilters(true);
        const payload = await fetchFilterOptions();
        if (!cancelled) {
          setOptions(payload);
        }
      } catch (error) {
        if (!cancelled) {
          setFilterError(error.message);
        }
      } finally {
        if (!cancelled) {
          setLoadingFilters(false);
        }
      }
    }

    loadFilterOptions();
    return () => {
      cancelled = true;
    };
  }, []);

  return (
    <div className="app-shell">
      <header className="hero">
        <div>
          <h1>CMS Dialysis Mortality Analysis</h1>
        </div>

        <nav className="nav-tabs">
          <NavLink to="/" end>
            Summary
          </NavLink>
          <NavLink to="/analysis">Analysis</NavLink>
        </nav>
      </header>

      {loadingFilters ? (
        <p className="status-text">Loading filter options...</p>
      ) : (
        <Filters filters={filters} onChange={setFilters} options={options} />
      )}
      {filterError && <p className="error-text">{filterError}</p>}

      <main>
        <Routes>
          <Route path="/" element={<SummaryPage filters={filters} />} />
          <Route path="/analysis" element={<AnalysisPage filters={filters} />} />
        </Routes>
      </main>
    </div>
  );
}
