import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_health_endpoint():
    """Test /api/health endpoint returns required payload format."""
    response = client.get("/api/health")
    assert response.status_code == 200
    assert response.json() == {
        "status": "ok",
        "service": "student-emotional-analysis-api"
    }


def test_analyze_normal_sentence():
    """Test /api/analyze with valid student academic feedback."""
    payload = {"text": "I have too many assignments and I am feeling overwhelmed."}
    response = client.post("/api/analyze", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert "analysis" in data
    assert "analysis_id" in data
    
    analysis = data["analysis"]
    signals = analysis["signals"]
    assert 0.0 <= signals["stress"] <= 1.0
    assert 0.0 <= signals["cognitive_overload"] <= 1.0
    assert 0.0 <= signals["frustration"] <= 1.0
    assert 0.0 <= signals["disengagement"] <= 1.0
    assert 0.0 <= signals["workload_difficulty"] <= 1.0
    assert analysis["overall_severity"] in ["LOW", "MODERATE", "HIGH"]
    assert isinstance(analysis["explanation"], str)


def test_analyze_empty_string():
    """Test /api/analyze with empty string returns validation error."""
    payload = {"text": ""}
    response = client.post("/api/analyze", json=payload)
    assert response.status_code in [400, 422]
    data = response.json()
    assert data["success"] is False


def test_analyze_whitespace_only():
    """Test /api/analyze with whitespace string returns validation error."""
    payload = {"text": "   \n\t  "}
    response = client.post("/api/analyze", json=payload)
    assert response.status_code in [400, 422]
    data = response.json()
    assert data["success"] is False


def test_analyze_invalid_json():
    """Test /api/analyze with invalid request body."""
    response = client.post(
        "/api/analyze",
        content="not valid json",
        headers={"Content-Type": "application/json"}
    )
    assert response.status_code == 422


def test_analyze_overly_long_input():
    """Test /api/analyze exceeding maximum text length limit (5000 chars)."""
    long_text = "stress " * 1000  # 7000 characters
    payload = {"text": long_text}
    response = client.post("/api/analyze", json=payload)
    assert response.status_code == 422
    data = response.json()
    assert data["success"] is False


def test_get_analysis_by_id():
    """Test /api/analyze/{id} structure returning 404 for non-existent record."""
    response = client.get("/api/analyze/anl_test_123")
    assert response.status_code == 404
    data = response.json()
    assert "detail" in data
    assert "not found" in data["detail"].lower()


def test_get_history():
    """Test /api/history endpoint structure."""
    response = client.get("/api/history")
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert data["count"] >= 0
    assert isinstance(data["history"], list)


def test_swagger_docs():
    """Test /docs and /openapi.json availability."""
    docs_response = client.get("/docs")
    assert docs_response.status_code == 200
    
    openapi_response = client.get("/openapi.json")
    assert openapi_response.status_code == 200
    assert "openapi" in openapi_response.json()
