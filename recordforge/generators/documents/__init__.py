"""Document generator registry.

Each entry maps the public type key to its build() function.
Keys must match v1 exactly — do not rename.
"""

from recordforge.generators.documents.contract import build as build_contract
from recordforge.generators.documents.intake_form import build as build_intake_form
from recordforge.generators.documents.invoice import build as build_invoice
from recordforge.generators.documents.offer_letter import build as build_offer_letter
from recordforge.generators.documents.purchase_order import build as build_purchase_order
from recordforge.generators.documents.sop import build as build_sop

DOCUMENT_REGISTRY: dict[str, callable] = {
    "invoice": build_invoice,
    "purchase_order": build_purchase_order,
    "intake_form": build_intake_form,
    "sop": build_sop,
    "contract": build_contract,
    "offer_letter": build_offer_letter,
}
