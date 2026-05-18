"""Intake form document generator."""

import random
import secrets

from recordforge.core.faker_utils import rand_date_pair, rand_party, rand_person
from recordforge.core.models import DocumentData

_SERVICES = [
    (
        "Enterprise Software Implementation",
        "Full implementation of enterprise resource planning (ERP) platform including discovery, configuration, data migration, user acceptance testing, and go-live support.",
        "Platform has been selected. We need an implementation partner with proven ERP experience in our industry.",
    ),
    (
        "Data Migration and Integration Services",
        "Migration of legacy system data to new cloud platform, including data profiling, cleansing, mapping, ETL build, and post-migration validation.",
        "Existing system is end-of-life in Q3. Migration must be complete before the decommission date.",
    ),
    (
        "IT Infrastructure Assessment",
        "Comprehensive assessment of current on-premise infrastructure, network architecture, and security posture, with recommendations for cloud readiness and modernization roadmap.",
        "Board has approved a cloud migration initiative. We need an objective third-party assessment before selecting a vendor.",
    ),
    (
        "Management Consulting — Process Optimization",
        "Current-state analysis of core operational workflows, bottleneck identification, future-state design, and implementation roadmap for process improvement across three business units.",
        "Recent audit identified significant process inefficiencies. Leadership has committed resources to address them.",
    ),
    (
        "Custom Software Development",
        "Development of a customer-facing web portal and supporting API integrations to replace a manual, spreadsheet-based workflow used by approximately 200 internal users.",
        "The current process cannot scale with projected growth. A custom solution is required as no off-the-shelf product meets our requirements.",
    ),
]

_INDUSTRIES = [
    "Healthcare", "Financial Services", "Manufacturing", "Retail",
    "Logistics & Supply Chain", "Professional Services", "Technology",
    "Nonprofit", "Government / Public Sector", "Education",
]

_TIMELINES = [
    "Immediately — project is urgent and budget is approved",
    "Within 30 days — pending final stakeholder sign-off",
    "Within 60–90 days — procurement process underway",
    "Q3 start — budgeted for next fiscal quarter",
    "Flexible — no hard deadline, seeking the right partner",
]

_BUDGETS = [
    "Under $50,000",
    "$50,000 – $100,000",
    "$100,000 – $250,000",
    "$250,000 – $500,000",
    "Over $500,000",
    "To be determined based on scoping",
]

_PAIN_POINTS = [
    "manual processes that are error-prone and time-consuming",
    "lack of real-time visibility into key operational metrics",
    "system fragmentation requiring excessive manual data reconciliation",
    "inability to scale current workflows with organizational growth",
    "compliance gaps identified in recent audit findings",
    "outdated technology creating security and maintenance risk",
]

_PRIORITIES = [
    ["On-time delivery", "Budget adherence", "Minimal disruption to operations"],
    ["Technical expertise", "Industry experience", "Transparent communication"],
    ["Scalability of solution", "Quality of documentation", "Post-launch support model"],
    ["Cultural fit", "Executive involvement", "Proven methodology"],
]


def build(rng: random.Random) -> DocumentData:
    """Build a randomized intake form DocumentData instance."""
    buyer = rand_party(rng)
    vendor = rand_party(rng)
    doc_date, _ = rand_date_pair(rng)
    contact = rand_person(rng)
    alt_contact = rand_person(rng)
    service_name, service_desc, service_context = rng.choice(_SERVICES)
    industry = rng.choice(_INDUSTRIES)
    emp_count = rng.choice(["1–50", "51–200", "201–500", "501–1,000", "1,001–5,000", "5,000+"])
    timeline = rng.choice(_TIMELINES)
    budget = rng.choice(_BUDGETS)
    pain_point = rng.choice(_PAIN_POINTS)
    priorities = rng.choice(_PRIORITIES)
    priorities_text = "\n  ".join(f"{i+1}. {p}" for i, p in enumerate(priorities))
    how_heard = rng.choice([
        "Referral from a current client",
        "LinkedIn / professional network",
        "Industry conference or event",
        "Online search",
        "Industry association membership",
        "Published case study or white paper",
    ])
    record_id = secrets.token_hex(4).upper()

    notes = f"""SERVICE INQUIRY AND INTAKE FORM

Record ID: {record_id}
Submission Date: {doc_date}
Status: Pending Review


SECTION 1 — ORGANIZATION INFORMATION

Organization Name: {buyer.name}
Industry: {industry}
Organization Size (Employees): {emp_count}
Headquarters Address: {buyer.address1}, {buyer.address2}
Website: [On File]


SECTION 2 — PRIMARY CONTACT

Name: {contact}
Title: [On File]
Organization: {buyer.name}
Phone: {buyer.phone}
Email: {buyer.email}

Alternate Contact: {alt_contact}
Alternate Phone: {buyer.phone}


SECTION 3 — SERVICE REQUEST

Service Category: {service_name}

Description of Need:
{service_desc}

Business Context:
{service_context}

Current State / Pain Points:
The organization is currently experiencing {pain_point}. This initiative is intended to address these challenges and position the organization for sustainable growth.


SECTION 4 — PROJECT PARAMETERS

Desired Start Timeline: {timeline}

Estimated Budget Range: {budget}

Note: Final budget authorization is contingent on scope confirmation and executive approval. The organization is prepared to discuss scope adjustments to align with budget parameters.

Project Decision Makers:
  - Executive Sponsor: [To Be Confirmed]
  - Project Lead: {contact}
  - IT / Technical Lead: [To Be Confirmed]
  - Finance / Procurement: [To Be Confirmed]

Procurement Process: Formal RFP process. Vendor will be required to submit a written proposal including scope, timeline, team composition, methodology, references, and fee schedule.

Proposal Deadline: To be communicated via formal RFP document.


SECTION 5 — EVALUATION CRITERIA

The following criteria will be used to evaluate vendor proposals (listed in priority order):
  {priorities_text}

References Required: Yes — minimum of two (2) references from comparable engagements within the past three (3) years. At least one reference should be from an organization of similar size and industry.


SECTION 6 — ADDITIONAL INFORMATION

How did you learn about {vendor.name}?
{how_heard}

Are there any known constraints or dependencies we should be aware of?
The project must work within existing IT infrastructure and comply with all applicable data privacy regulations. Vendor personnel working on-site will be required to execute an NDA prior to project kickoff.

Is there an incumbent vendor currently providing similar services?
[To Be Disclosed During Discovery]

Any additional comments or context:
We are committed to selecting a partner who will take the time to understand our business and deliver a solution tailored to our specific needs. We are not interested in a one-size-fits-all approach.


SECTION 7 — AUTHORIZATION

By submitting this intake form, the undersigned confirms that the information provided is accurate to the best of their knowledge and that they have the authority to initiate this inquiry on behalf of the organization.

Name: {contact}
Organization: {buyer.name}
Signature: ___________________________
Date: {doc_date}


FOR INTERNAL USE ONLY

Received By: ___________________________
Assigned To: ___________________________
Follow-Up Date: ___________________________
Notes: ___________________________"""

    return DocumentData(
        doc_type="intake_form",
        doc_number=f"INT-{record_id}",
        doc_date=doc_date,
        due_date=None,
        buyer=buyer,
        vendor=vendor,
        notes=notes,
    )
