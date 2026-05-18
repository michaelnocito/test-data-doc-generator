"""Offer letter document generator."""

import random

from recordforge.core.faker_utils import rand_date_pair, rand_party, rand_person
from recordforge.core.models import DocumentData

_POSITIONS = [
    ("Business Systems Analyst", "Technology Solutions", "Director of Technology"),
    ("Data Engineer", "Data & Analytics", "VP of Data Engineering"),
    ("Project Manager", "Program Management Office", "Director of PMO"),
    ("Operations Coordinator", "Operations", "VP of Operations"),
    ("Financial Analyst", "Finance & Accounting", "Controller"),
    ("IT Specialist", "Information Technology", "IT Director"),
    ("Solutions Architect", "Technology Solutions", "Chief Technology Officer"),
    ("Compliance Officer", "Risk & Compliance", "Chief Compliance Officer"),
    ("Product Manager", "Product Development", "VP of Product"),
    ("Senior Consultant", "Advisory Services", "Managing Director"),
]

_BENEFIT_PACKAGES = [
    {
        "health": "comprehensive medical, dental, and vision coverage effective on your first day of employment",
        "pto": "20 days of paid time off per year, accrued bi-weekly, plus 11 company-observed holidays",
        "retirement": "401(k) plan with a 4% company match, vesting immediately upon enrollment",
        "other": "employer-paid life insurance equal to one times your annual base salary, short-term and long-term disability coverage, and an annual professional development stipend of $1,500",
    },
    {
        "health": "medical, dental, and vision coverage with the company contributing 80% of employee premiums",
        "pto": "15 days of paid time off, accruing monthly, plus federal holidays and two floating personal days",
        "retirement": "403(b) retirement plan with a 3% company match after six months of employment",
        "other": "employee assistance program (EAP), flexible spending accounts (FSA), and commuter benefits up to $150/month",
    },
    {
        "health": "choice of three health plan tiers (HMO, PPO, HDHP) plus dental and vision; company covers 75% of premiums",
        "pto": "unlimited flexible paid time off subject to manager approval, plus 12 paid holidays annually",
        "retirement": "401(k) with Roth option and 5% company match, fully vested after two years",
        "other": "quarterly wellness reimbursement of $300, home office stipend of $500 upon hire, and tuition reimbursement up to $5,250 per year",
    },
]


def build(rng: random.Random) -> DocumentData:
    """Build a randomized offer letter DocumentData instance."""
    buyer = rand_party(rng)
    vendor = rand_party(rng)
    doc_date, start_date = rand_date_pair(rng)
    candidate = rand_person(rng)
    position, department, manager_title = rng.choice(_POSITIONS)
    manager = rand_person(rng)
    salary = rng.randint(55, 145) * 1000
    bonus_pct = rng.choice([0, 5, 8, 10, 12, 15])
    benefits = rng.choice(_BENEFIT_PACKAGES)
    accept_days = rng.choice([5, 7, 10])

    bonus_line = ""
    if bonus_pct > 0:
        bonus_target = int(salary * bonus_pct / 100)
        bonus_line = f"\nAnnual Performance Bonus: Target {bonus_pct}% of base salary (${bonus_target:,}), paid annually based on individual and company performance."

    notes = f"""{doc_date}

{candidate}
[Address on File]

Dear {candidate.split()[0]},

On behalf of {buyer.name}, I am pleased to extend this formal offer of employment. We were impressed by your background and believe your skills and experience will be a strong addition to our team. We look forward to the contributions you will make.


POSITION DETAILS

Job Title: {position}
Department: {department}
Reports To: {manager}, {manager_title}
Employment Type: Full-Time, Exempt
Start Date: {start_date}
Work Location: {buyer.address1}, {buyer.address2}


COMPENSATION

Base Salary: ${salary:,} per year, paid bi-weekly (${salary // 26:,} per pay period before applicable deductions).{bonus_line}

Compensation will be reviewed annually as part of the company's standard performance review process. Salary adjustments are at the discretion of management and are not guaranteed.


BENEFITS

As a full-time employee, you will be eligible for the following benefits:

Health & Insurance: {benefits['health']}.

Paid Time Off: {benefits['pto']}.

Retirement: {benefits['retirement']}.

Additional Benefits: {benefits['other']}.

Complete details regarding benefit plans, eligibility dates, and enrollment procedures will be provided during your onboarding. Benefits are subject to the terms and conditions of each plan and may be modified by the company at any time.


CONDITIONS OF EMPLOYMENT

This offer is contingent upon the following:

1. Successful completion of a pre-employment background check and, where required by law, a reference check.

2. Your execution of {buyer.name}'s standard Employee Confidentiality, Non-Disclosure, and Invention Assignment Agreement, which you will receive as part of your onboarding paperwork.

3. Verification of your legal authorization to work in the United States, as required by the Immigration Reform and Control Act (IRCA). You will need to provide acceptable identity and work authorization documents on or before your first day.

4. Compliance with all company policies and procedures, as outlined in the Employee Handbook, which will be made available to you upon hire.


AT-WILL EMPLOYMENT

Your employment with {buyer.name} is at-will, meaning that either you or the company may terminate the employment relationship at any time, with or without cause, and with or without notice. Nothing in this offer letter, the Employee Handbook, or any other company document creates a contract of employment for a definite term or guarantees employment for any specific period of time.


ACCEPTANCE

This offer will remain open until the close of business on the {accept_days}th business day following the date of this letter. To accept this offer, please sign and return a copy of this letter to {vendor.name} at {vendor.email} by that date.

If you have any questions about this offer or your upcoming start date, please contact {vendor.name} at {vendor.phone} or {vendor.email}. We are happy to discuss any aspect of this offer.

We are excited about the prospect of you joining our team and look forward to your acceptance.


Sincerely,

{vendor.name}
{buyer.name}
{vendor.phone} | {vendor.email}


CANDIDATE ACCEPTANCE

I, {candidate}, accept the offer of employment described in this letter under the terms and conditions set forth above. I understand that my employment is at-will and that this letter does not constitute a contract of employment.

Signature: ___________________________________
Printed Name: {candidate}
Date: ___________________"""

    return DocumentData(
        doc_type="offer_letter",
        doc_number=f"OFR-{rng.randint(100000, 999999)}",
        doc_date=doc_date,
        due_date=None,
        buyer=buyer,
        vendor=vendor,
        notes=notes,
    )
