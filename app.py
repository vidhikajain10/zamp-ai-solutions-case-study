from fastapi import FastAPI, Form
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
import time
import re

app = FastAPI(title="Vendor Onboarding Workflow")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

runs = []


def validate_vendor(company, bank_name, country, tax_id, documents):
    issues = []
    stages = []

    # Stage 1
    stages.append({
        "name": "Submission Received",
        "status": "completed"
    })

    # Stage 2 - Required fields
    time.sleep(0.3)

    if not all([company, bank_name, country, tax_id]):
        issues.append("Required information is missing.")

    stages.append({
        "name": "Required Field Validation",
        "status": "completed" if not issues else "warning"
    })

    # Stage 3 - Tax ID validation
    time.sleep(0.3)

    tax_valid = bool(re.match(r"^[A-Za-z0-9]{6,15}$", tax_id))

    if not tax_valid:
        issues.append("Tax ID format appears invalid.")

    stages.append({
        "name": "Tax ID Validation",
        "status": "completed" if tax_valid else "warning"
    })

    # Stage 4 - Bank/company consistency
    time.sleep(0.3)

    company_match = (
        company.lower() in bank_name.lower()
        or bank_name.lower() in company.lower()
    )

    if not company_match:
        issues.append(
            "Company name and bank account holder appear inconsistent."
        )

    stages.append({
        "name": "Bank Detail Cross-Check",
        "status": "completed" if company_match else "warning"
    })

    # Stage 5 - Document validation
    time.sleep(0.3)

    required_docs = ["Tax Registration", "Bank Proof"]

    missing_docs = [
        doc for doc in required_docs
        if doc not in documents
    ]

    if missing_docs:
        issues.append(
            "Missing documents: " + ", ".join(missing_docs)
        )

    stages.append({
        "name": "Document Check",
        "status": "completed" if not missing_docs else "warning"
    })

    # Final decision
    time.sleep(0.3)

    if not company_match:
        decision = "REJECTED"
        reason = (
            "The submission contains a significant inconsistency "
            "between the company and bank account holder."
        )

    elif missing_docs or not tax_valid or not all([company, bank_name, country, tax_id]):
        decision = "PENDING"
        reason = (
            "Additional information or correction is required "
            "before approval."
        )

    else:
        decision = "APPROVED"
        reason = (
            "All required information and documents passed "
            "the validation checks."
        )

    stages.append({
        "name": "Decision Generated",
        "status": "completed"
    })

    return decision, reason, issues, stages


@app.get("/", response_class=HTMLResponse)
def home():

    return """
<!DOCTYPE html>
<html>
<head>
    <title>Vendor Onboarding Workflow</title>

    <style>

        body {
            font-family: Arial, sans-serif;
            background: #f5f7fb;
            margin: 0;
            padding: 40px;
            color: #1e293b;
        }

        .container {
            max-width: 900px;
            margin: auto;
        }

        h1 {
            margin-bottom: 5px;
        }

        .subtitle {
            color: #64748b;
            margin-bottom: 30px;
        }

        .card {
            background: white;
            padding: 25px;
            border-radius: 12px;
            margin-bottom: 25px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.08);
        }

        input, select {
            width: 100%;
            padding: 12px;
            margin-top: 8px;
            margin-bottom: 18px;
            border: 1px solid #d1d5db;
            border-radius: 8px;
            box-sizing: border-box;
        }

        button {
            background: #2563eb;
            color: white;
            border: none;
            padding: 12px 20px;
            border-radius: 8px;
            cursor: pointer;
            font-size: 16px;
        }

        button:hover {
            background: #1d4ed8;
        }

        .stage {
            padding: 12px;
            margin: 8px 0;
            border-left: 4px solid #2563eb;
            background: #f8fafc;
        }

        .approved {
            color: #15803d;
            font-weight: bold;
        }

        .pending {
            color: #d97706;
            font-weight: bold;
        }

        .rejected {
            color: #dc2626;
            font-weight: bold;
        }

        .issue {
            background: #fff7ed;
            padding: 10px;
            margin-top: 8px;
            border-radius: 6px;
        }

    </style>

</head>

<body>

<div class="container">

<h1>Vendor Onboarding Workflow</h1>

<p class="subtitle">
Automated validation and decision workflow for vendor submissions
</p>

<div class="card">

<form action="/process" method="post">

<label>Company Name</label>
<input name="company" required>

<label>Bank Account Holder Name</label>
<input name="bank_name" required>

<label>Country</label>

<select name="country">
<option>India</option>
<option>United States</option>
<option>United Kingdom</option>
</select>

<label>Tax ID</label>
<input name="tax_id" required>

<label>Documents</label>

<select name="documents" multiple size="3">

<option value="Tax Registration">
Tax Registration
</option>

<option value="Bank Proof">
Bank Proof
</option>

<option value="Compliance Certificate">
Compliance Certificate
</option>

</select>

<button type="submit">
Run Vendor Workflow
</button>

</form>

</div>

<div class="card">

<h2>Workflow</h2>

<p>
Submission → Validation → Cross-check → Decision
</p>

</div>

<div class="card">

<h2>Run History</h2>

""" + "".join([
    f"""
    <div class="stage">
        <strong>{run["company"]}</strong>
        — {run["decision"]}
    </div>
    """
    for run in runs[-5:]
]) + """

</div>

</div>

</body>
</html>
"""


