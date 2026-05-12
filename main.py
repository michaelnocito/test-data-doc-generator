import webview
import os
import sys
import json
import random
import string
from pathlib import Path
from datetime import datetime, timedelta

# ---------------------------------------------------------------------------
# FICTIONAL DATA HELPERS
# ---------------------------------------------------------------------------

FIRST_NAMES = ["Alex","Jordan","Morgan","Taylor","Casey","Riley","Jamie","Avery",
               "Peyton","Quinn","Drew","Reese","Skyler","Blake","Cameron"]
LAST_NAMES  = ["Rivera","Chen","Okafor","Patel","Novak","Larsen","Osei","Fujita",
               "Delacroix","Vasquez","Thornton","Mbeki","Sorensen","Haddad","Winters"]
COMPANY_SUFFIXES = ["LLC","Inc.","Corp.","Group","Solutions","Partners","Services","Technologies"]
COMPANY_WORDS   = ["Apex","Nexus","Crestview","Riverdale","Pinnacle","Lakewood",
                   "Summit","Horizon","Clearwater","Meridian","Ironwood","Bridgepoint"]
STREETS = ["Main St","Oak Ave","Maple Dr","Cedar Blvd","Elm St","Park Rd","Lake Dr","Ridge Rd"]
CITIES  = [
    ("Springfield","IL","62701"),("Riverdale","NY","10471"),("Lakewood","CO","80214"),
    ("Fairview","TX","75069"),("Maplewood","NJ","07040"),("Cedarville","OH","45314"),
    ("Brookhaven","GA","30319"),("Crestwood","MO","63126")
]
STATES = ["AL","AZ","CA","CO","FL","GA","IL","IN","MA","MI",
          "MN","MO","NC","NJ","NV","NY","OH","OR","PA","TX","VA","WA","WI"]

def rand_name():
    return f"{random.choice(FIRST_NAMES)} {random.choice(LAST_NAMES)}"

def rand_company():
    return f"{random.choice(COMPANY_WORDS)} {random.choice(COMPANY_WORDS)} {random.choice(COMPANY_SUFFIXES)}"

def rand_address():
    num = random.randint(100, 9999)
    street = random.choice(STREETS)
    city, state, zip_ = random.choice(CITIES)
    return f"{num} {street}", f"{city}, {state} {zip_}"

def rand_phone():
    area = random.randint(200, 999)
    mid  = random.randint(200, 999)
    end  = random.randint(1000, 9999)
    return f"({area}) {mid}-{end}"

def rand_email(name: str, company: str):
    local = name.lower().replace(" ", ".")
    domain = company.split()[0].lower()
    return f"{local}@{domain}.example.com"

def rand_date(start_offset=0, end_offset=365):
    base = datetime.today() + timedelta(days=start_offset)
    delta = random.randint(0, end_offset)
    return (base + timedelta(days=delta)).strftime("%B %d, %Y")

def rand_id(prefix="DOC", length=8):
    chars = string.ascii_uppercase + string.digits
    return prefix + "-" + "".join(random.choices(chars, k=length))

def rand_amount(lo=1000, hi=250000):
    return f"${random.randint(lo, hi):,}.00"


# ---------------------------------------------------------------------------
# DOCUMENT GENERATORS
# ---------------------------------------------------------------------------

DISCLAIMER_FOOTER = (
    "SAMPLE — For testing, demo, or training use only. "
    "Not valid for legal, financial, medical, regulatory, or identity purposes."
)
WATERMARK = "TEST DOCUMENT"


