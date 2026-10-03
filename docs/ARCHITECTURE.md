# EduSense AI — Technical Architecture Documentation

**Project**: EduSense AI — Context-Aware Student Academic Experience & Emotion Analyzer  
**Team**: CodeCrafter  
**Institution**: Institute of Engineering and Management (IEM)  
**Team Leader**: Makinur Rahaman  

---

## Architecture Overview

EduSense AI is designed as a decoupled, multi-layered web application featuring a modern React SPA frontend and a high-performance Python FastAPI backend integrated with a local Hugging Face Transformer NLP pipeline and SQLite persistence.

```
                    ┌─────────────────────────────────────────┐
                    │          React SPA (Vite + Tailwind)    │
                    │   • Dashboard Page & Component Hierarchy │
                    │   • Recharts Data Visualizations        │
                    │   • Interactive Demo Input & History    │
                    └────────────────────┬────────────────────┘
                                         │ Axios HTTP / JSON API
                                         ▼
                    ┌─────────────────────────────────────────┐
                    │          FastAPI Backend Application    │
                    │   • CORS & Health Endpoints (/api/health)│
                    │   • Request Validation (Pydantic v2)    │
                    │   • Analysis Router (/api/analyze)      │
                    │   • History & Dashboard Stats Endpoints │
                    └────────────────────┬────────────────────┘
                                         │
                   ┌─────────────────────┴─────────────────────┐
                   ▼                                           ▼
┌──────────────────────────────────────┐     ┌──────────────────────────────────┐
│   Context-Aware NLP Analysis Engine  │     │   SQLite Persistence Layer       │
│ • Hugging Face Transformer Sentiment │     │ • SQLAlchemy ORM                 │
│ • Clause Contrast & Sentence Parser │     │ • Analysis Record Data Model     │
│ • Negation Scope Resolution Engine   │     │ • Unique ID Transaction Engine   │
│ • Academic Signal & Evidence Scorer  │     │ • Real-Time Aggregate Metrics    │
└──────────────────────────────────────┘     └──────────────────────────────────┘
```

---

## Component Details

### 1. Frontend Layer (`frontend/src/`)
- **Technology**: React 19, Vite, Tailwind CSS v4, Recharts, Lucide React, Axios.
- **Service Layer (`services/api.js`)**: Centralized HTTP client managing API calls (`healthCheck`, `analyzeText`, `getAnalysis`, `getHistory`, `getDashboardSummary`, `getDashboardTrends`) with unified error formatting.
- **Components**:
  - `Navbar.jsx`: Brand title and live health status badge (`● Analysis Engine Online`).
  - `AnalysisInput.jsx`: Input text area, character count, 1-click demo examples, analyze/clear controls.
  - `AnalysisResult.jsx`: Main result container holding `PrimaryConcernCard`, `SignalCard`, `SentimentCard`, `EmotionList`, `AcademicContext`, and `EvidenceList`.
  - `SummaryCards.jsx` & `Charts`: Real-time aggregate metric cards and Recharts visualizations (Pie chart for severity distribution, horizontal bar chart for signal comparison, multi-line chart for trends).
  - `RecentAnalyses.jsx`: Filterable history list with client-side severity filtering (`ALL`, `HIGH`, `MODERATE`, `LOW`).

### 2. Backend API Layer (`backend/app/`)
- **Technology**: Python 3.10+, FastAPI, Uvicorn, Pydantic v2, SQLAlchemy.
- **Routes (`app/routes/analysis.py`)**:
  - `POST /api/analyze`: Main entry point for feedback analysis and DB persistence.
  - `GET /api/analyze/{analysis_id}`: Retrieves individual historical session by ID.
  - `GET /api/history`: Order-by-newest query for past sessions with text snippets.
  - `GET /api/dashboard/summary`: Aggregate calculations (averages, count, severity counts, top concern).
  - `GET /api/dashboard/trends`: Time-series trend records for charting.

### 3. Context-Aware NLP Engine (`app/services/`)
- **SentimentService (`sentiment_service.py`)**: Warm-loads Hugging Face `distilbert-base-uncased-finetuned-sst-2-english` pipeline.
- **SentenceService (`sentence_service.py`)**: Splits input into sentences and contrast clauses (connected by `but`, `however`, `although`) to evaluate mixed sentiment.
- **Negation Module (`app/utils/negation.py`)**: Resolves negation scope (e.g. *"not stressed"*, *"no difficulty"*) up to 4 words post-negator (`not`, `no`, `never`, `cannot`, `don't`).
- **ContextService (`context_service.py`)**: Evaluates max concept weight across 6 academic dimensions (**Stress**, **Cognitive Overload**, **Frustration**, **Disengagement**, **Workload Difficulty**, **Time Pressure**, **Choice Difficulty**), applies intensity multipliers, and mitigates scores when positive coping contrast clauses exist.
- **ExplainabilityService (`explainability_service.py`)**: Extracts verbatim text evidence with severity impact ratings (`HIGH`, `MEDIUM`, `LOW`) and generates non-clinical student experience insights.

### 4. Database Layer (`app/database.py` & `app/models/`)
- **Engine**: SQLite file-based database (`data/student_analysis.db`).
- **ORM**: SQLAlchemy declarative models.
- **Tables**: `analysis_records` table storing text, ID, timestamps, scores, JSON evidence, and natural language explanations.
