"""Standard operating procedure document generator."""

import random

from recordforge.core.faker_utils import rand_date_pair, rand_party, rand_person
from recordforge.core.models import DocumentData

_PROCEDURES = [
    {
        "title": "Vendor Onboarding and Approval",
        "purpose": "To establish a standardized process for evaluating, approving, and onboarding new vendors to ensure compliance with organizational procurement policies, financial controls, and risk management requirements.",
        "scope": "This procedure applies to all departments initiating a new vendor relationship involving goods, services, or software with an expected annual spend exceeding $5,000. It does not apply to emergency procurement or pre-approved vendor list additions.",
        "definitions": [
            ("Vendor", "Any external supplier, contractor, or service provider engaged by the organization in exchange for payment."),
            ("Requestor", "The department employee initiating the vendor onboarding request."),
            ("Procurement Team", "The internal team responsible for vendor evaluation, negotiation, and contract management."),
            ("AP Department", "Accounts Payable, responsible for payment processing and vendor record management in the financial system."),
        ],
        "roles": [
            ("Requestor", "Initiates the request and provides business justification and vendor contact information."),
            ("Procurement Team", "Conducts due diligence, negotiates terms, and manages the approval workflow."),
            ("Finance / AP", "Reviews tax documentation, sets up vendor in the financial system, and processes payments."),
            ("Legal / Compliance", "Reviews contracts exceeding $50,000 or flagged for compliance risk."),
            ("Department Manager", "Approves the business need and budget availability."),
        ],
        "steps": [
            ("Identify Business Need", "Requestor identifies the need for a new vendor and confirms no approved vendor can fulfill the requirement. Requestor documents the business justification in the Procurement Request Form (PRF)."),
            ("Submit Procurement Request", "Requestor submits the completed PRF through the internal procurement portal, attaching at least two competitive quotes or a sole-source justification memo. Department Manager must co-sign the PRF prior to submission."),
            ("Initial Vendor Screening", "Procurement Team reviews the PRF for completeness within two (2) business days. Vendor is screened against the Debarred Vendor List and OFAC sanctions list. Any match results in automatic rejection and notification to the Requestor."),
            ("Due Diligence Package", "Procurement Team sends the vendor a Due Diligence Package via secure email, which includes: W-9 or W-8BEN tax form, Certificate of Insurance (COI) requirements, vendor questionnaire (financial stability, data security, references), and NDA for review and execution."),
            ("Due Diligence Review", "Upon receipt of completed due diligence materials, Procurement Team evaluates financial stability (D&B or equivalent), insurance coverage against required limits, data security posture for vendors with access to company systems, and references (minimum two required for contracts over $25,000)."),
            ("Contract Negotiation and Execution", "Procurement Team negotiates contract terms using the standard Master Services Agreement (MSA) template. Deviations from standard terms require Legal review. All contracts must be executed using the organization's approved e-signature platform. Fully executed contracts are archived in the Contract Management System within one (1) business day."),
            ("Vendor Setup in Financial System", "AP Department receives the executed contract and W-9 from Procurement within two (2) business days of execution. AP sets up the vendor record in the financial system, assigns a Vendor ID, and confirms ACH or check payment preference. Requestor is notified of the Vendor ID upon completion."),
            ("Requestor Notification and Handoff", "Procurement Team notifies the Requestor that the vendor is approved and active. Requestor receives the Vendor ID, primary contact information, and a copy of the executed contract. Procurement closes the PRF and updates the Vendor Registry."),
        ],
        "qc": [
            "All required due diligence documents are on file before contract execution.",
            "Contract is fully executed by authorized signatories from both parties.",
            "Vendor ID is confirmed in the financial system before the first purchase order is issued.",
            "Certificate of Insurance is current and meets required coverage limits.",
        ],
        "references": [
            "Procurement Policy (POL-PROC-001)",
            "Vendor Risk Assessment Framework (FRM-RISK-007)",
            "Master Services Agreement Template (TMPL-LEGAL-003)",
            "Data Security Vendor Questionnaire (FRM-IT-012)",
        ],
    },
    {
        "title": "Invoice Processing and Payment Approval",
        "purpose": "To define the standard process for receiving, validating, approving, and processing vendor invoices to ensure timely and accurate payment while maintaining appropriate financial controls.",
        "scope": "This procedure applies to all accounts payable staff, department managers with invoice approval authority, and any employee submitting or approving expense reimbursements. It covers all vendor invoices regardless of payment method.",
        "definitions": [
            ("Invoice", "A formal document issued by a vendor requesting payment for goods delivered or services rendered."),
            ("Three-Way Match", "The process of matching an invoice against the corresponding purchase order and receiving report before approving payment."),
            ("Approval Threshold", "The dollar amount above which additional approvers are required per the Delegation of Authority matrix."),
            ("AP Aging", "The report tracking outstanding invoices by days outstanding, used to manage cash flow and payment timing."),
        ],
        "roles": [
            ("AP Specialist", "Receives invoices, performs three-way match, enters invoices into the financial system, and routes for approval."),
            ("Department Manager", "Reviews and approves invoices for goods or services received by their department."),
            ("Finance Controller", "Approves invoices exceeding $10,000 and reviews weekly AP aging report."),
            ("VP Finance", "Approves invoices exceeding $50,000 and all wire transfers."),
            ("Vendor", "Submits invoices per the remittance instructions on the purchase order."),
        ],
        "steps": [
            ("Invoice Receipt", "All vendor invoices must be submitted to invoices@company.com or mailed to the AP department address. Invoices received by individual employees must be forwarded to AP within one (1) business day of receipt. Paper invoices are scanned and uploaded to the document management system within 24 hours."),
            ("Invoice Validation", "AP Specialist confirms the invoice includes: vendor name and remittance address, invoice number and date, purchase order number (if applicable), itemized description of goods or services, unit prices and extended amounts, and total amount due. Incomplete invoices are returned to the vendor with a request for correction within two (2) business days."),
            ("Three-Way Match", "For PO-based invoices, AP performs a three-way match against the original purchase order and the receiving report in the procurement system. Variances greater than 5% or $100 (whichever is lower) are escalated to the Requestor for review before processing."),
            ("System Entry", "AP Specialist enters the validated invoice into the financial system, coding to the appropriate general ledger account, cost center, and project code per the chart of accounts. Coding questions are escalated to the department manager or finance team within one (1) business day."),
            ("Approval Routing", "Invoices are routed electronically for approval per the Delegation of Authority: up to $2,500 — Department Manager; $2,501–$10,000 — Finance Controller; $10,001–$50,000 — Finance Controller + Division VP; over $50,000 — Finance Controller + Division VP + CFO. Approvers have three (3) business days to approve or return the invoice."),
            ("Payment Scheduling", "Approved invoices are scheduled for payment in accordance with vendor payment terms (Net 30 standard unless otherwise contracted). Early payment discounts (e.g., 2/10 Net 30) are flagged for Controller review. Payments are batched and processed on Tuesday and Thursday of each week."),
            ("Payment Execution", "ACH payments are initiated through the banking portal with dual approval required. Checks are printed, signed by two authorized signatories, and mailed via USPS. Wire transfers require VP Finance approval and are executed same-day when initiated before 2:00 PM local time."),
            ("Recordkeeping", "AP Specialist attaches proof of payment to the invoice record in the document management system and marks the invoice as paid in the financial system. Vendor payment confirmation is filed for a minimum of seven (7) years per the records retention policy."),
        ],
        "qc": [
            "Three-way match completed and documented for all PO-based invoices before payment.",
            "Invoice approved by all required signatories per the Delegation of Authority matrix.",
            "GL coding reviewed by department manager for accuracy before final posting.",
            "All wire transfers confirmed with receiving bank within one (1) business day.",
        ],
        "references": [
            "Accounts Payable Policy (POL-FIN-002)",
            "Delegation of Authority Matrix (DOA-FIN-2026)",
            "Chart of Accounts Reference Guide (FRM-FIN-001)",
            "Records Retention Schedule (POL-COMP-005)",
        ],
    },
]

