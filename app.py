from fastapi import FastAPI, Form
from fastapi.responses import HTMLResponse
import re
import time

app = FastAPI(title="Vendor Onboarding Workflow")

runs = []


def validate_vendor(company, bank_name, country, tax_id, documents):

    issues = []
    stages = []

    # 1. Submission received
    stages.append(("Submission Received", "passed"))

    # 2. Required information
    time.sleep(0.4)

    required_valid = all([
        company.strip(),
        bank_name.strip(),
        country.strip(),
        tax_id.strip()
    ])

    if not required_valid:
        issues.append("Required information is missing.")

    stages.append((
        "Required Information Validation",
        "passed" if required_valid else "warning"
    ))

    # 3. Tax ID validation
    time.sleep(0.4)

   tax_id = tax_id.strip()

if country == "India":
    # Simplified GSTIN-style validation for demo purposes
    tax_valid = bool(
        re.match(r"^[0-9]{2}[A-Z]{5}[0-9]{4}[A-Z][0-9A-Z]Z[0-9A-Z]$", tax_id.upper())
    )

elif country == "United States":
    # Simplified US Tax ID validation
    tax_valid = bool(
        re.match(r"^[0-9]{2}-?[0-9]{7}$", tax_id)
    )

elif country == "United Kingdom":
    # Simplified UK tax reference validation
    tax_valid = bool(
        re.match(r"^[A-Za-z0-9]{8,15}$", tax_id)
    )

else:
    tax_valid = bool(
        re.match(r"^[A-Za-z0-9]{6,20}$", tax_id)
    )
    if not tax_valid:
        issues.append(
            "Tax ID format does not match the selected country.""
        )

    stages.append((
        "Tax ID Validation",
        "passed" if tax_valid else "warning"
    ))

    # 4. Bank / company cross-check
    time.sleep(0.4)

    company_clean = company.lower().replace(" ", "")
    bank_clean = bank_name.lower().replace(" ", "")

    company_match = (
        company_clean in bank_clean
        or bank_clean in company_clean
    )

    if not company_match:
        issues.append(
            "Company name does not match the bank account holder."
        )

    stages.append((
        "Bank Detail Cross-Check",
        "passed" if company_match else "failed"
    ))

    # 5. Document validation
    time.sleep(0.4)

    required_docs = [
        "Tax Registration",
        "Bank Proof"
    ]

    missing_docs = [
        doc for doc in required_docs
        if doc not in documents
    ]

    if missing_docs:
        issues.append(
            "Missing documents: " + ", ".join(missing_docs)
        )

    stages.append((
        "Document Validation",
        "passed" if not missing_docs else "warning"
    ))

    # 6. Final decision
    time.sleep(0.4)

    if not company_match:
        decision = "REJECTED"
        reason = (
            "The submission contains a significant inconsistency "
            "between the company and bank account holder. "
            "Manual investigation is recommended."
        )

    elif not required_valid or not tax_valid or missing_docs:
        decision = "PENDING"
        reason = (
            "The submission requires additional information or "
            "corrections before it can be approved."
        )

    else:
        decision = "APPROVED"
        reason = (
            "All required information, documents and validation "
            "checks passed successfully."
        )

    stages.append(("Decision Generated", "passed"))

    return decision, reason, issues, stages


