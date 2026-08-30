# CogniPath-BuildSprint26

# CogniPath 🧠
**[🎥 Watch the 2-Minute Demo Video Here](https://drive.google.com/file/d/1FEihsLXOR0s_0tLWiyZHLGLgJ-80eOqT/view?usp=sharing)** | **[🌍 Live Deployed Frontend](https://sohaam007.github.io/CogniPath-BuildSprint26/frontend/index.html)**

**AI-Driven Multimodal Triage Engine for Cognitive Health & Neurodegenerative Risk Stratification**

CogniPath bridges the critical gap between patient self-reporting and clinical decision-making. By analyzing multimodal inputs—like cognitive assessments and blood biomarkers—CogniPath accelerates early intervention for Alzheimer's and progressive cognitive decline.

---

## 📖 The Problem Statement: A Story of Delayed Cognitive Intervention

Imagine Eleanor, a 68-year-old retired teacher experiencing subtle memory lapses. She misplaces her keys daily, struggles to follow complex conversations, and feels increasingly disoriented during routine errands. Her family suspects early-stage Alzheimer's disease and requests a specialist evaluation.

When her primary care physician submits a referral to a regional neurology clinic, Eleanor enters a broken triage pipeline:

1. **The Waitlist Bottleneck:** Specialist clinics face overwhelming referral volumes, resulting in wait times of **6 to 9 months** for initial cognitive consultations.
2. **Subjective & Fragmented Data:** Referrals rely heavily on paper self-reporting or single-dimensional cognitive tests (like basic MMSE scores), omitting critical biological indicators.
3. **Delayed Diagnostic Windows:** Disease-modifying Alzheimer's therapies are exponentially more effective during preclinical or Mild Cognitive Impairment (MCI) stages. By the time Eleanor finally sees a neurologist, valuable therapeutic intervention windows have closed.

### The CogniPath Solution
CogniPath eliminates the specialist bottleneck by providing an instant, **multimodal AI triage layer**. By fusing patient self-reported cognitive scores (0–30) with objective blood biomarkers (such as p-tau181 and Amyloid-Beta ratios), CogniPath risk-stratifies incoming cases into **High**, **Moderate**, and **Low** urgency cohorts within milliseconds—ensuring critical patients like Eleanor are prioritized immediately.

---

## Key Features
* **Patient Intake Portal:** A secure, intuitive interface for patients or caregivers to submit demographic data, cognitive scores (0-30), and biomarker levels (e.g., p-tau181).
* **Dynamic Patient Tracking:** Automatically generates unique, secure Patient IDs (e.g., `PT_LIVE_XXXX`) upon intake initiation to ensure anonymous triage tracking.
* **Biomarker Data Integration Pipeline:** Connects incoming patient payloads with objective clinical biomarker data, pairing clinical assessments with biological ground truths.
* **Clinician Triage Dashboard:** A specialized provider portal that ingests patient data and instantly applies risk stratification, categorizing cases into High, Moderate, and Low urgency, with real-time queues, biomarker vectors, and cohort statistics.
* **Seamless SPA Architecture:** Built with a "Liquid Glass" UI, featuring instant state transitions between the landing page, intake modals, and the clinical dashboard without page reloads.
* **Microsecond Profiling & Synthetic Cohort Benchmark:** Built-in benchmarking pipeline leveraging Python's `time.perf_counter` to profile triage latency against a synthetic 500+ patient cohort, ensuring sub-millisecond execution at scale.

---

## 📐 System Architecture

CogniPath utilizes a decoupled client-server architecture designed for high availability and zero-latency UI transitions:

```text
  +-------------------------------------------------------------------+
  |                   LIQUID GLASS FRONTEND (SPA)                     |
  |  - HTML5, Tailwind CSS, Vanilla JavaScript (ES6+)                 |
  |  - Patient Intake Portal (Dynamic PT_LIVE_XXXX tracking)          |
  |  - Clinician Triage Dashboard (Risk Stratification Cockpit)       |
  |  - Static Data Locking for Deterministic Clinical Demos           |
  +---------------------------------+---------------------------------+
                                    |
                        REST API Payloads / JSON
                                    |
                                    v
  +-------------------------------------------------------------------+
  |                  FASTAPI BACKEND ENGINE (PORT 8000)               |
  |  - Asynchronous Route Controller & CORS Middleware (main.py)      |
  |  - Pydantic Schema Validation for Clinical Payloads               |
  |  - Multimodal Risk Stratification & Scoring Algorithm             |
  |  - Microsecond Latency Profiler & Synthetic Cohort Generator      |
  +-------------------------------------------------------------------+
```

## 🛠️ Tech Stack
* **Frontend:** HTML5, Vanilla JavaScript (ES6+), CSS3 / Tailwind CSS (Liquid Glass UI design)
* **Backend Engine:** Python 3.11, FastAPI, Uvicorn, Pydantic
* **Benchmarking & Data:** JSON Synthetic Patient Cohort, Python unittest suite, microsecond `time.perf_counter` profiler
* **State Management:** Client-side DOM manipulation and static data locking for stable, deterministic clinical demonstrations

---

## 🔌 API Credentials & Safety (Zero-Leak Security)
To ensure absolute security when pushing codebase assets to GitHub:
* **No hardcoded secrets:** All API endpoints, gateway routes, and backend variables read from local configuration or environment variables.
* **Deterministic Fallback:** If offline or detached from backend servers, the frontend UI gracefully falls back to deterministic static data locking to guarantee uninterrupted demonstration during judging.

---

## Getting Started

### Testing the Frontend UI Locally
1. Clone this repository to your local machine:
```bash
   git clone https://github.com/Sohaam007/CogniPath-BuildSprint26.git
   cd CogniPath-BuildSprint26
```
2. Open the `frontend/index.html` file directly in any modern web browser.
3. Click **Access Patient Intake**, generate a dynamic ID (e.g., `PT_LIVE_9021`), fill out the mock clinical data (e.g., Age: 68, MMSE Score: 18/30, p-tau181 level: 2.4 pg/mL), and submit.
4. From the landing page, select a medical center from the dropdown, enter a mock Doctor ID (e.g., `DOC_77`) under the **Clinician Portal**, and log in to view the stabilized risk stratification dashboard.

### ⚙️ Running the AI Triage Backend
To execute the FastAPI server and explore interactive API documentation:
1. Ensure Python 3.11+ is installed.
2. Install dependencies:
```bash
   pip install -r requirements.txt
```
3. Boot up the server:
```bash
   uvicorn api.main:app --reload
```
   (Adjust `api.main:app` if your entry point script is located in a different directory.)
4. Access interactive Swagger API documentation at: `http://localhost:8000/docs`

---

## 🌌 Interactive Walkthrough Checklist for Judges
Follow this sequence to test the complete end-to-end triage flow:
1. **Access the Live Portal:** Open the [Live Deployed Frontend](https://sohaam007.github.io/CogniPath-BuildSprint26/frontend/index.html) in your browser.
2. **Initiate Patient Intake:** Click **Access Patient Intake**, then click **Generate ID** to produce a secure patient hash (e.g., `PT_LIVE_9021`).
3. **Submit Clinical Symptoms:** Enter mock patient data (e.g., Age: 68, MMSE Score: 18/30, p-tau181 level: 2.4 pg/mL) and click **Submit Assessment**.
4. **Log in to Clinician Portal:** Return to the main portal, select a medical center from the dropdown, enter a mock Doctor ID (e.g., `DOC_77`), and click **Login as Clinician**.
5. **Inspect Stratified Triage:** View the Clinician Dashboard to see the real-time risk stratification matrix, dynamic cohort statistics, and prioritized patient queues.

---

## 🖼️ Interface Showcase

### Landing Page & Patient Intake
![CogniPath Landing Page](images/Landing-page.png)

![Patient Intake Modal](images/patient-modal.png)

### Clinician Triage Dashboard
![Clinician Dashboard](images/Dashboard.png)

---
*Built by Team Code Blue for fast, reliable healthcare triage during BuildSprint 2026.*
