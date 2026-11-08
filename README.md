# SCANNAI — Cybercrime & Scam Awareness Intelligence

> **AI-Assisted Financial Communication Trust-Verification System**  
> *"Don't just detect the deepfake. Verify the trust."*  
> **Team:** ROCKERZ | **Category:** Cybercrime & Digital Safety Prototype  
> **Scope:** Preliminary Inter-College Competition Selection Round

---

## 1. Executive Summary & Problem Statement

Modern cyber fraud in India—most notably **"Digital Arrest" extortion**, **fake customs/narcotics parcel seizures**, and **bogus regulatory clearance demands**—does not rely primarily on photorealistic deepfakes. Instead, scammers exploit **psychological coercion, institutional intimidation, and manufactured legal urgency**.

Victims are pressured into transferring life savings into "verification accounts" under threats of immediate arrest over Skype or WhatsApp video calls. Traditional cybersecurity filters and deepfake detectors fail because:
1. The communication itself is ordinary text, voice, or consumer video conferencing.
2. The core flaw is not audiovisual synthesis; **the flaw is statutory procedural impossibility**.

**SCANNAI** shifts the defensive paradigm from biometric deepfake detection to **Statutory Procedural Verification**. Rather than asking *"Does this video look real?"*, SCANNAI asks:  
***"Does Indian criminal, judicial, or banking procedure ever permit what this communication is demanding?"***

By cross-referencing incoming demands against official procedural safeguards (the *Bharatiya Nagarik Suraksha Sanhita, 2023 (BNSS)*, Reserve Bank of India directives, TRAI advisories, and CBIC regulations), SCANNAI deterministically unmasks fraudulent extortion in milliseconds—operating **100% self-contained with zero reliance on third-party commercial LLM APIs**.

---

## 2. Key Features

- **6 Deterministic Statutory Fallacy Detectors**:
  - `PROC-IND-001` (Digital Arrest): Identifies coercive video confinement and fictitious warrants, citing BNSS 2023 (Sec 35, 63, 64(2), 179, 530) and MHA Parliamentary advisories (PIB PRID=2110809).
  - `PROC-IND-002` (Verification Escrow): Detects bogus asset clearance or verification accounts, citing RBI Caution Notice (PRID 58595) and statutory asset attachment under BNSS Sec 107 / PMLA Sec 17.
  - `PROC-IND-003` (Personal UPI Dues): Flags personal VPA handles (@okhdfcbank, @paytm) demanded for official bail, penalties, or court fees against legitimate Treasury/e-Challan portals.
  - `PROC-IND-004` (Coercive Secrecy): Unmasks demands prohibiting communication with family or legal counsel against Article 22(1) of the Constitution and BNSS Sections 38 and 48.
  - `PROC-IND-005` (Telecom Disconnection Ultimatum): Flags immediate 2-hour disconnection threats, citing TRAI Press Release No. 55/2024 and mandatory DoT verification procedures.
  - `PROC-IND-006` (Customs / Courier Narcotics Extortion): Detects courier parcel drug-seizure threats, citing mandatory Document Identification Numbers (CBIC Circular 19/2019) and NDPS Act Section 67.
- **Three-Tier Deterministic Risk Scoring**:
  - `LOW RISK` (0–34): Standard communications with zero coercion markers.
  - `NEEDS VERIFICATION` (35–69): Isolated urgency or anomalous requests requiring independent verification.
  - `HIGH RISK` (70–100): Direct procedural violations. Any statutory fallacy automatically enforces a **guaranteed 85-point score floor**.
- **Context-Aware False-Positive Shields**:
  - Protects legitimate e-Courts hearing summons (CNR numbers, official portal references).
  - Protects legitimate commercial UPI receipts and genuine telecom billing reminders.
  - Differentiates educational/journalistic reporting on digital arrest scams from live attacks.
- **Binary File-Signature (Magic-Byte) Security Guard**:
  - Inspects true binary headers for PDF (`%PDF-`), PNG (`\x89PNG`), JPEG (`\xFF\xD8\xFF`), and WEBP files.
  - Rejects masqueraded binaries (e.g. `.exe` disguised as `.pdf`) and sanitizes path traversals.
- **Reactive Forensic Presentation Dashboard**:
  - High-contrast, dark-mode cybersecurity dashboard built with React 18, TypeScript, and Tailwind CSS.
  - Visual circular SVG risk score gauge with dynamic color thresholds and statutory contrast cards.
  - Five built-in, 1-click demonstration presets for evaluation panels.

---

## 3. System Architecture

