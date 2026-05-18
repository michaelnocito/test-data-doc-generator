"""Contract document generator."""

import random

from recordforge.core.faker_utils import rand_date_pair, rand_party
from recordforge.core.models import DocumentData

_SCOPES = [
    (
        "implementation and deployment of enterprise software systems, including requirements "
        "gathering, configuration, testing, training, and post-launch hypercare support"
    ),
    (
        "management consulting and business process optimization services, including current-state "
        "assessment, gap analysis, roadmap development, and facilitated stakeholder workshops"
    ),
    (
        "data migration and systems integration services, including source data profiling, "
        "transformation mapping, ETL development, validation testing, and cutover support"
    ),
    (
        "IT infrastructure assessment and cloud readiness planning, including architecture review, "
        "security gap analysis, vendor evaluation, and detailed migration playbook development"
    ),
    (
        "custom software development services, including product discovery, UX design, agile "
        "development sprints, QA testing, documentation, and deployment to client environment"
    ),
]

_STATES = [
    "Delaware", "New York", "California", "Texas", "Illinois",
    "Florida", "Georgia", "Washington", "Colorado", "Pennsylvania",
]

_CORP_TYPES = ["limited liability company", "corporation", "professional services firm"]

_PAYMENT_SCHEDULES = [
    "fifty percent (50%) upon execution of this Agreement and fifty percent (50%) upon final acceptance of all deliverables",
    "one-third (1/3) upon execution, one-third (1/3) at the project midpoint milestone, and one-third (1/3) upon final delivery",
    "monthly in equal installments over the term of this Agreement, invoiced on the first business day of each month",
    "in full within fifteen (15) days of execution of this Agreement",
]