@app.get("/", response_class=HTMLResponse)
def home():

    history = "".join([
        f"""
        <div class="history-item">
            <strong>{run["company"]}</strong>
            <span class="{run["decision"].lower()}">
                {run["decision"]}
            </span>
        </div>
        """
        for run in runs[-5:][::-1]
    ])

    if not history:
        history = "<p class='muted'>No workflow runs yet.</p>"

    return f"""
<!DOCTYPE html>
<html>

<head>

<title>Vendor Onboarding Workflow</title>

<style>

* {{
    box-sizing: border-box;
}}

body {{
    font-family: Arial, sans-serif;
    background: #f4f6f9;
    margin: 0;
    padding: 40px 20px;
    color: #1e293b;
}}

.container {{
    max-width: 950px;
    margin: auto;
}}

.header {{
    margin-bottom: 30px;
}}

h1 {{
    margin-bottom: 8px;
}}

.subtitle {{
    color: #64748b;
}}

.card {{
    background: white;
    padding: 28px;
    border-radius: 14px;
    margin-bottom: 24px;
    box-shadow: 0 4px 18px rgba(0,0,0,0.08);
}}

input, select {{
    width: 100%;
    padding: 12px;
    margin-top: 8px;
    margin-bottom: 18px;
    border: 1px solid #d1d5db;
    border-radius: 8px;
    font-size: 15px;
}}

.documents {{
    margin: 12px 0 24px 0;
}}

.checkbox {{
    display: flex;
    align-items: center;
    gap: 10px;
    margin: 12px 0;
    padding: 12px;
    background: #f8fafc;
    border-radius: 8px;
}}

.checkbox input {{
    width: auto;
    margin: 0;
}}

button {{
    background: #2563eb;
    color: white;
    border: none;
    padding: 14px 22px;
    border-radius: 8px;
    cursor: pointer;
    font-size: 16px;
}}

button:hover {{
    background: #1d4ed8;
}}

.workflow {{
    display: flex;
    flex-wrap: wrap;
    gap: 10px;
    align-items: center;
}}

.step {{
    background: #eef2ff;
    padding: 10px 14px;
    border-radius: 8px;
    font-size: 14px;
}}

.arrow {{
    color: #64748b;
}}

.history-item {{
    display: flex;
    justify-content: space-between;
    padding: 14px;
    margin: 8px 0;
    background: #f8fafc;
    border-radius: 8px;
}}

.approved {{
    color: #15803d;
    font-weight: bold;
}}

.pending {{
    color: #d97706;
    font-weight: bold;
}}

.rejected {{
    color: #dc2626;
    font-weight: bold;
}}

.muted {{
    color: #94a3b8;
}}

.dashboard-link {{
    display: inline-block;
    margin-top: 10px;
}}

</style>

</head>

<body>

<div class="container">

<div class="header">

<h1>Vendor Onboarding Workflow</h1>

<p class="subtitle">
Automated validation and decision workflow for vendor submissions
</p>

</div>

<div class="card">

<h2>New Vendor Submission</h2>

<form action="/process" method="post">

<label>Company Name</label>
<input
    name="company"
    placeholder="e.g. Acme Technologies Pvt Ltd"
    required
>

<label>Bank Account Holder Name</label>
<input
    name="bank_name"
    placeholder="Enter registered bank account holder name"
    required
>

<label>Country</label>

<select name="country">

<option value="India">India</option>
<option value="United States">United States</option>
<option value="United Kingdom">United Kingdom</option>

</select>

<label>Tax ID</label>

<input
    name="tax_id"
    placeholder="Enter Tax ID"
    required
>

<label>Submitted Documents</label>

<div class="documents">

<label class="checkbox">
<input
    type="checkbox"
    name="documents"
    value="Tax Registration"
>
Tax Registration
</label>

<label class="checkbox">
<input
    type="checkbox"
    name="documents"
    value="Bank Proof"
>
Bank Proof
</label>

<label class="checkbox">
<input
    type="checkbox"
    name="documents"
    value="Compliance Certificate"
>
Compliance Certificate
</label>

</div>

<button type="submit">
Run Vendor Workflow
</button>

</form>

</div>

<div class="card">

<h2>Process Design</h2>

<div class="workflow">

<div class="step">Submission</div>

<div class="arrow">→</div>

<div class="step">Validation</div>

<div class="arrow">→</div>

<div class="step">Cross-check</div>

<div class="arrow">→</div>

<div class="step">Decision</div>

</div>

</div>

<div class="card">

<h2>Recent Workflow Runs</h2>

{history}

<p>
<a class="dashboard-link" href="/dashboard">
View Workflow Dashboard →
</a>
</p>

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

    stage_html = ""

    for name, status in stages:

        if status == "passed":
            icon = "✓"
            label = "Passed"
            css = "passed"

        elif status == "warning":
            icon = "⚠"
            label = "Attention Required"
            css = "warning"

        else:
            icon = "✕"
            label = "Failed"
            css = "failed"

        stage_html += f"""
        <div class="stage {css}">
            <div>
                <strong>{icon} {name}</strong>
            </div>

            <span>{label}</span>
        </div>
        """

    issues_html = ""

    if issues:

        issues_html = "<h3>Issues Requiring Attention</h3>"

        for issue in issues:

            issues_html += f"""
            <div class="issue">
                ⚠ {issue}
            </div>
            """

    else:

        issues_html = """
        <div class="success">
            ✓ No issues detected.
        </div>
        """

    return f"""