```
┌────────────────────────────────────────────────────────────────────────┐
│                        SCANNAI FRONTEND (React 18)                     │
│  - Single-Page Responsive Dashboard (Tailwind CSS + Lucide Icons)       │
│  - 5 One-Click Scenario Demonstration Presets                          │
│  - Circular SVG Risk Gauge & Statutory Violation Comparison Cards       │
│  - Drag-and-Drop Evidence Ingestion (PDF / Images up to 25 MB)         │
│  - Dynamic Health Beacon polling /api/v1/health                        │
└───────────────────────────────────┬────────────────────────────────────┘
                                    │ HTTP / REST (JSON + Multipart)
                                    ▼
┌────────────────────────────────────────────────────────────────────────┐
│                        SCANNAI BACKEND (FastAPI)                       │
│                                                                        │
│  ┌───────────────────────┐          ┌───────────────────────────────┐  │
│  │    Security Guard     │          │        API Routing V1         │  │
│  │ - Magic-Byte Sniffer  │          │ - GET  /api/v1/health         │  │
│  │ - Path Sanitization   │          │ - POST /api/v1/analyze        │  │
│  │ - 25 MB Payload Limit │          │ - GET  /docs (OpenAPI)        │  │
│  └───────────┬───────────┘          └───────────────┬───────────────┘  │
│              │                                      │                  │
│              ▼                                      ▼                  │
│  ┌──────────────────────────────────────────────────────────────────┐  │
│  │                Deterministic Threat & Rule Engine                │  │
│  │                                                                  │  │
│  │  1. Threat Vector Extractor (Impersonation, Urgency, Secrecy)    │  │
│  │  2. Procedural Fallacy KB (PROC-IND-001 to 006 Statutory Rules)   │  │
│  │  3. False-Positive Context Shields (e-Courts, TSPs, Banking)      │  │
│  │  4. Deduplication & Score Clamping (85 Floor, 100 Ceiling)        │  │
│  └──────────────────────────────────────────────────────────────────┘  │
└────────────────────────────────────────────────────────────────────────┘
```

---

## 4. Technology Stack

| Layer | Technologies & Frameworks |
| :--- | :--- |
| **Backend Framework** | Python 3.12.16, FastAPI 0.115.6, Pydantic V2, Uvicorn 0.34.0 |
| **Environment & Package Mgmt** | Isolated `uv` virtual environment (`backend/.venv`), pinned `requirements.txt` |
| **Testing & Quality** | `pytest 8.3.4`, `pytest-asyncio`, `anyio` (43 regression tests) |
| **Frontend Framework** | React 18.3.1, TypeScript 5.7.3, Vite 6.1.0 |
| **Styling & UI Components** | Tailwind CSS 3.4.17, PostCSS, Autoprefixer, Lucide React 1.16.0 |
| **API Protocol** | RESTful HTTP/JSON + `multipart/form-data` with OpenAPI 3.1 schemas |

---

## 5. Local Setup & Execution Guide

### Prerequisites
- **Node.js**: v18+ (tested on Node v22 / v26)
- **Python**: 3.12 (managed via `uv` or system Python 3.12)

---

### Step 1: Backend Setup & Launch

1. Open a terminal in the project root (`SCANNAI/`):
   ```powershell
   cd backend
   ```
2. Activate the pre-configured virtual environment:
   - **Windows (PowerShell)**:
     ```powershell
     .\.venv\Scripts\Activate.ps1
     ```
   - **Linux / macOS**:
     ```bash
     source .venv/bin/activate
     ```
3. If setting up from scratch without the pre-built environment:
   ```bash
   uv venv .venv --python 3.12
   uv pip install -r requirements.txt
   ```
4. Start the FastAPI backend server:
   ```bash
   python main.py
   ```
   *The server boots at `http://127.0.0.1:8000`.*
   - Health status: `http://127.0.0.1:8000/api/v1/health`
   - Interactive Swagger API docs: `http://127.0.0.1:8000/docs`

---

### Step 2: Frontend Setup & Launch

1. Open a second terminal in `SCANNAI/frontend`:
   ```bash
   cd frontend
   npm install
   ```
2. Start the Vite development server:
   ```bash
   npm run dev
   ```
3. Open your browser and navigate to:
   ```
   http://127.0.0.1:5173
   ```
   *The dashboard automatically connects to the backend and displays `SYSTEM ONLINE (DETERMINISTIC)`.*

---

## 6. How to Run the 5 Demonstration Scenarios

On the dashboard, click any of the **Quick Demonstration Presets** located directly above the analysis workspace:

| Preset | Scenario Description | Tested Risk Score | Classification | Expected Violation |
| :---: | :--- | :---: | :---: | :--- |
| **1** | **Digital Arrest Scam**<br>*Fake police, Skype camera order, arrest threat* | **98 / 100** | **HIGH RISK** | `PROC-IND-001` (Digital Arrest / BNSS Sec 530) |
| **2** | **Legitimate e-Courts Notice**<br>*Authentic summons with CNR number* | **10 / 100** | **LOW RISK** | None (False-positive shield active) |
| **3** | **Fraudulent UPI Clearance Demand**<br>*Bogus RBI asset verification deposit* | **90 / 100** | **HIGH RISK** | `PROC-IND-002` (Escrow / RBI PRID 58595) |
| **4** | **Legitimate Commercial Order**<br>*Retail grocery invoice with optional UPI* | **10 / 100** | **LOW RISK** | None (Ordinary retail context) |
| **5** | **Customs / NCB Parcel Extortion**<br>*FedEx courier drug seizure penalty demand* | **73 / 100** | **HIGH RISK** | `PROC-IND-006` (CBIC DIN Circular 19/2019) |

---

## 7. Testing & Verification

### Backend Regression Tests (43 Tests)
Run the automated test suite from the root directory:
```powershell
& "backend\.venv\Scripts\python.exe" -m pytest backend/tests -v
```
**Outcome:** `43 passed in ~0.5s` (100% pass rate, 0 failures, 0 warnings).

### Frontend Type Safety & Production Build
```powershell
cd frontend
npx tsc --noEmit     # TypeScript type-check
npm run build        # Production minification & bundling
```
**Outcome:** `0 errors`, production assets bundled into `frontend/dist/` in ~3.5s.

---

## 8. Privacy, Data Handling & Deployment Models

### Truthful Privacy Disclosure
SCANNAI does not transmit evidence to external AI vendors (such as OpenAI, Anthropic, or commercial cloud LLMs). All rule evaluation occurs strictly in-engine.

However, data transmission boundaries depend on the deployment topology:

| Deployment Model | Network Path | Data Storage / Retention | Evaluator Recommendation |
| :--- | :--- | :--- | :---: |
| **1. Local Deployment (Current)** | `localhost` / `127.0.0.1` (Zero external network egress) | In-memory only; non-persisted | **RECOMMENDED FOR HACKATHON DEMO** |
| **2. Self-Hosted Docker / On-Prem** | Private LAN / Intranet (HTTPS) | Contained within organization's server | Suitable for campus/enterprise networks |
| **3. Public Cloud (PaaS)** | Client browser to Public Cloud Server (HTTPS) | Processed on cloud VPS; zero 3rd-party LLM calls | Suitable for remote web screening |

> [!NOTE]
> For the preliminary competition round, **Local Deployment (Option 1)** is strongly recommended. It eliminates internet flakiness, cloud latency, and third-party hosting dependencies during live judging.

---

## 9. Current Limitations & Future Scope

### What SCANNAI Does NOT Do (Phase 3.2 Scope)
- **No OCR / Vision Parsing**: In Phase 3.2, document uploads are validated for file-signature (magic bytes) and MIME integrity. Text extraction from scanned PDFs/images is scheduled for Phase 4.
- **No Machine Learning / Real-time Govt Database Lookups**: SCANNAI does not query live police databases or active banking ledgers. It evaluates procedural adherence deterministically against codified law.
- **Educational Prototype**: Results are indicative and designed for decision support; they do not constitute legal advice or formal evidentiary certification.

### Future Roadmap (Phase 4 & Beyond)
- Multi-engine Optical Character Recognition (Tesseract / PaddleOCR) for visual court summonses.
- Multilingual speech-to-text for real-time scam call analysis (Hindi, Tamil, Telugu, Marathi).
- Native WhatsApp Web and browser extension integration for real-time message flagging.

---

## 10. Legal & Statutory Citations

1. **Bharatiya Nagarik Suraksha Sanhita, 2023 (BNSS)**: Sections 35, 38, 48, 63, 64(2), 107, 179, and 530.
2. **Ministry of Home Affairs (MHA) & I4C**: Lok Sabha Unstarred Question No. 1290 (12 March 2025); PIB PRID=2110809.
3. **Reserve Bank of India (RBI)**: Public Caution Notice on Fictitious Offers & Clearance Accounts (PRID 58595).
4. **Telecom Regulatory Authority of India (TRAI)**: Press Release No. 55/2024 on mobile disconnection scams.
5. **Central Board of Indirect Taxes and Customs (CBIC)**: Circular No. 19/2019-Customs (Mandatory DIN Generation).
6. **Constitution of India**: Article 22(1) (Right to consult and be defended by a legal practitioner).

---

## 11. Project Credits

- **Product**: SCANNAI (Cybercrime & Scam Awareness Intelligence)
- **Team**: ROCKERZ
- **Version**: 0.1.0-DEMO (Stage 3 Release Candidate)
- **License**: MIT Open Source Educational License
