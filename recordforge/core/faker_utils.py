"""Random data helpers and expanded word lists.

All rand_* functions accept an rng parameter — never use module-level
random globals.
"""

import random
import secrets
from datetime import date, timedelta
from decimal import Decimal
from typing import Literal

from recordforge.core.models import LineItem, Party

# --- Word lists (40+ entries each) ---

FIRST_WORDS: list[str] = [
    "Apex", "Horizon", "Meridian", "Nexus", "Pinnacle", "Summit", "Catalyst",
    "Elevate", "Vantage", "Clarity", "Arcadia", "Bridgepoint", "Crestline",
    "Delphi", "Embark", "Frontier", "Granite", "Harbor", "Ironstone", "Juniper",
    "Keystone", "Lakeview", "Monarch", "Navigate", "Oakridge", "Paragon",
    "Quantum", "Ridgeline", "Silverstone", "Trident", "Uplift", "Vertex",
    "Waypoint", "Xcalibur", "Yellowstone", "Zenith", "Alliant", "Bridgespan",
    "Clearpath", "Datapoint",
]

INDUSTRY_WORDS: list[str] = [
    "Clinical", "Health", "Analytics", "Solutions", "Systems", "Informatics",
    "Care", "Data", "Consulting", "Technologies", "Advisors", "Capital",
    "Dynamics", "Enterprises", "Financial", "Global", "Holdings", "Innovations",
    "Logistics", "Management", "Networks", "Operations", "Partners", "Research",
    "Services", "Strategies", "Supply", "Talent", "Transformation", "Ventures",
    "Workflow", "Intelligence", "Procurement", "Infrastructure", "Compliance",
    "Assurance", "Integration", "Performance", "Excellence", "Digital",
]

CORP_SUFFIXES: list[str] = [
    "LLC", "Inc.", "Group", "Partners", "Associates", "Corp.", "Co.", "Ltd.",
    "Enterprises", "Advisors",
]

STREETS: list[str] = [
    "Oak", "Maple", "Commerce", "Innovation", "Enterprise", "Corporate", "Tech",
    "Riverside", "Lakeside", "Parkview", "Summit", "Hillcrest", "Meadow",
    "Cedar", "Birch", "Elmwood", "Pinecrest", "Willow", "Springfield",
    "Clearwater", "Stonegate", "Ironwood", "Bridgewater", "Foxcroft",
    "Greenfield", "Harborview", "Kingsway", "Lakewood", "Northgate",
    "Orchard", "Primrose", "Quarry", "Ridgeview", "Sunridge", "Timberline",
    "Union", "Valley", "Westgate", "Yorktown",
]

STREET_TYPES: list[str] = [
    "Blvd", "Dr", "Ave", "Way", "Pkwy", "St", "Ct", "Ln", "Pl", "Rd",
]

CITIES: list[tuple[str, str]] = [
    ("Austin", "TX"), ("Nashville", "TN"), ("Atlanta", "GA"), ("Denver", "CO"),
    ("Charlotte", "NC"), ("Phoenix", "AZ"), ("Raleigh", "NC"), ("Tampa", "FL"),
    ("Columbus", "OH"), ("Indianapolis", "IN"), ("Kansas City", "MO"),
    ("Louisville", "KY"), ("Memphis", "TN"), ("Oklahoma City", "OK"),
    ("Portland", "OR"), ("Richmond", "VA"), ("Salt Lake City", "UT"),
    ("San Antonio", "TX"), ("Tucson", "AZ"), ("Tulsa", "OK"),
    ("Birmingham", "AL"), ("Boise", "ID"), ("Cincinnati", "OH"),
    ("Cleveland", "OH"), ("Des Moines", "IA"), ("El Paso", "TX"),
    ("Fort Worth", "TX"), ("Fresno", "CA"), ("Hartford", "CT"),
    ("Honolulu", "HI"), ("Jacksonville", "FL"), ("Las Vegas", "NV"),
    ("Little Rock", "AR"), ("Milwaukee", "WI"), ("Minneapolis", "MN"),
    ("New Orleans", "LA"), ("Omaha", "NE"), ("Pittsburgh", "PA"),
    ("Sacramento", "CA"), ("St. Louis", "MO"),
]

