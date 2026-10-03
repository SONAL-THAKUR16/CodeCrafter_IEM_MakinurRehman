# EduSense AI — Student Academic Experience & Emotion Analyzer

[![Backend Tests](https://img.shields.io/badge/pytest-31%20passed-emerald)](https://github.com/SONAL-THAKUR16/CodeCrafter_IEM_MakinurRehman)
[![Frontend Build](https://img.shields.io/badge/vite-v8.3.2%20build%20passing-indigo)](https://github.com/SONAL-THAKUR16/CodeCrafter_IEM_MakinurRehman)
[![Python](https://img.shields.io/badge/python-3.10%2B-blue)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-v0.115%2B-009688)](https://fastapi.tiangolo.com/)
[![React](https://img.shields.io/badge/React-v19-61dafb)](https://react.dev/)

**EduSense AI** is a context-aware student feedback analysis platform built for educational institutions to detect signals of **stress, cognitive overload, frustration, disengagement, and workload difficulty** from qualitative student responses.

👉 [View Project Presentation Deck](https://docs.google.com/presentation/d/1LL4XcUcwB-SYawPCfesOR3KWkVZwZ0av/edit?usp=drivesdk&ouid=103757897487667590142&rtpof=true&sd=true)

---

## 1. Hackathon & Team Information

* **Team Name**: CodeCrafter
* **College**: Institute of Engineering and Management (IEM)
* **Team Leader**: Makinur Rahaman
* **GitHub Repository**: [CodeCrafter_IEM_MakinurRehman](https://github.com/SONAL-THAKUR16/CodeCrafter_IEM_MakinurRehman)

---

## 2. Problem Statement

Students express their academic experiences through emails, forums, feedback forms, learning platforms, and journals. These texts contain crucial indications of stress, cognitive overload, frustration, disengagement, and workload-related difficulties. Manually analyzing large volumes of qualitative responses is time-consuming, while generic keyword-based classifiers fail because they lack understanding of:
- **Context & Scope**
- **Negation** (e.g. *"I am not stressed about the exam"*)
- **Intensity Multipliers** (e.g. *"extremely overwhelmed"* vs *"slightly worried"*)
- **Mixed Sentiments & Contrasts** (e.g. *"I love this course, but the workload is too heavy"*)

---

## 3. Our Solution & Approach

EduSense AI combines open-source Hugging Face Transformer models (`distilbert-base-uncased-finetuned-sst-2-english`) with a context-aware linguistic scoring engine. It analyzes student feedback, extracts verbatim phrase evidence with severity impact ratings, and persists results to provide real-time institutional dashboard analytics.

---

## 4. Key Features

- **Context-Aware NLP Pipeline**: Evaluates negation scope, intensity multipliers, and clause-level contrasts.
- **Explainable Evidence Extraction**: Answers *"Why did the system detect this?"* by extracting exact text snippets with severity impact tags (`HIGH`, `MEDIUM`, `LOW`).
- **6 Academic Distress Dimensions**: Tracks Stress, Cognitive Overload, Frustration, Disengagement, Workload Difficulty, Time Pressure, and Choice Difficulty.
- **Non-Clinical Student Insights**: Generates neutral, student-focused experience assessments without medical diagnosis labeling.
- **SQLite Persistence**: Stores complete analysis records and assigns unique identifiers (`anl_YYYYMMDDHHMMSS_xxxxxx`).
- **Institutional Analytics Dashboard**: Visualizes severity distribution (Donut Chart), signal comparison averages (Horizontal Bar Chart), and distress progression (Multi-Line Chart).
- **Filterable Session History**: Client-side pill filtering by severity with 1-click session inspection.

---

## 5. System Architecture

```
[React UI (Vite + Tailwind + Recharts)]
                  ↓ HTTP / Axios
[FastAPI REST API Layer (main.py / routes/analysis.py)]
                  ↓
   ┌──────────────┴────────────────────────┐
   ▼                                       ▼
[Context-Aware NLP Engine]        [SQLite Persistence Layer]
  • Transformer Sentiment           • SQLAlchemy ORM
  • Clause Contrast Parser          • Analysis Records Table
  • Negation Scope Engine           • History & Trends Query
  • Evidence Extractor              • Real-Time Metrics Aggregator
```

---

## 6. Technology Stack

### Frontend
- **Framework**: React 19 (Vite)
- **Styling**: Tailwind CSS v4
- **Charts**: Recharts
- **HTTP Client**: Axios
- **Icons**: Lucide React

### Backend & AI/NLP
- **API Framework**: Python 3.10+ / FastAPI / Uvicorn
- **NLP Models**: Hugging Face Transformers (`distilbert-base-uncased-finetuned-sst-2-english`), PyTorch
- **Validation**: Pydantic v2
- **ORM & Database**: SQLAlchemy / SQLite (`data/student_analysis.db`)

---

## 7. Context-Aware Analysis vs Keyword Classification

| Student Input | Keyword Classifier Result | EduSense AI Context Result |
| :--- | :--- | :--- |
| `"I am stressed."` | High Stress | **Stress: 60%** (Moderate Signal) |
| `"I am not stressed."` | High Stress (matches "stressed") | **Stress: 5%** (Negation recognized, Low Signal) |
| `"I am overwhelmed by my workload."` | High Distress | **Stress: 94%, Workload: 85%** (High Signal) |
| `"I am not overwhelmed by my workload."` | High Distress | **Stress: 14%, Workload: 15%** (Low Signal) |
| `"The course is difficult, but I enjoy learning it."` | Negative | **Mixed Sentiment** (Positive engagement balancing workload) |

---

## 8. Database Schema & Persistence

SQLite database automatically initialized at `data/student_analysis.db` (ignored by Git):

- `id` (VARCHAR 64, PK): Unique transaction ID (`anl_20261003122845_a95c2c`)
- `input_text` (TEXT): Anonymous student feedback text
- `sentiment_label` (VARCHAR 32): `positive`, `negative`, `neutral`, or `mixed`
- `sentiment_scores` (JSON): Confidence probability breakdown
- `emotion_results` (JSON): Emotion classification list
- `stress_score` / `cognitive_overload_score` / `workload_difficulty_score` (FLOAT): 0.0 to 1.0
- `overall_severity` (VARCHAR 16): `LOW`, `MODERATE`, or `HIGH`
- `primary_concern` (VARCHAR 64): Dominant academic experience concern
- `evidence` (JSON): Extracted phrases with category and impact level
- `explanation` (TEXT) & `student_insight` (TEXT): Natural language summaries
- `created_at` (DATETIME): Timestamp

---

## 9. API Endpoints

| Method | Endpoint | Description |
| :--- | :--- | :--- |
| `GET` | `/api/health` | Health check endpoint returning backend & DB status |
| `POST` | `/api/analyze` | Analyzes student feedback via NLP and persists record in SQLite |
| `GET` | `/api/analyze/{analysis_id}` | Retrieves stored analysis record by unique ID |
| `GET` | `/api/history` | Retrieves recent analysis records (`?limit=20`, newest first) |
| `GET` | `/api/dashboard/summary` | Calculates real-time summary statistics for frontend dashboard |
| `GET` | `/api/dashboard/trends` | Retrieves time-series trend data points for chart visualization |
| `GET` | `/docs` | Interactive Swagger UI documentation |

---

## 10. Quick Start & Installation

### Prerequisites
- Python 3.10+
- Node.js v18+ & npm

### 1. Backend Setup
```bash
cd backend

# Install dependencies
pip install -r requirements.txt

# Seed demo dataset (optional)
python -m app.seed_demo_data

# Run unit test suite (31 tests)
python -m pytest tests/

# Start FastAPI server
uvicorn app.main:app --reload --port 8000
```
Backend API will be accessible at `http://127.0.0.1:8000` (Docs: `http://127.0.0.1:8000/docs`).

### 2. Frontend Setup
```bash
cd frontend

# Install dependencies
npm install

# Start Vite dev server
npm run dev
```
Frontend will be accessible at `http://localhost:3000`.

---

## 11. Judge Demonstration Script

A step-by-step 2-minute judge walkthrough guide is available at [docs/DEMO_SCRIPT.md](file:///c:/Users/RUPAM%20SUR/Desktop/CodeCrafter_IEM_MakinurRahaman/docs/DEMO_SCRIPT.md).

---

## 12. Project Limitations & Ethical Intent

- **Non-Clinical Intent**: EduSense AI evaluates linguistic and academic experience signals for educational feedback analysis. It is **not** a psychological or medical diagnosis system.
- **Local Prototype Scope**: Built as an 8-hour hackathon MVP; trained on local open-source models without cloud LLM dependencies.