@app.post("/process", response_class=HTMLResponse)
def process(
    company: str = Form(...),
    bank_name: str = Form(...),
    country: str = Form(...),
    tax_id: str = Form(...),
    documents: list[str] = Form([])
):

    decision, reason, issues, stages = validate_vendor(
        company,
        bank_name,
        country,
        tax_id,
        documents
    )

    runs.append({
        "company": company,
        "decision": decision
    })

    decision_class = decision.lower()

    stages_html = "".join([
        f"""
        <div class="stage">
        ✓ {stage["name"]}
        </div>
        """
        for stage in stages
    ])

    issues_html = ""

    if issues:

        issues_html = "<h3>Issues Found</h3>"

        for issue in issues:

            issues_html += f"""
            <div class="issue">
            {issue}
            </div>
            """

    return f"""
<!DOCTYPE html>

<html>

<head>

<title>Workflow Result</title>

<style>

body {{
font-family: Arial;
background: #f5f7fb;
padding: 40px;
color: #1e293b;
}}

.container {{
max-width: 900px;
margin: auto;
}}

.card {{
background: white;
padding: 25px;
border-radius: 12px;
margin-bottom: 20px;
box-shadow: 0 4px 12px rgba(0,0,0,0.08);
}}

.stage {{
padding: 12px;
margin: 8px 0;
background: #f8fafc;
border-left: 4px solid #2563eb;
}}

.approved {{
color: #15803d;
font-size: 28px;
font-weight: bold;
}}

.pending {{
color: #d97706;
font-size: 28px;
font-weight: bold;
}}

.rejected {{
color: #dc2626;
font-size: 28px;
font-weight: bold;
}}

.issue {{
background: #fff7ed;
padding: 10px;
margin: 8px 0;
border-radius: 6px;
}}

button {{
background: #2563eb;
color: white;
border: none;
padding: 12px 20px;
border-radius: 8px;
cursor: pointer;
}}

</style>

</head>

<body>

<div class="container">

<div class="card">

<h1>Vendor Onboarding Result</h1>

<div class="{decision_class}">
{decision}
</div>

<p>{reason}</p>

</div>

<div class="card">

<h2>Live Workflow Execution</h2>

{stages_html}

</div>

<div class="card">

{issues_html}

</div>

<a href="/">
<button>
Run Another Submission
</button>
</a>

</div>

</body>

</html>
"""


@app.get("/dashboard", response_class=HTMLResponse)
def dashboard():

    total = len(runs)

    approved = len([
        r for r in runs
        if r["decision"] == "APPROVED"
    ])

    pending = len([
        r for r in runs
        if r["decision"] == "PENDING"
    ])

    rejected = len([
        r for r in runs
        if r["decision"] == "REJECTED"
    ])

    return f"""

    <h1>Workflow Dashboard</h1>

    <h2>Total Runs: {total}</h2>

    <p>Approved: {approved}</p>

    <p>Pending: {pending}</p>

    <p>Rejected: {rejected}</p>

    """