FIRST_NAMES: list[str] = [
    "Mia", "Liam", "Noah", "Emma", "Olivia", "Ava", "Ethan", "Lucas", "James",
    "Sophia", "Aiden", "Isabella", "Mason", "Aria", "Logan", "Ella", "Jackson",
    "Scarlett", "Sebastian", "Grace", "Mateo", "Chloe", "Jack", "Penelope",
    "Owen", "Layla", "Theodore", "Riley", "Asher", "Nora", "Henry", "Zoey",
    "Alexander", "Lily", "Daniel", "Eleanor", "Michael", "Hannah", "Benjamin",
    "Lillian", "Elijah", "Addison", "Samuel", "Aubrey", "David", "Ellie",
    "Joseph", "Stella", "Carter", "Natalie", "Jaylen", "Amara", "Destiny",
    "Marcus", "Priya", "Aiko", "Rafael", "Fatima", "Kenji", "Aaliyah",
]

LAST_NAMES: list[str] = [
    "Carter", "Hayes", "Brooks", "Foster", "Morgan", "Bennett", "Turner",
    "Parker", "Bailey", "Reed", "Coleman", "Jenkins", "Perry", "Powell",
    "Long", "Patterson", "Hughes", "Flores", "Washington", "Butler",
    "Simmons", "Foster", "Gonzalez", "Bryant", "Alexander", "Russell",
    "Griffin", "Diaz", "Myers", "Ford", "Hamilton", "Graham",
    "Sullivan", "Wallace", "Woods", "Cole", "West", "Jordan", "Owens",
    "Reynolds", "Fisher", "Ellis", "Harrison", "Gibson", "Mcdonald",
    "Cruz", "Marshall", "Ortiz", "Gomez", "Murray", "Freeman", "Wells",
    "Webb", "Simpson", "Stevens", "Tucker", "Porter", "Hunter", "Hicks",
]

EMAIL_DOMAINS: list[str] = [
    "acmecorp.io", "bridgepoint.co", "crestlinegroup.net", "dataworks.biz",
    "elevateops.co", "frontiertech.io", "graniteadvisors.com", "harborgroup.net",
    "ironbridge.biz", "junipersystems.co", "keystonellc.io", "lakewoodco.net",
    "monarchtech.biz", "navigatecorp.co", "oakridgeinc.io", "paragonworks.net",
    "quantumgrp.biz", "ridgelineops.co", "silverstoneco.io", "tridentgroup.net",
]

PRODUCTS: list[str] = [
    "Laptop Docking Station", "24-inch Monitor", "Wireless Keyboard",
    "USB-C Hub", "Ergonomic Chair", "Standing Desk", "Webcam HD 1080p",
    "Network Switch 24-Port", "Uninterruptible Power Supply", "Label Printer",
    "Barcode Scanner", "Thermal Printer", "External SSD 1TB", "RAM Module 16GB",
    "Cat6 Ethernet Cable 50ft", "Patch Panel 24-Port", "Rack Mount Cabinet",
    "Surge Protector 8-Outlet", "Cable Management Kit", "KVM Switch 4-Port",
    "Laser Printer Toner Cartridge", "Shredder Cross-Cut", "Projector 3500 Lumens",
    "Whiteboard 4x6ft", "Conference Phone", "Headset Noise-Cancelling",
    "Tablet 10-inch", "Wireless Access Point", "Firewall Appliance",
    "Server RAM 32GB",
]

