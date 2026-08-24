# Vendor Onboarding Workflow Automation

## Problem Statement

Vendor onboarding often involves manual review of company details, bank account information, tax identification, and supporting documents.

This creates several operational challenges:

- Manual validation takes time
- Missing information creates back-and-forth communication
- Inconsistent bank details may create financial or compliance risk
- Review decisions may not be standardized
- Teams have limited visibility into workflow outcomes

This project demonstrates a simplified automated workflow that processes vendor submissions, validates key information, generates a decision, and communicates the required next action.

---

# Proposed Solution

The **Vendor Onboarding Workflow Automation** processes a vendor submission through a structured decision flow.

## Workflow

```text
Vendor Submission
        ↓
Required Information Validation
        ↓
Country-Aware Tax ID Validation
        ↓
Bank Account Holder Cross-Check
        ↓
Required Document Validation
        ↓
Decision Generation
        ↓
Vendor Communication / Next Action
        ↓
APPROVED / PENDING / REJECTED
```

The goal is to standardize the initial review process and make onboarding decisions more transparent and consistent.

---

# How It Works

A user submits:

- Company name
- Bank account holder name
- Country
- Tax ID
- Supporting documents

The workflow then performs multiple validation checks.

### 1. Required Information Validation

Checks whether all required vendor information has been provided.

### 2. Country-Aware Tax ID Validation

Validates the Tax ID format based on the selected country.

Currently supported:

- India
- United States
- United Kingdom

### 3. Bank Detail Cross-Check

Compares the company name with the bank account holder name.

A significant inconsistency is treated as a higher-risk issue and can result in rejection.

### 4. Document Validation

Checks whether the required documents are provided:

- Tax Registration
- Bank Proof

### 5. Decision Generation

Based on the validation results, the workflow generates one of three outcomes:

| Decision | Meaning |
|---|---|
| APPROVED | All required validation checks passed |
| PENDING | Information or documents require correction |
| REJECTED | A significant inconsistency was detected |

### 6. Next Action for Vendor

The system communicates what should happen next.

For **Pending** submissions, the vendor is asked to correct issues or provide missing documents.

For **Rejected** submissions, the vendor is asked to correct inconsistent banking information or provide supporting documentation for manual investigation.

---

# Decision Logic

```text
Vendor Submission
        ↓
Are required fields valid?
        ↓
No → PENDING

Yes
        ↓
Is Tax ID valid?
        ↓
No → PENDING

Yes
        ↓
Do company and bank details match?
        ↓
No → REJECTED

Yes
        ↓
Are required documents available?
        ↓
No → PENDING

Yes → APPROVED
```

---

# Edge Cases Tested

## Happy Path — Approved

**Scenario:**

- Valid company information
- Matching bank account holder
- Valid Tax ID
- Tax Registration provided
- Bank Proof provided

**Result:** `APPROVED`

---

## Edge Case 1 — Missing Document

**Scenario:** Vendor information is valid, but Bank Proof is missing.

**Result:** `PENDING`

The workflow identifies the missing document and communicates what needs to be submitted.

---

## Edge Case 2 — Invalid Tax ID

**Scenario:** Vendor submits an incorrectly formatted Tax ID.

**Result:** `PENDING`

The vendor must correct the Tax ID before approval.

---

## Edge Case 3 — Bank Detail Mismatch

**Scenario:** Company name and bank account holder are significantly inconsistent.

**Result:** `REJECTED`

The workflow flags the submission for manual investigation.

---

# Live Workflow Execution

Each submission moves through visible workflow stages:

```text
✓ Submission Received
✓ Required Information Validation
✓ Tax ID Validation
✓ Bank Detail Cross-Check
✓ Document Validation
✓ Decision Generated
```

Stages are displayed as:

- Passed
- Attention Required
- Failed

---

# Dashboard and Run History

The application includes a dashboard showing:

- Total workflow runs
- Approved submissions
- Pending submissions
- Rejected submissions
- Recent workflow history
- Country
- Decision status
- Submission timestamp

This provides basic operational visibility and an audit trail of workflow outcomes.

---

# Before vs After

## Before Automation

```text
Vendor submits information
        ↓
Operations team manually reviews data
        ↓
Checks documents manually
        ↓
Checks tax information
        ↓
Compares banking details
        ↓
Makes a decision
        ↓
Contacts vendor for corrections
```

### Problems

- Repetitive manual work
- Inconsistent review processes
- Delayed decisions
- Repeated follow-ups
- Limited visibility into workflow status

## After Automation

```text
Vendor submits information
        ↓
Automated validation
        ↓
Automated cross-checks
        ↓
Decision generation
        ↓
Clear explanation of issues
        ↓
Next action communicated
        ↓
Dashboard tracking
```

---

# Business Impact

This MVP demonstrates how workflow automation could improve vendor onboarding operations.

### Potential Benefits

- Reduced manual review effort
- Faster identification of incomplete submissions
- More consistent validation
- Earlier detection of banking inconsistencies
- Clearer communication with vendors
- Better visibility into workflow outcomes

## KPI Framework

| KPI | Purpose |
|---|---|
| Total Vendor Submissions | Measures workflow volume |
| Approval Rate | Measures successful onboarding |
| Pending Rate | Identifies incomplete submissions |
| Rejection Rate | Highlights risk or inconsistency patterns |
| Average Processing Time | Measures workflow efficiency |
| Manual Reviews Required | Measures automation effectiveness |

---

# Tech Stack

- Python
- FastAPI
- SQLite
- HTML/CSS
- Rule-Based Validation
- Render

The MVP intentionally uses a minimal architecture to focus on workflow design and business logic rather than unnecessary infrastructure.

---

# Architecture

```text
User
  │
  ▼
FastAPI Web Application
  │
  ▼
Vendor Validation Workflow
  │
  ├── Required Field Validation
  ├── Tax ID Validation
  ├── Bank Detail Cross-Check
  └── Document Validation
  │
  ▼
Decision Engine
  │
  ├── APPROVED
  ├── PENDING
  └── REJECTED
  │
  ▼
Next Action Communication
  │
  ▼
SQLite Run History
  │
  ▼
Workflow Dashboard
```

---

# Running Locally

Clone the repository:

```bash
git clone https://github.com/vidhikajain10/zamp-ai-solutions-case-study.git
cd zamp-ai-solutions-case-study
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Run the application:

```bash
uvicorn app:app --reload
```

Open:

```text
http://127.0.0.1:8000
```

Dashboard:

```text
http://127.0.0.1:8000/dashboard
```

---

# Project Goal

This project was designed as a **small but functional workflow MVP**.

The focus is not on unnecessary enterprise infrastructure. Instead, the project demonstrates:

- Business process understanding
- Workflow analysis
- Validation and decision logic
- Automation opportunities
- Exception handling
- Clear next actions
- Operational visibility
- End-to-end workflow ownership