def build(rng: random.Random) -> DocumentData:
    """Build a randomized service contract DocumentData instance."""
    buyer = rand_party(rng)
    vendor = rand_party(rng)
    doc_date, due_date = rand_date_pair(rng)
    flat_fee = rng.randint(5, 50) * 1000
    scope = rng.choice(_SCOPES)
    state = rng.choice(_STATES)
    buyer_corp = rng.choice(_CORP_TYPES)
    vendor_corp = rng.choice(_CORP_TYPES)
    payment_sched = rng.choice(_PAYMENT_SCHEDULES)
    notice_days = rng.choice([15, 30, 45])
    cure_days = rng.choice([10, 15, 30])

    notes = f"""SERVICES AGREEMENT

RECITALS

This Services Agreement ("Agreement") is entered into as of {doc_date}, by and between {vendor.name}, a {vendor_corp} ("Service Provider"), and {buyer.name}, a {buyer_corp} ("Client"). Service Provider and Client are each referred to herein individually as a "Party" and collectively as the "Parties."

WHEREAS, Client desires to engage Service Provider to provide certain professional services; and

WHEREAS, Service Provider desires to provide such services to Client on the terms and conditions set forth herein;

NOW, THEREFORE, in consideration of the mutual covenants and agreements set forth herein, and for other good and valuable consideration, the receipt and sufficiency of which are hereby acknowledged, the Parties agree as follows:


1. SCOPE OF SERVICES

1.1 Services. Service Provider agrees to perform the following professional services for Client: {scope} (the "Services"). Service Provider shall perform the Services in a diligent, professional, and workmanlike manner consistent with industry standards.

1.2 Statement of Work. The Parties may execute one or more Statements of Work ("SOW") referencing this Agreement that set forth additional detail regarding specific deliverables, timelines, acceptance criteria, and project-specific terms. Each SOW, once executed by both Parties, is incorporated herein by reference.

1.3 Change Orders. Any material changes to the scope of Services must be documented in a written change order executed by authorized representatives of both Parties prior to implementation.


2. TERM

2.1 Term. This Agreement shall commence on {doc_date} and continue in full force through {due_date} (the "Initial Term"), unless earlier terminated in accordance with Section 8.

2.2 Renewal. Following the Initial Term, this Agreement shall automatically renew for successive thirty (30)-day periods unless either Party provides written notice of non-renewal at least fifteen (15) days prior to the end of the then-current term.


3. COMPENSATION AND PAYMENT

3.1 Fees. In consideration for the Services, Client agrees to pay Service Provider a total project fee of ${flat_fee:,} (the "Fee"), payable as follows: {payment_sched}.

3.2 Expenses. Client shall reimburse Service Provider for all pre-approved, reasonable, and documented out-of-pocket expenses incurred in connection with the Services, including travel, lodging, and materials. Expenses exceeding $500 individually require prior written authorization from Client.

3.3 Invoicing. Service Provider shall submit invoices to Client at {buyer.email}. Client shall pay all undisputed invoices within thirty (30) days of receipt.

3.4 Late Payment. Invoices not paid within thirty (30) days of the due date shall accrue interest at the rate of one and one-half percent (1.5%) per month, or the maximum rate permitted by applicable law, whichever is less.

3.5 Disputed Invoices. Client shall notify Service Provider in writing of any disputed invoice amounts within ten (10) days of receipt. The Parties agree to work in good faith to resolve disputes within fifteen (15) days of such notification.


4. CONFIDENTIALITY

4.1 Confidential Information. Each Party (as a "Receiving Party") agrees to hold in strict confidence all non-public, proprietary, or confidential information of the other Party (the "Disclosing Party"), including but not limited to business plans, financial data, customer lists, technical specifications, and trade secrets ("Confidential Information").

4.2 Obligations. The Receiving Party shall: (a) use the Disclosing Party's Confidential Information solely for the purposes of this Agreement; (b) protect such information with at least the same degree of care it uses to protect its own confidential information, but no less than reasonable care; and (c) not disclose such information to any third party without the Disclosing Party's prior written consent.

4.3 Exceptions. The obligations in this Section shall not apply to information that: (i) is or becomes publicly available through no fault of the Receiving Party; (ii) was already known to the Receiving Party prior to disclosure; (iii) is independently developed by the Receiving Party; or (iv) is required to be disclosed by law or court order, provided that the Receiving Party provides prompt written notice to the Disclosing Party.

4.4 Survival. The obligations of this Section 4 shall survive termination or expiration of this Agreement for a period of three (3) years.


5. INTELLECTUAL PROPERTY

5.1 Work Product. All deliverables, reports, software, documentation, and other work product created specifically for Client under this Agreement ("Work Product") shall, upon full payment of all amounts due, be considered works made for hire and shall be the exclusive property of Client.

5.2 Service Provider IP. Service Provider retains all right, title, and interest in and to its pre-existing intellectual property, methodologies, tools, and frameworks ("Service Provider IP"). Service Provider hereby grants Client a non-exclusive, perpetual, royalty-free license to use any Service Provider IP incorporated into the Work Product solely in connection with Client's use of the Work Product.

5.3 License to Client Materials. Client grants Service Provider a limited, non-exclusive license to use Client's materials, data, and systems solely as necessary to perform the Services under this Agreement.


6. REPRESENTATIONS AND WARRANTIES

6.1 Mutual Representations. Each Party represents and warrants that: (a) it has full power and authority to enter into this Agreement; (b) this Agreement constitutes a valid and binding obligation enforceable in accordance with its terms; and (c) its execution, delivery, and performance of this Agreement do not violate any applicable law or any agreement to which it is a party.

6.2 Service Provider Warranties. Service Provider represents and warrants that: (a) the Services will be performed by qualified personnel with the skills and experience necessary to fulfill the obligations herein; (b) the Work Product will not knowingly infringe any third-party intellectual property rights; and (c) Service Provider will comply with all applicable laws and regulations in the performance of the Services.


7. LIMITATION OF LIABILITY

7.1 Exclusion of Consequential Damages. IN NO EVENT SHALL EITHER PARTY BE LIABLE TO THE OTHER FOR ANY INDIRECT, INCIDENTAL, SPECIAL, CONSEQUENTIAL, EXEMPLARY, OR PUNITIVE DAMAGES, INCLUDING LOSS OF PROFITS, LOSS OF REVENUE, OR LOSS OF DATA, ARISING OUT OF OR RELATED TO THIS AGREEMENT, EVEN IF SUCH PARTY HAS BEEN ADVISED OF THE POSSIBILITY OF SUCH DAMAGES.

7.2 Liability Cap. EXCEPT FOR BREACHES OF SECTION 4 (CONFIDENTIALITY) OR A PARTY'S INDEMNIFICATION OBLIGATIONS, EACH PARTY'S TOTAL CUMULATIVE LIABILITY ARISING OUT OF OR RELATED TO THIS AGREEMENT SHALL NOT EXCEED THE TOTAL FEES ACTUALLY PAID OR PAYABLE BY CLIENT TO SERVICE PROVIDER DURING THE TWELVE (12) MONTHS PRECEDING THE CLAIM.


8. TERMINATION

8.1 Termination for Convenience. Either Party may terminate this Agreement for any reason upon {notice_days} days' prior written notice to the other Party.

8.2 Termination for Cause. Either Party may terminate this Agreement immediately upon written notice if the other Party: (a) materially breaches this Agreement and fails to cure such breach within {cure_days} days after written notice specifying the breach in reasonable detail; (b) becomes insolvent or makes a general assignment for the benefit of creditors; or (c) has a receiver appointed over a material portion of its assets.

8.3 Effect of Termination. Upon termination, Client shall pay Service Provider for all Services performed and expenses incurred through the effective date of termination. Service Provider shall deliver to Client all Work Product completed or in progress as of the termination date.

8.4 Survival. Sections 3 (outstanding payment obligations), 4 (Confidentiality), 5 (Intellectual Property), 7 (Limitation of Liability), and 9 (General Provisions) shall survive any termination or expiration of this Agreement.


9. GENERAL PROVISIONS

9.1 Governing Law. This Agreement shall be governed by and construed in accordance with the laws of the State of {state}, without regard to its conflict of law provisions.

9.2 Dispute Resolution. The Parties agree to attempt to resolve any dispute through good-faith negotiation for a period of thirty (30) days before pursuing formal legal action. Any unresolved disputes shall be submitted to binding arbitration in accordance with the rules of the American Arbitration Association.

9.3 Independent Contractors. The Parties are independent contractors. Nothing in this Agreement shall be construed to create a partnership, joint venture, agency, employment, or fiduciary relationship between the Parties.

9.4 Non-Solicitation. During the term of this Agreement and for one (1) year thereafter, neither Party shall solicit for employment any employee or contractor of the other Party who was involved in the performance of this Agreement, without prior written consent.

9.5 Notices. All notices required under this Agreement shall be in writing and delivered by email with confirmation of receipt or by overnight courier to the addresses set forth in this Agreement.

9.6 Entire Agreement. This Agreement, together with all executed SOWs, constitutes the entire agreement between the Parties with respect to the subject matter hereof and supersedes all prior negotiations, representations, warranties, and understandings.

9.7 Amendments. This Agreement may not be modified except by a written instrument signed by authorized representatives of both Parties.

9.8 Severability. If any provision of this Agreement is held invalid or unenforceable, the remaining provisions shall continue in full force and effect.

9.9 Waiver. The failure of either Party to enforce any provision of this Agreement shall not constitute a waiver of that Party's right to enforce such provision in the future.

9.10 Counterparts. This Agreement may be executed in one or more counterparts, each of which shall be deemed an original, and all of which together shall constitute one and the same instrument. Electronic signatures shall be deemed valid.


IN WITNESS WHEREOF, the Parties have executed this Services Agreement as of the date first written above.

SERVICE PROVIDER: {vendor.name}

Signature: ___________________________________
Name:
Title:
Date:

CLIENT: {buyer.name}

Signature: ___________________________________
Name:
Title:
Date:"""

    return DocumentData(
        doc_type="contract",
        doc_number=f"AGR-{rng.randint(2024, 2026)}-{rng.randint(10000, 99999)}",
        doc_date=doc_date,
        due_date=due_date,
        buyer=buyer,
        vendor=vendor,
        notes=notes,
    )
