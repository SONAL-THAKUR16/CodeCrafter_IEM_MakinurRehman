# EduSense AI — Judge Talking Points & Pitch Summary

**Team**: CodeCrafter  
**Institution**: Institute of Engineering and Management (IEM)  
**Team Leader**: Makinur Rahaman  

---

### 1. Problem Statement
Traditional feedback analysis in educational institutions relies on static survey forms or keyword-matching algorithms. These keyword systems fail to understand context, negation, intensity, or sentence structure:
- They treat *"I am stressed"* and *"I am not stressed"* identically because both contain the word *"stressed"*.
- They fail to distinguish between *"I am slightly worried"* and *"I am extremely overwhelmed"*.
- They cannot parse mixed sentiments such as *"I love this course, but the workload is becoming impossible to manage"*.

---

### 2. Our Approach
**EduSense AI** provides a context-aware student academic experience analysis engine that combines:
1. **Transformer Sentiment Classification**: Warm-loaded local Hugging Face `distilbert-base-uncased-finetuned-sst-2-english` model.
2. **Clause-Level Contrast Parsing**: Evaluates sentences joined by conjunctions (`but`, `however`, `although`) to identify mixed academic sentiment.
3. **Negation Scope Engine**: Scans text windows around negators (`not`, `no`, `never`, `cannot`, `don't`) to reverse or neutralize distress signals.
4. **Academic Signal Extractor**: Evaluates 6 core dimensions (**Stress**, **Cognitive Overload**, **Frustration**, **Disengagement**, **Workload Difficulty**, **Time Pressure**, **Choice Difficulty**).

---

### 3. Key Differentiation
- **Context vs Keyword Matching**: Evaluates contextual relationships rather than counting negative word occurrences.
- **Explainable Evidence Extraction**: Answers *"Why did the system detect this?"* by highlighting verbatim input text snippets with severity impact ratings (`HIGH IMPACT`, `MEDIUM IMPACT`, `LOW IMPACT`).
- **Non-Clinical Student Experience Focus**: Evaluates workload distress, cognitive fatigue, and academic engagement without making medical or psychological diagnoses.
- **Real-Time Institutional Analytics**: Persists analysis transactions in SQLite and updates aggregate metrics, severity distributions, signal averages, and time-series trends dynamically.

---

### 4. Technical Honesty & System Limitations
- **Local & Open-Source**: Runs 100% locally on open-source Hugging Face Transformers & PyTorch without relying on paid third-party APIs.
- **Probabilistic Predictions**: Transformer predictions and linguistic rules are probabilistic representations of linguistic patterns in feedback.
- **Scope**: Designed as an 8-hour hackathon MVP prototype for student feedback analytics; future extensions would integrate multi-modal learning analytics.