SERVICES: list[str] = [
    "Implementation Services", "Configuration Support", "Training Session",
    "Project Management", "System Integration", "Data Migration",
    "Security Audit", "Compliance Review", "Custom Development",
    "API Integration", "Workflow Automation", "Technical Documentation",
    "Infrastructure Assessment", "Disaster Recovery Planning",
    "Performance Optimization", "Staff Augmentation", "Onboarding Services",
    "Quality Assurance Review", "Change Management Consulting",
    "Business Process Analysis", "Cloud Architecture Review",
    "Database Optimization", "Network Assessment", "Vendor Management",
    "Contract Negotiation Support", "Executive Briefing", "Roadmap Planning",
    "Stakeholder Workshop", "Post-Go-Live Support", "Annual Maintenance",
]

_EMAIL_PREFIXES = ["info", "contact", "hello", "admin", "support", "billing"]


# --- Helpers ---

def sanitize_filename(s: str) -> str:
    """Preserve v1 sanitize_filename behavior exactly."""
    s = "".join(ch if ch.isalnum() or ch in "._-" else "_" for ch in str(s).strip())
    return s[:100] or "output"


def rand_company(rng: random.Random) -> str:
    """Generate a random fictional company name."""
    return f"{rng.choice(FIRST_WORDS)} {rng.choice(INDUSTRY_WORDS)} {rng.choice(CORP_SUFFIXES)}"


def rand_person(rng: random.Random) -> str:
    """Generate a random fictional full name."""
    return f"{rng.choice(FIRST_NAMES)} {rng.choice(LAST_NAMES)}"


def rand_phone(rng: random.Random) -> str:
    """Generate a random US phone number string."""
    return f"({rng.randint(200, 989)}) {rng.randint(200, 989)}-{rng.randint(1000, 9999)}"


def rand_address(rng: random.Random) -> tuple[str, str]:
    """Return (street_line, city_state_zip) tuple."""
    city, state = rng.choice(CITIES)
    street = f"{rng.randint(100, 9999)} {rng.choice(STREETS)} {rng.choice(STREET_TYPES)}"
    return street, f"{city}, {state} {rng.randint(10000, 99999)}"


def rand_email(rng: random.Random, company_name: str) -> str:
    """Derive a plausible email address from a company name."""
    slug = "".join(ch.lower() for ch in company_name.split()[0] if ch.isalnum())
    domain = rng.choice(EMAIL_DOMAINS)
    prefix = rng.choice(_EMAIL_PREFIXES + [slug])
    return f"{prefix}@{domain}"


def rand_party(rng: random.Random) -> Party:
    """Build a fully populated Party instance."""
    company = rand_company(rng)
    a1, a2 = rand_address(rng)
    return Party(
        name=company,
        address1=a1,
        address2=a2,
        phone=rand_phone(rng),
        email=rand_email(rng, company),
    )


def rand_date_pair(rng: random.Random) -> tuple[str, str]:
    """Return (doc_date, due_date) strings, due_date always after doc_date."""
    doc_date = date.today() + timedelta(days=rng.randint(-60, 0))
    due_date = doc_date + timedelta(days=rng.randint(15, 45))
    return doc_date.strftime("%B %d, %Y"), due_date.strftime("%B %d, %Y")


def rand_line_items(
    rng: random.Random,
    kind: Literal["products", "services"],
    count: int = 3,
) -> list[LineItem]:
    """Generate realistic LineItem instances.

    Products: unit price $15–$500, quantity 1–50.
    Services: unit price $500–$8000, quantity 1–5.
    """
    pool = PRODUCTS if kind == "products" else SERVICES
    chosen = rng.sample(pool, min(count, len(pool)))
    items = []
    for desc in chosen:
        if kind == "products":
            qty = rng.randint(1, 50)
            unit_price = Decimal(rng.randint(15, 500))
        else:
            qty = rng.randint(1, 5)
            unit_price = Decimal(rng.randint(500, 8000))
        items.append(LineItem(description=desc, quantity=qty, unit_price=unit_price))
    return items