def _html_wrap(title: str, body: str) -> str:
    """Wrap content in a clean HTML shell with watermark and footer."""
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>{title}</title>
<style>
  body {{ font-family: 'Segoe UI', Arial, sans-serif; font-size: 13px; color: #1a1a1a;
          max-width: 820px; margin: 40px auto; padding: 0 32px; line-height: 1.6; }}
  h1   {{ font-size: 20px; margin-bottom: 4px; }}
  h2   {{ font-size: 15px; margin: 24px 0 8px; border-bottom: 1px solid #ccc; padding-bottom: 4px; }}
  table {{ width: 100%; border-collapse: collapse; margin: 12px 0; }}
  th, td {{ border: 1px solid #ccc; padding: 7px 10px; text-align: left; font-size: 12px; }}
  th   {{ background: #f0f0f0; font-weight: 600; }}
  .meta {{ color: #555; font-size: 11px; margin-bottom: 24px; }}
  .watermark {{
    position: fixed; top: 46%; left: 50%; transform: translate(-50%,-50%) rotate(-35deg);
    font-size: 72px; color: rgba(0,0,0,0.06); font-weight: 900; pointer-events: none;
    white-space: nowrap; z-index: 0; user-select: none;
  }}
  .footer {{
    margin-top: 48px; border-top: 1px solid #ddd; padding-top: 10px;
    font-size: 10px; color: #888; text-align: center;
  }}
</style>
</head>
<body>
<div class="watermark">{WATERMARK}</div>
{body}
<div class="footer">{DISCLAIMER_FOOTER}</div>
</body>
</html>"""


def generate_invoice(config: dict) -> dict:
    vendor   = config.get("vendorName") or rand_company()
    buyer    = config.get("buyerName")  or rand_company()
    v_addr1, v_addr2 = rand_address()
    b_addr1, b_addr2 = rand_address()
    inv_num  = rand_id("INV")
    inv_date = rand_date(-30, 0)
    due_date = rand_date(0, 30)

    items = []
    total = 0
    for _ in range(random.randint(2, 6)):
        desc  = random.choice(["Professional Services","Software License","Consulting Hours",
                               "Support & Maintenance","Implementation Services","Training"])
        qty   = random.randint(1, 20)
        rate  = random.randint(50, 500)
        amt   = qty * rate
        total += amt
        items.append((desc, qty, f"${rate:,.2f}", f"${amt:,.2f}"))

    rows = "".join(
        f"<tr><td>{d}</td><td>{q}</td><td>{r}</td><td>{a}</td></tr>"
        for d, q, r, a in items
    )

    body = f"""
    <h1>INVOICE</h1>
    <div class="meta">
      <strong>Invoice #:</strong> {inv_num} &nbsp;|
      <strong>Date:</strong> {inv_date} &nbsp;|
      <strong>Due:</strong> {due_date}
    </div>
    <h2>From</h2>
    <p><strong>{vendor}</strong><br>{v_addr1}<br>{v_addr2}<br>{rand_phone()}</p>
    <h2>Bill To</h2>
    <p><strong>{buyer}</strong><br>{b_addr1}<br>{b_addr2}<br>{rand_phone()}</p>
    <h2>Line Items</h2>
    <table>
      <tr><th>Description</th><th>Qty</th><th>Unit Rate</th><th>Amount</th></tr>
      {rows}
      <tr><td colspan="3"><strong>Total</strong></td><td><strong>${total:,.2f}</strong></td></tr>
    </table>
    """
    return {"filename": f"{inv_num}.html", "html": _html_wrap(f"Invoice {inv_num}", body)}


def generate_contract(config: dict) -> dict:
    buyer    = config.get("buyerName")  or rand_company()
    vendor   = config.get("vendorName") or rand_company()
    b_addr1, b_addr2 = rand_address()
    v_addr1, v_addr2 = rand_address()
    contract_type = config.get("contractType", "MSA")
    doc_id   = rand_id(contract_type)
    eff_date = rand_date(-90, 0)
    exp_date = rand_date(300, 730)

    body = f"""
    <h1>{contract_type} — Master Service Agreement</h1>
    <div class="meta">
      <strong>Doc ID:</strong> {doc_id} &nbsp;|
      <strong>Effective:</strong> {eff_date} &nbsp;|
      <strong>Expires:</strong> {exp_date}
    </div>
    <h2>Parties</h2>
    <p><strong>Client:</strong> {buyer}, {b_addr1}, {b_addr2}</p>
    <p><strong>Vendor:</strong> {vendor}, {v_addr1}, {v_addr2}</p>
    <h2>1. Scope of Services</h2>
    <p>Vendor agrees to provide professional services as mutually agreed in writing.
    Services shall be performed in a professional manner consistent with industry standards.</p>
    <h2>2. Term</h2>
    <p>This Agreement commences on {eff_date} and continues through {exp_date} unless earlier terminated.</p>
    <h2>3. Compensation</h2>
    <p>Client shall pay Vendor {rand_amount()} annually, invoiced quarterly, due within 30 days of receipt.</p>
    <h2>4. Confidentiality</h2>
    <p>Both parties agree to hold in strict confidence any proprietary information exchanged under this Agreement.</p>
    <h2>5. Governing Law</h2>
    <p>This Agreement shall be governed by the laws of the State of {random.choice(STATES)}.</p>
    <h2>Signatures</h2>
    <table>
      <tr><th>Client</th><th>Vendor</th></tr>
      <tr><td>{rand_name()}<br>{buyer}</td><td>{rand_name()}<br>{vendor}</td></tr>
    </table>
    """
    return {"filename": f"{doc_id}_contract.html", "html": _html_wrap(f"{contract_type} {doc_id}", body)}


def generate_intake_form(config: dict) -> dict:
    org   = config.get("buyerName") or rand_company()
    doc_id = rand_id("FORM")
    name   = rand_name()
    dob    = rand_date(-365*40, -365*18)
    addr1, addr2 = rand_address()

    body = f"""
    <h1>Intake / Registration Form</h1>
    <div class="meta"><strong>Form ID:</strong> {doc_id} &nbsp;| <strong>Organization:</strong> {org}</div>
    <h2>Applicant Information</h2>
    <table>
      <tr><th>Field</th><th>Value</th></tr>
      <tr><td>Full Name</td><td>{name}</td></tr>
      <tr><td>Date of Birth</td><td>{dob}</td></tr>
      <tr><td>Address</td><td>{addr1}, {addr2}</td></tr>
      <tr><td>Phone</td><td>{rand_phone()}</td></tr>
      <tr><td>Email</td><td>{rand_email(name, org)}</td></tr>
      <tr><td>Preferred Contact</td><td>{random.choice(["Phone","Email","Mail"])}</td></tr>
    </table>
    <h2>Service Request</h2>
    <table>
      <tr><th>Field</th><th>Value</th></tr>
      <tr><td>Service Type</td><td>{random.choice(["New Enrollment","Transfer","Update","Renewal","Inquiry"])}</td></tr>
      <tr><td>Requested Date</td><td>{rand_date(0, 30)}</td></tr>
      <tr><td>Notes</td><td>N/A</td></tr>
    </table>
    <h2>Acknowledgment</h2>
    <p>I certify the information above is accurate to the best of my knowledge.</p>
    <p>Signature: ______________________________ &nbsp; Date: ___________</p>
    """
    return {"filename": f"{doc_id}_intake.html", "html": _html_wrap(f"Intake Form {doc_id}", body)}


def generate_sop(config: dict) -> dict:
    org    = config.get("buyerName") or rand_company()
    doc_id = rand_id("SOP")
    topic  = random.choice(["Vendor Onboarding","Data Entry Review","Document Archiving",
                            "Access Request","Incident Response","Quality Review"])
    body = f"""
    <h1>Standard Operating Procedure</h1>
    <div class="meta">
      <strong>Doc ID:</strong> {doc_id} &nbsp;|
      <strong>Topic:</strong> {topic} &nbsp;|
      <strong>Organization:</strong> {org}
    </div>
    <h2>Purpose</h2>
    <p>This SOP defines the standard process for {topic.lower()} within {org}.</p>
    <h2>Scope</h2>
    <p>Applies to all staff involved in {topic.lower()} activities.</p>
    <h2>Procedure</h2>
    <table>
      <tr><th>Step</th><th>Action</th><th>Responsible</th></tr>
      {''.join(f"<tr><td>{i+1}</td><td>{a}</td><td>{random.choice(['Manager','Analyst','Admin','Lead'])}</td></tr>"
        for i,a in enumerate([
          "Initiate request and document in tracking system",
          "Review for completeness and accuracy",
          "Escalate to supervisor if exceptions found",
          "Obtain required approvals",
          "Complete processing and file documentation",
          "Confirm completion with requesting party"
        ]))}
    </table>
    <h2>Review Schedule</h2>
    <p>This SOP shall be reviewed annually. Last reviewed: {rand_date(-365, 0)}.</p>
    """
    return {"filename": f"{doc_id}_sop.html", "html": _html_wrap(f"SOP {doc_id}", body)}


def generate_offer_letter(config: dict) -> dict:
    org    = config.get("buyerName") or rand_company()
    doc_id = rand_id("OFR")
    name   = rand_name()
    role   = random.choice(["Data Analyst","Project Manager","Software Engineer",
                            "Operations Coordinator","Business Analyst","IT Specialist"])
    salary = random.randint(45, 135) * 1000
    start  = rand_date(7, 45)
    body = f"""
    <h1>Employment Offer Letter</h1>
    <div class="meta"><strong>Ref:</strong> {doc_id} &nbsp;| <strong>Date:</strong> {rand_date(-5,0)}</div>
    <p>Dear {name},</p>
    <p>We are pleased to offer you the position of <strong>{role}</strong> at <strong>{org}</strong>.
    This is a full-time position with a start date of <strong>{start}</strong>.</p>
    <h2>Compensation & Benefits</h2>
    <table>
      <tr><th>Item</th><th>Detail</th></tr>
      <tr><td>Annual Salary</td><td>${salary:,}.00</td></tr>
      <tr><td>Benefits</td><td>Medical, Dental, Vision — effective 30 days from start</td></tr>
      <tr><td>PTO</td><td>{random.randint(10,20)} days per year</td></tr>
      <tr><td>Work Location</td><td>{random.choice(["On-site","Remote","Hybrid"])}</td></tr>
    </table>
    <p>Please sign and return this letter by <strong>{rand_date(3,10)}</strong> to confirm your acceptance.</p>
    <p>We look forward to welcoming you to the team.</p>
    <p>Sincerely,<br><strong>{rand_name()}</strong><br>Human Resources, {org}</p>
    <p style="margin-top:32px">Accepted: ______________________________ &nbsp; Date: ___________</p>
    """
    return {"filename": f"{doc_id}_offer.html", "html": _html_wrap(f"Offer Letter {doc_id}", body)}


def generate_purchase_order(config: dict) -> dict:
    buyer  = config.get("buyerName")  or rand_company()
    vendor = config.get("vendorName") or rand_company()
    doc_id = rand_id("PO")
    po_date = rand_date(-10, 0)

    items = []
    total = 0
    for _ in range(random.randint(3, 8)):
        desc = random.choice(["Office Supplies","Hardware","Software License",
                              "Furniture","IT Equipment","Maintenance Services","Subscription"])
        qty  = random.randint(1, 50)
        unit = random.randint(10, 2000)
        amt  = qty * unit
        total += amt
        items.append((desc, qty, f"${unit:,.2f}", f"${amt:,.2f}"))

    rows = "".join(
        f"<tr><td>{d}</td><td>{q}</td><td>{r}</td><td>{a}</td></tr>"
        for d, q, r, a in items
    )
    body = f"""
    <h1>Purchase Order</h1>
    <div class="meta">
      <strong>PO #:</strong> {doc_id} &nbsp;|
      <strong>Date:</strong> {po_date}
    </div>
    <h2>Buyer</h2>
    <p><strong>{buyer}</strong></p>
    <h2>Vendor</h2>
    <p><strong>{vendor}</strong></p>
    <h2>Order Items</h2>
    <table>
      <tr><th>Description</th><th>Qty</th><th>Unit Price</th><th>Total</th></tr>
      {rows}
      <tr><td colspan="3"><strong>Order Total</strong></td><td><strong>${total:,.2f}</strong></td></tr>
    </table>
    <p>Authorized by: ______________________________ &nbsp; Date: ___________</p>
    """
    return {"filename": f"{doc_id}_po.html", "html": _html_wrap(f"PO {doc_id}", body)}


# Map UI doc type keys to generator functions
DOC_GENERATORS = {
    "invoice":        generate_invoice,
    "contract":       generate_contract,
    "intake_form":    generate_intake_form,
    "sop":            generate_sop,
    "offer_letter":   generate_offer_letter,
    "purchase_order": generate_purchase_order,
}


# ---------------------------------------------------------------------------
# PYWEBVIEW API
# ---------------------------------------------------------------------------

class API:
    def generate(self, payload: dict):
        """
        payload keys:
          buyerName, vendorName, docTypes (list of keys from DOC_GENERATORS),
          contractType, outputFolder, quantity
        """
        output_folder = Path(payload.get("outputFolder") or Path.home() / "Documents" / "sample_docs")
        output_folder.mkdir(parents=True, exist_ok=True)

        doc_types = payload.get("docTypes", [])
        quantity  = int(payload.get("quantity", 1))
        results   = []

        for doc_key in doc_types:
            gen_fn = DOC_GENERATORS.get(doc_key)
            if not gen_fn:
                continue
            for _ in range(quantity):
                result = gen_fn(payload)
                out_path = output_folder / result["filename"]
                out_path.write_text(result["html"], encoding="utf-8")
                results.append(str(out_path))

        return {"success": True, "files": results, "folder": str(output_folder)}

    def choose_folder(self):
        dirs = webview.windows[0].create_file_dialog(webview.FOLDER_DIALOG)
        if dirs and len(dirs) > 0:
            return dirs[0]
        return None

    def open_folder(self, folder_path: str):
        os.startfile(folder_path) if sys.platform == "win32" else os.system(f'open "{folder_path}"')


# ---------------------------------------------------------------------------
# ENTRY POINT
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    api = API()
    ui_path = Path(__file__).parent / "ui.html"
    webview.create_window(
        title="Test Data & Document Generator",
        url=str(ui_path),
        js_api=api,
        width=860,
        height=780,
        min_size=(700, 600),
        resizable=True,
    )
    webview.start(debug=False)