_DEPARTMENTS = [
    "Finance & Accounting", "Operations", "Information Technology",
    "Human Resources", "Procurement", "Legal & Compliance", "Customer Success",
]


def build(rng: random.Random) -> DocumentData:
    """Build a randomized SOP DocumentData instance."""
    buyer = rand_party(rng)
    vendor = rand_party(rng)
    doc_date, _ = rand_date_pair(rng)
    proc = rng.choice(_PROCEDURES)
    owner = rand_person(rng)
    approver = rand_person(rng)
    dept = rng.choice(_DEPARTMENTS)
    sop_num = f"SOP-{rng.randint(100, 999)}-{rng.randint(10, 99)}"
    version = f"1.{rng.randint(0, 3)}"
    review_freq = rng.choice(["Annually", "Every 18 months", "Every 24 months"])

    definitions_block = "\n".join(
        f"  {term}: {definition}" for term, definition in proc["definitions"]
    )
    roles_block = "\n".join(
        f"  {role}: {resp}" for role, resp in proc["roles"]
    )
    steps_block = "\n\n".join(
        f"  Step {i+1}: {title}\n  {detail}"
        for i, (title, detail) in enumerate(proc["steps"])
    )
    qc_block = "\n".join(f"  ✓ {item}" for item in proc["qc"])
    refs_block = "\n".join(f"  - {ref}" for ref in proc["references"])

    notes = f"""STANDARD OPERATING PROCEDURE
{proc['title'].upper()}

Document Number: {sop_num}
Version: {version}
Effective Date: {doc_date}
Review Frequency: {review_freq}
Department: {dept}
Process Owner: {owner}
Approved By: {approver}


1. PURPOSE

{proc['purpose']}


2. SCOPE

{proc['scope']}


3. DEFINITIONS

{definitions_block}


4. ROLES AND RESPONSIBILITIES

{roles_block}


5. PROCEDURE

{steps_block}


6. QUALITY CHECKS AND CONTROLS

{qc_block}


7. EXCEPTIONS

Any deviation from this procedure requires written approval from the Process Owner or designee prior to action. All approved exceptions must be documented with a business justification and retained in the department exception log for audit purposes.


8. REFERENCES AND RELATED DOCUMENTS

{refs_block}


9. REVISION HISTORY

  Version {version} — {doc_date}: Initial release.
  Review scheduled: {review_freq.lower()} from effective date.


APPROVALS

Process Owner: {owner}
Signature: ___________________________  Date: ______________

Department Head: {approver}
Signature: ___________________________  Date: ______________"""

    return DocumentData(
        doc_type="sop",
        doc_number=sop_num,
        doc_date=doc_date,
        due_date=None,
        buyer=buyer,
        vendor=vendor,
        notes=notes,
    )