<!DOCTYPE html>

<html>

<head>

<title>Vendor Onboarding Result</title>

<style>

body {{
    font-family: Arial, sans-serif;
    background: #f4f6f9;
    margin: 0;
    padding: 40px 20px;
    color: #1e293b;
}}

.container {{
    max-width: 950px;
    margin: auto;
}}

.card {{
    background: white;
    padding: 28px;
    border-radius: 14px;
    margin-bottom: 24px;
    box-shadow: 0 4px 18px rgba(0,0,0,0.08);
}}

.result {{
    font-size: 32px;
    font-weight: bold;
    margin: 15px 0;
}}

.approved {{
    color: #15803d;
}}

.pending {{
    color: #d97706;
}}

.rejected {{
    color: #dc2626;
}}

.stage {{
    display: flex;
    justify-content: space-between;
    padding: 16px;
    margin: 10px 0;
    border-radius: 8px;
}}

.passed {{
    background: #f0fdf4;
    border-left: 4px solid #22c55e;
}}

.warning {{
    background: #fffbeb;
    border-left: 4px solid #f59e0b;
}}

.failed {{
    background: #fef2f2;
    border-left: 4px solid #ef4444;
}}

.issue {{
    padding: 14px;
    margin: 10px 0;
    background: #fff7ed;
    border-radius: 8px;
}}

.success {{
    padding: 14px;
    background: #f0fdf4;
    border-radius: 8px;
    color: #15803d;
}}

button {{
    background: #2563eb;
    color: white;
    border: none;
    padding: 14px 22px;
    border-radius: 8px;
    cursor: pointer;
    font-size: 16px;
}}

</style>

</head>

<body>

<div class="container">

<div class="card">

<h1>Vendor Onboarding Decision</h1>

<div class="result {decision.lower()}">
{decision}
</div>

<p>{reason}</p>

</div>

<div class="card">

<h2>Workflow Execution</h2>

{stage_html}

</div>

<div class="card">

{issues_html}

</div>

<a href="/">
<button>Run Another Submission</button>
</a>

<a href="/dashboard">
<button>View Dashboard</button>
</a>

</div>

</body>

</html>
"""


@app.get("/dashboard", response_class=HTMLResponse)
def dashboard():

    total = len(runs)

    approved = sum(
        1 for run in runs
        if run["decision"] == "APPROVED"
    )

    pending = sum(
        1 for run in runs
        if run["decision"] == "PENDING"
    )

    rejected = sum(
        1 for run in runs
        if run["decision"] == "REJECTED"
    )

    return f"""
<!DOCTYPE html>

<html>

<head>

<title>Workflow Dashboard</title>

<style>

body {{
    font-family: Arial;
    background: #f4f6f9;
    padding: 40px;
    color: #1e293b;
}}

.container {{
    max-width: 950px;
    margin: auto;
}}

.stats {{
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 15px;
}}

.stat {{
    background: white;
    padding: 25px;
    border-radius: 12px;
    box-shadow: 0 4px 12px rgba(0,0,0,0.08);
}}

.number {{
    font-size: 32px;
    font-weight: bold;
}}

a {{
    display: inline-block;
    margin-top: 30px;
}}

</style>

</head>

<body>

<div class="container">

<h1>Workflow Dashboard</h1>

<p>Operational overview of vendor onboarding runs.</p>

<div class="stats">

<div class="stat">
<p>Total Runs</p>
<div class="number">{total}</div>
</div>

<div class="stat">
<p>Approved</p>
<div class="number">{approved}</div>
</div>

<div class="stat">
<p>Pending</p>
<div class="number">{pending}</div>
</div>

<div class="stat">
<p>Rejected</p>
<div class="number">{rejected}</div>
</div>

</div>

<a href="/">← Back to Workflow</a>

</div>

</body>

</html>
"""
