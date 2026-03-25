from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_healthcheck() -> None:
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_filters_endpoint_has_values() -> None:
    response = client.get("/api/filters")
    assert response.status_code == 200
    payload = response.json()
    assert payload["years"]
    assert payload["months"]
    assert payload["states"]


def test_summary_endpoint_returns_expected_shape() -> None:
    response = client.get("/api/summary")
    assert response.status_code == 200
    payload = response.json()
    assert payload["total"] > 0
    assert "avgMortality" in payload
    assert len(payload["top10Highest"]) <= 10
    assert len(payload["top10Lowest"]) <= 10


def test_table_endpoint_paginates() -> None:
    response = client.get("/api/table", params={"page": 2, "pageSize": 10})
    assert response.status_code == 200
    payload = response.json()
    assert payload["page"] == 2
    assert payload["pageSize"] == 10
    assert len(payload["data"]) <= 10


def test_zero_results_return_empty_collections() -> None:
    response = client.get("/api/analysis", params={"facilityName": "zzzzzz-not-a-real-facility"})
    assert response.status_code == 200
    payload = response.json()
    assert payload["monthlyTrend"] == []
    assert payload["byState"] == []
    assert payload["byZip"] == []
    assert payload["distribution"] == []
    assert payload["facilityRanking"] == []
