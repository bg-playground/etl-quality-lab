"""Standalone Lab 03 contract checks: schema evolution and referential integrity."""
import csv
from dataclasses import dataclass
from pathlib import Path

CUSTOMER_COLUMNS = frozenset({"customer_id", "name", "country"})
ORDER_COLUMNS = frozenset({"order_id", "customer_id", "amount_cents"})
OPTIONAL_CUSTOMER_COLUMNS = frozenset({"preferred_language"})


@dataclass(frozen=True)
class Finding:
    code: str
    location: str
    detail: str


def read_csv(path: Path) -> tuple[set[str], list[dict[str, str]]]:
    with Path(path).open(newline="", encoding="utf-8") as stream:
        reader = csv.DictReader(stream)
        if reader.fieldnames is None:
            return set(), []
        columns = reader.fieldnames
        if len(columns) != len(set(columns)):
            raise ValueError("duplicate CSV header names")
        return set(columns), list(reader)


def check_dataset(customers_path: Path, orders_path: Path) -> list[Finding]:
    """Return stable findings; unknown additive columns allowed, missing required columns fail."""
    customers_columns, customers = read_csv(customers_path)
    orders_columns, orders = read_csv(orders_path)
    findings = []
    for dataset, actual, required in (
        ("customers", customers_columns, CUSTOMER_COLUMNS),
        ("orders", orders_columns, ORDER_COLUMNS),
    ):
        for column in sorted(required - actual):
            findings.append(Finding("MISSING_COLUMN", dataset, column))
    if findings:
        return findings  # Avoid confusing record checks when required fields are absent.

    known_customers = set()
    for index, row in enumerate(customers, start=2):
        key = (row["customer_id"] or "").strip()
        if not key:
            findings.append(Finding("NULL_KEY", f"customers:{index}", "customer_id"))
        elif key in known_customers:
            findings.append(Finding("DUPLICATE_KEY", f"customers:{index}", key))
        else:
            known_customers.add(key)
        if not (row["name"] or "").strip():
            findings.append(Finding("NULL_REQUIRED", f"customers:{index}", "name"))

    seen_orders = set()
    for index, row in enumerate(orders, start=2):
        key = (row["order_id"] or "").strip()
        customer = (row["customer_id"] or "").strip()
        amount = (row["amount_cents"] or "").strip()
        if not key:
            findings.append(Finding("NULL_KEY", f"orders:{index}", "order_id"))
        elif key in seen_orders:
            findings.append(Finding("DUPLICATE_KEY", f"orders:{index}", key))
        else:
            seen_orders.add(key)
        if not customer:
            findings.append(Finding("NULL_REQUIRED", f"orders:{index}", "customer_id"))
        elif customer not in known_customers:
            findings.append(Finding("ORPHAN_FK", f"orders:{index}", customer))
        try:
            parsed = int(amount)
            if parsed < 0 or amount != str(parsed):
                raise ValueError
        except ValueError:
            findings.append(Finding("INVALID_TYPE", f"orders:{index}", "amount_cents"))
    return findings
