# Section C Mortality Analysis App

This section implements a small full-stack application for analyzing `Mortality Rate (Facility)` from the CMS dialysis facility dataset in `DFC_FACILITY.csv`.

## Architecture

- `backend/`: FastAPI + pandas API layer
- `frontend/`: React + Vite UI
- data source: `../DFC_FACILITY.csv`

The backend loads the CSV once, normalizes mortality values, derives `year` and `month` from `Certification Date`, and exposes filtered summary, table, and analysis endpoints.

The frontend provides:

- shared filters for year, month, state, ZIP code, and facility name
- a Summary page with KPI cards, top/bottom rankings, and a paginated table
- an Analysis page with monthly trend, state and ZIP comparisons, mortality distribution, and a facility ranking table

## Dataset Assumptions

- `Mortality Rate (Facility)` is the measure used for all mortality math.
- `Patient Survival data availability code == 001` is treated as valid for mortality calculations.
- missing or invalid mortality values are excluded from averages, min/max, rankings, and analysis charts.
- the table endpoint still returns matching facilities even if mortality is unavailable.
- `Certification Date` is used to derive the filterable `year` and `month` fields.

## Backend Setup

From `Section_C/backend`:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Backend URLs:

- API root: `http://localhost:8000`
- healthcheck: `http://localhost:8000/health`
- docs: `http://localhost:8000/docs`

### Backend Endpoints

- `GET /api/filters`
- `GET /api/summary`
- `GET /api/table?page=1&pageSize=25`
- `GET /api/analysis`

Supported query params on the data endpoints:

- `year`
- `month`
- `state`
- `zipCode`
- `facilityName`

## Frontend Setup

From `Section_C/frontend`:

```bash
npm install
npm run dev
```

The Vite app runs on `http://localhost:5173` and expects the backend at `http://localhost:8000`.

If needed, override the backend base URL:

```bash
VITE_API_BASE_URL=http://localhost:8000 npm run dev
```

## Tests And Verification

Run backend smoke tests from `Section_C/backend`:

```bash
.venv/bin/pytest -q
```

The backend tests cover:

- filter metadata availability
- summary response shape
- pagination behavior
- zero-result analysis responses
- healthcheck

## Key Files

- `backend/app/main.py`
- `backend/app/data_loader.py`
- `backend/app/filters.py`
- `backend/app/routes.py`
- `backend/app/schemas.py`
- `backend/tests/test_api.py`
- `frontend/src/App.jsx`
- `frontend/src/pages/SummaryPage.jsx`
- `frontend/src/pages/AnalysisPage.jsx`
- `frontend/src/components/Filters.jsx`
- `frontend/src/components/DataTable.jsx`
