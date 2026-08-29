# CogniPath-BuildSprint26
# CogniPath 🧠
**[🎥 Watch the 2-Minute Demo Video Here](https://link-to-your-youtube-or-drive-video.com)**

**AI-Driven Multimodal Triage Engine for Cognitive Health**

CogniPath bridges the critical gap between patient self-reporting and clinical decision-making. By analyzing multimodal inputs—like cognitive assessments and blood biomarkers—CogniPath accelerates early intervention for Alzheimer's and progressive cognitive decline.

## Key Features
* **Patient Intake Portal:** A secure, intuitive interface for patients or caregivers to submit demographic data, cognitive scores (0-30), and biomarker levels (e.g., p-tau181).
* **Dynamic Patient Tracking:** Automatically generates unique, secure Patient IDs (e.g., `PT_LIVE_XXXX`) upon intake initiation to ensure anonymous triage tracking.
* **Clinician Triage Dashboard:** A specialized provider portal that ingests patient data and instantly applies risk stratification, categorizing cases into High, Moderate, and Low urgency.
* **Seamless SPA Architecture:** Built with a "Liquid Glass" UI, featuring instant state transitions between the landing page, intake modals, and the clinical dashboard without page reloads.

## Tech Stack
* **Frontend:** HTML5, Vanilla JavaScript (ES6+), CSS3 / Tailwind CSS
* **State Management:** Client-side DOM manipulation and static data locking for stable, deterministic clinical demonstrations.

## Getting Started
To run this project locally and test the triage flow:

1. Clone this repository to your local machine.
2. Open the `index.html` file directly in any modern web browser.
3. Click **Access Patient Intake**, generate a dynamic ID, fill out the mock clinical data, and submit.
4. From the landing page, enter a mock Doctor ID under the **Clinician Portal** and log in to view the stabilized risk stratification dashboard.

## Interface Showcase

### Landing Page & Patient Intake
![CogniPath Landing Page](images/Landing-page.png)

![Patient Intake Modal](images/patient-modal.png)

### Clinician Triage Dashboard
![Clinician Dashboard](images/Dashboard.png)

---
*Built for fast, reliable healthcare triage.*
