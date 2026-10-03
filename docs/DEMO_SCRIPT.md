# EduSense AI — 2-Minute Judge Demonstration Script

**Project**: EduSense AI — Context-Aware Student Experience & Emotion Analyzer  
**Team**: CodeCrafter  
**College**: Institute of Engineering and Management (IEM)  
**Team Leader**: Makinur Rahaman  

---

### Demonstration Overview

This script guides a 2-to-3 minute live demonstration of **EduSense AI** for hackathon judges, highlighting our **context-aware transformer NLP engine**, **interpretable phrase evidence extraction**, and **real-time aggregate institutional analytics**.

---

### Step 1: Launch & Problem Statement (30 Seconds)

1. **Action**: Open the application at `http://localhost:5173` (or active frontend port).
2. **Judge Pitch**:
   > *"Welcome to EduSense AI. Traditional student feedback systems rely on rigid keyword searches that fail to understand context, negation, or sentence structure—often misinterpreting statements or ignoring workload distress until it's too late. EduSense AI uses local open-source transformer models and context-aware linguistic algorithms to identify real student experience signals—like stress, cognitive overload, time pressure, and disengagement—without medical diagnoses or clinical labeling."*

3. **Point Out**: Notice the **"● Analysis Engine Online"** live health badge in the top navigation bar, confirming active connection to our FastAPI backend.

---

### Step 2: Live Feedback Analysis (45 Seconds)

1. **Action**: Click the sample button or paste the following student feedback text into the input box:
   > *"I have four assignments due this week and I cannot concentrate. I feel overwhelmed."*

2. **Action**: Click the **"Analyze Feedback"** button.
3. **Point Out Results**:
   - **Overall Experience Rating**: Highlight the `HIGH` severity badge.
   - **Primary Concern**: Point to `WORKLOAD PRESSURE` (Signal Score: 90%).
   - **Student Insight**: Read the generated neutral summary: *"The response suggests elevated workload pressure and potential difficulty balancing academic tasks."*
   - **Academic Signals**: Show normalized progress meters for **Stress** (79%), **Cognitive Overload** (75%), **Workload Difficulty** (90%), and **Time Pressure** (75%) alongside neutral interpretations (*"Strong signal detected"*).

---

### Step 3: Explainability — "Why Did the System Detect This?" (30 Seconds)

1. **Action**: Scroll to the **"Why did the system detect this?"** section.
2. **Point Out**:
   > *"Unlike black-box AI systems, EduSense AI provides complete explainability. Notice how our engine extracted exact text snippets from the student's input with severity impact tags:"*
   - `[TIME PRESSURE]` *"due this week"* — High Impact
   - `[WORKLOAD PRESSURE]` *"four assignments due"* — High Impact
   - `[COGNITIVE OVERLOAD]` *"cannot concentrate"* — High Impact
   - `[STRESS]` *"overwhelmed"* — High Impact
3. **Point Out**: Show the **Academic Context Dimensions** grid (`✓ Workload Pressure`, `✓ Time Pressure`, `✓ Cognitive Load`, `✓ Choice / Priority Difficulty`), demonstrating structural context detection beyond generic sentiment.

---

### Step 4: Context & Negation Handling Demonstration (30 Seconds)

1. **Action**: Click the demo example or type:
   > *"I am not stressed about the upcoming exam."*

2. **Action**: Click **"Analyze Feedback"**.
3. **Judge Pitch**:
   > *"Here is why context matters. A keyword-based classifier sees the word 'stressed' and flags this as negative or high distress. Watch what EduSense AI does:"*
4. **Point Out Results**:
   - **Overall Severity**: `LOW`
   - **Dominant Sentiment**: `POSITIVE`
   - **Extracted Evidence**: `[STRESS] "'not stressed' (negation recognized)"`
   - **Stress Signal**: 5% (Negation scope correctly identified and negated).

---

### Step 5: Institutional Analytics & History (30 Seconds)

1. **Action**: Scroll down to the **Institutional Dashboard Analytics** section.
2. **Point Out**:
   - **Summary Cards**: Real-time aggregate statistics for **Total Analyses**, **Average Stress**, **Average Cognitive Overload**, **Average Workload Difficulty**, and **Most Common Concern**.
   - **Recharts Visualizations**:
     - **Severity Distribution**: Donut pie chart displaying breakdown across Low, Moderate, and High records.
     - **Academic Signal Comparison**: Horizontal bar chart comparing signal averages.
     - **Distress Trends**: Multi-line graph showing stress, workload, and overload trajectories over time.
3. **History Filter**: Click the **`HIGH`** severity filter pill in the **Recent Analysis History** card to show instant client-side filtering. Click any session row to reload its full analysis view.

---

### Summary Checklist for Judges

| Feature | Demonstrated | Key Takeaway |
| :--- | :---: | :--- |
| **Context-Aware NLP** | ✅ | Understands negation, intensity, contrast, and multi-clause sentences. |
| **Explainability** | ✅ | Extracted verbatim phrases with severity impact tags. |
| **Non-Clinical Design** | ✅ | Focuses on linguistic academic experience signals without medical diagnosis. |
| **Real-Time Analytics** | ✅ | SQLite persistence with real-time Recharts visualizations. |
| **Local & Open-Source** | ✅ | Zero paid third-party APIs; runs locally on Hugging Face & PyTorch. |
