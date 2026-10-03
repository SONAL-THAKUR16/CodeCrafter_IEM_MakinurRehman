import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_case_1_negation_handling():
    """
    CASE 1: 'I am not stressed about the exam.'
    Expected: low stress, negation detected.
    """
    response = client.post("/api/analyze", json={"text": "I am not stressed about the exam."})
    assert response.status_code == 200
    data = response.json()["analysis"]
    
    assert data["signals"]["stress"] < 0.35
    assert data["overall_severity"] == "LOW"
    assert any("negation" in e["evidence"].lower() for e in data["evidence"])


def test_case_2_high_intensity_and_overload():
    """
    CASE 2: 'I am extremely overwhelmed by the amount of coursework.'
    Expected: high cognitive overload, high workload difficulty, high stress, strong intensity.
    """
    response = client.post("/api/analyze", json={"text": "I am extremely overwhelmed by the amount of coursework."})
    assert response.status_code == 200
    data = response.json()["analysis"]
    
    assert data["signals"]["stress"] >= 0.70
    assert data["signals"]["workload_difficulty"] >= 0.70
    assert data["overall_severity"] == "HIGH"
    assert data["academic_context"]["workload_pressure"] is True


def test_case_3_mixed_context_and_prioritization():
    """
    CASE 3: 'I enjoy this subject, but I have too many assignments and I don't know what to prioritize.'
    Expected: positive evidence exists, workload pressure detected, choice/prioritization difficulty detected, mixed context.
    """
    response = client.post("/api/analyze", json={"text": "I enjoy this subject, but I have too many assignments and I don't know what to prioritize."})
    assert response.status_code == 200
    data = response.json()["analysis"]
    
    assert data["sentiment"]["label"] == "mixed"
    assert data["academic_context"]["workload_pressure"] is True
    assert data["academic_context"]["choice_difficulty"] is True
    assert any(e["category"] in ["positive_engagement", "positive_sentiment"] for e in data["evidence"])


def test_case_4_simple_difficulty_not_severe_stress():
    """
    CASE 4: 'The course is difficult.'
    Expected: difficulty signal, do not automatically classify as severe stress.
    """
    response = client.post("/api/analyze", json={"text": "The course is difficult."})
    assert response.status_code == 200
    data = response.json()["analysis"]
    
    assert data["signals"]["workload_difficulty"] > 0
    assert data["signals"]["stress"] < 0.40
    assert data["overall_severity"] != "HIGH"


def test_case_5_difficulty_with_positive_enjoyment():
    """
    CASE 5: 'The course is difficult, but I am enjoying it and learning a lot.'
    Expected: positive/engaged context, difficulty detected, avoid incorrectly classifying as highly negative.
    """
    response = client.post("/api/analyze", json={"text": "The course is difficult, but I am enjoying it and learning a lot."})
    assert response.status_code == 200
    data = response.json()["analysis"]
    
    assert data["sentiment"]["label"] in ["mixed", "positive"]
    assert data["signals"]["workload_difficulty"] > 0
    assert data["overall_severity"] != "HIGH"
    assert any("enjoying" in e["evidence"].lower() or "learning" in e["evidence"].lower() for e in data["evidence"])


def test_case_6_time_pressure_and_cognitive_overload():
    """
    CASE 6: 'I have three assignments due tomorrow and I cannot concentrate.'
    Expected: workload pressure, time pressure, cognitive overload, high severity.
    """
    response = client.post("/api/analyze", json={"text": "I have three assignments due tomorrow and I cannot concentrate."})
    assert response.status_code == 200
    data = response.json()["analysis"]
    
    assert data["signals"]["time_pressure"] >= 0.70
    assert data["signals"]["cognitive_overload"] >= 0.70
    assert data["overall_severity"] == "HIGH"
    assert data["academic_context"]["time_pressure"] is True
    assert data["academic_context"]["cognitive_load"] is True


def test_case_7_workload_negation():
    """
    CASE 7: 'I don't have any problems with the workload.'
    Expected: workload difficulty should be low, negation should be handled.
    """
    response = client.post("/api/analyze", json={"text": "I don't have any problems with the workload."})
    assert response.status_code == 200
    data = response.json()["analysis"]
    
    assert data["signals"]["workload_difficulty"] <= 0.25
    assert data["signals"]["stress"] <= 0.25
    assert data["overall_severity"] == "LOW"


def test_case_8_low_intensity_modifier():
    """
    CASE 8: 'I am slightly worried about one assignment.'
    Expected: low/moderate concern, intensity lower than an 'extremely overwhelmed' statement.
    """
    response_mild = client.post("/api/analyze", json={"text": "I am slightly worried about one assignment."})
    response_high = client.post("/api/analyze", json={"text": "I am extremely overwhelmed by assignments."})
    
    assert response_mild.status_code == 200
    assert response_high.status_code == 200
    
    data_mild = response_mild.json()["analysis"]
    data_high = response_high.json()["analysis"]
    
    assert data_mild["signals"]["stress"] < data_high["signals"]["stress"]
    assert data_mild["overall_severity"] in ["LOW", "MODERATE"]
