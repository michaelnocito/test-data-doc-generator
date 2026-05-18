"""Core dataclasses: Party, LineItem, DocumentData, GeneratedDoc."""

from dataclasses import dataclass, field
from decimal import Decimal
from pathlib import Path


@dataclass
class Party:
    name: str
    address1: str
    address2: str
    phone: str
    email: str


@dataclass
class LineItem:
    description: str
    quantity: int
    unit_price: Decimal

    @property
    def total(self) -> Decimal:
        """Computed line total — quantity × unit_price."""
        return Decimal(self.quantity) * self.unit_price


@dataclass
class DocumentData:
    doc_type: str
    doc_number: str
    doc_date: str
    due_date: str | None
    buyer: Party
    vendor: Party
    line_items: list[LineItem] = field(default_factory=list)
    notes: str = ""

    @property
    def subtotal(self) -> Decimal:
        """Sum of all line item totals."""
        return sum(item.total for item in self.line_items)

    @property
    def tax(self) -> Decimal:
        """8% tax on subtotal, rounded to cents."""
        return (self.subtotal * Decimal("0.08")).quantize(Decimal("0.01"))

    @property
    def total_due(self) -> Decimal:
        """subtotal + tax."""
        return self.subtotal + self.tax


@dataclass
class GeneratedDoc:
    path: Path
    doc_type: str
    format: str
