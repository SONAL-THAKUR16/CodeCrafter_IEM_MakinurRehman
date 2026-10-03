# EduSense AI — Final Demo Checklist

**Project**: EduSense AI — Context-Aware Student Academic Experience & Emotion Analyzer  
**Team**: CodeCrafter | IEM Kolkata  
**Team Leader**: Makinur Rahaman  

---

### BEFORE DEMO (Pre-Flight Checks)

- [ ] **Backend Service Running**: Start server via `uvicorn app.main:app --reload --port 8000` inside `backend/`.
- [ ] **Frontend Application Running**: Start Vite via `npm run dev` inside `frontend/`.
- [ ] **Health Status Verified**: Confirm navigation bar shows **"● Analysis Engine Online"** at `http://localhost:3000`.
- [ ] **Database Ready**: SQLite database (`data/student_analysis.db`) contains seeded demo data (`python -m app.seed_demo_data`).
- [ ] **No Secrets Exposed**: Confirm `.env` and `.env.local` files are excluded from Git repository.

---

### DURING DEMO (2–3 Minute Presentation Flow)

#### 1. Problem Introduction (30 seconds)
- [ ] Open application homepage.
- [ ] Explain the limitation of keyword-based classifiers in understanding academic feedback context.
- [ ] Point out the live health indicator in the header bar.

#### 2. Live Feedback Submission (45 seconds)
- [ ] Select or paste sample input:
  > *"I have four assignments due this week and I cannot concentrate. I feel overwhelmed."*
- [ ] Click **"Analyze Feedback"**.
- [ ] Show **Overall Severity Badge** (`HIGH`).
- [ ] Show **Primary Concern** (`WORKLOAD PRESSURE`, score 90%).
- [ ] Show **Signal Scores**: Stress (79%), Cognitive Overload (75%), Workload Difficulty (90%), Time Pressure (75%).

#### 3. Explainability & Evidence (30 seconds)
- [ ] Scroll to **"Why did the system detect this?"**.
- [ ] Point to extracted verbatim phrases with impact badges (`[TIME PRESSURE] "due this week"`, `[COGNITIVE OVERLOAD] "cannot concentrate"`).
- [ ] Show detected **Academic Context Dimensions** (`✓ Workload Pressure`, `✓ Time Pressure`, `✓ Cognitive Load`, `✓ Choice / Priority Difficulty`).

#### 4. Context & Negation Handling (30 seconds)
- [ ] Click demo sample or type:
  > *"I am not stressed about the upcoming exam."*
- [ ] Click **"Analyze Feedback"**.
- [ ] Point out that keyword "stressed" is correctly negated by the NLP engine (`Stress Score: 5%`, `Severity: LOW`).

#### 5. Institutional Analytics & History (30 seconds)
- [ ] Scroll down to **Institutional Dashboard Analytics**.
- [ ] Show **Summary Cards** (Total Analyses, Avg Stress, Avg Overload, Avg Workload, Top Concern).
- [ ] Show **Recharts Visualizations** (Severity Donut Chart, Signal Bar Chart, Trend Line Chart).
- [ ] Demonstrate **History Filtering**: Click `HIGH` severity pill in **Recent Analysis History** card.

---

### AFTER DEMO (Q&A Talking Points)

- [ ] Explain local Hugging Face Transformer & PyTorch pipeline (zero paid API dependencies).
- [ ] Emphasize context-aware linguistic engine (handles negation, scope, intensity, contrast).
- [ ] Clarify system intent: **Non-clinical student experience analytics** (not a clinical/medical diagnosis system).
- [ ] Highlight SQLite persistence and clean REST API design.
