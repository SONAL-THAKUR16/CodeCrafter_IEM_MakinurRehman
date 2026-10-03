import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_database_initialization():
    """Verify health and database readiness."""
    response = client.get("/api/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_post_analyze_creates_db_record():
    """Verify POST /api/analyze persists record and returns valid analysis_id."""
    payload = {"text": "I am feeling overwhelmed by four assignments due tomorrow."}
    response = client.post("/api/analyze", json=payload)
    assert response.status_code == 200
    
    data = response.json()
    assert data["success"] is True
    assert "analysis_id" in data
    assert data["analysis_id"].startswith("anl_")
    assert data["analysis"]["overall_severity"] in ["MODERATE", "HIGH"]


def test_get_analysis_by_valid_id():
    """Verify GET /api/analyze/{analysis_id} fetches stored record."""
    # First create a record
    post_res = client.post("/api/analyze", json={"text": "I have four assignments due this week and heavy coursework."})
    analysis_id = post_res.json()["analysis_id"]
    
    # Retrieve record
    get_res = client.get(f"/api/analyze/{analysis_id}")
    assert get_res.status_code == 200
    get_data = get_res.json()
    assert get_data["success"] is True
    assert get_data["analysis_id"] == analysis_id
    assert get_data["analysis"]["signals"]["workload_difficulty"] > 0


def test_get_analysis_invalid_id():
    """Verify GET /api/analyze/{invalid_id} returns 404."""
    response = client.get("/api/analyze/anl_non_existent_id_999999")
    assert response.status_code == 404
    assert "not found" in response.json()["detail"].lower()


def test_get_history_limit():
    """Verify GET /api/history respects limit parameter."""
    # Submit 3 records
    for i in range(3):
        client.post("/api/analyze", json={"text": f"Feedback submission test number {i}"})

    history_res = client.get("/api/history?limit=2")
    assert history_res.status_code == 200
    h_data = history_res.json()
    assert h_data["success"] is True
    assert len(h_data["items"]) == 2
    assert "text_snippet" in h_data["items"][0]


def test_get_dashboard_summary():
    """Verify GET /api/dashboard/summary calculates valid statistics."""
    res = client.get("/api/dashboard/summary")
    assert res.status_code == 200
    data = res.json()
    assert data["success"] is True
    summary = data["summary"]
    
    assert summary["total_analyses"] >= 1
    assert 0.0 <= summary["average_stress"] <= 1.0
    assert 0.0 <= summary["average_workload_difficulty"] <= 1.0
    assert "LOW" in summary["severity_distribution"]
    assert "MODERATE" in summary["severity_distribution"]
    assert "HIGH" in summary["severity_distribution"]
    assert isinstance(summary["most_common_concern"], str)


def test_get_dashboard_trends():
    """Verify GET /api/dashboard/trends returns trend points for charts."""
    res = client.get("/api/dashboard/trends?limit=5")
    assert res.status_code == 200
    data = res.json()
    assert data["success"] is True
    assert "trends" in data
    assert isinstance(data["trends"], list)
    if len(data["trends"]) > 0:
        point = data["trends"][0]
        assert "analysis_id" in point
        assert "stress" in point
        assert "overall_severity" in point
