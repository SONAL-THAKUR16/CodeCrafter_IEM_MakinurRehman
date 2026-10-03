import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_health_check():
    """Verify /api/health endpoint."""
    response = client.get("/api/health")
    assert response.status_code == 200
    assert response.json() == {
        "status": "ok",
        "service": "student-emotional-analysis-api"
    }


def test_case_1_positive_experience():
    """
    TEST 1: 'I am enjoying this course and I feel confident about my assignments.'
    Expected: Positive sentiment, low stress, low overload.
    """
    payload = {"text": "I am enjoying this course and I feel confident about my assignments."}
    response = client.post("/api/analyze", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    analysis = data["analysis"]
    
    assert analysis["sentiment"]["label"] == "positive"
    assert analysis["signals"]["stress"] < 0.30
    assert analysis["signals"]["cognitive_overload"] < 0.30
    assert analysis["overall_severity"] == "LOW"


def test_case_2_workload_and_cognitive_overload():
    """
    TEST 2: 'I have four assignments due this week and I don't know which one to complete first.'
    Expected: Workload pressure, choice/priority difficulty, cognitive overload signal.
    """
    payload = {"text": "I have four assignments due this week and I don't know which one to complete first."}
    response = client.post("/api/analyze", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    analysis = data["analysis"]

    assert analysis["signals"]["workload_difficulty"] >= 0.60
    assert analysis["signals"]["cognitive_overload"] >= 0.60
    assert analysis["overall_severity"] in ["MODERATE", "HIGH"]
    assert any("assignments" in e["evidence"].lower() for e in analysis["evidence"])


def test_case_3_negation_handling():
    """
    TEST 3: 'I am not stressed about the upcoming exam.'
    Expected: Negation recognized, stress should not be strongly triggered by the word 'stressed'.
    """
    payload = {"text": "I am not stressed about the upcoming exam."}
    response = client.post("/api/analyze", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    analysis = data["analysis"]

    # Stress score should be low because of negation
    assert analysis["signals"]["stress"] < 0.35
    assert analysis["overall_severity"] == "LOW"
    assert any("negation" in e["evidence"].lower() for e in analysis["evidence"])


def test_case_4_high_distress_and_overload():
    """
    TEST 4: 'I am extremely overwhelmed. I cannot concentrate and I feel like I have too much work.'
    Expected: High stress signal, high cognitive overload signal, high workload difficulty, strong negative emotion/sentiment.
    """
    payload = {"text": "I am extremely overwhelmed. I cannot concentrate and I feel like I have too much work."}
    response = client.post("/api/analyze", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    analysis = data["analysis"]

    assert analysis["signals"]["stress"] >= 0.70
    assert analysis["signals"]["cognitive_overload"] >= 0.70
    assert analysis["signals"]["workload_difficulty"] >= 0.70
    assert analysis["overall_severity"] == "HIGH"
    assert analysis["sentiment"]["label"] == "negative"


def test_case_5_mixed_context_and_frustration():
    """
    TEST 5: 'The course is fine, but the number of assignments is becoming frustrating.'
    Expected: Mixed context, workload difficulty, frustration.
    """
    payload = {"text": "The course is fine, but the number of assignments is becoming frustrating."}
    response = client.post("/api/analyze", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    analysis = data["analysis"]

    assert analysis["signals"]["frustration"] >= 0.50
    assert analysis["signals"]["workload_difficulty"] >= 0.50
    assert analysis["overall_severity"] in ["MODERATE", "HIGH"]


def test_disclaimer_present():
    """Verify system disclaimer is present in response."""
    payload = {"text": "I am feeling a bit tired after the exam."}
    response = client.post("/api/analyze", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "disclaimer" in data["analysis"]
    assert "not a medical" in data["analysis"]["disclaimer"].lower()
