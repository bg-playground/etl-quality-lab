"""Controlled faulty implementation for instructional use only.

Do not import into the production-like Lab 01 pipeline.
"""
from decimal import Decimal
from pipeline.business_rules import normalize_status


def faulty_transform_sales(rows: list[dict]) -> list[dict]:
    """BUG: applies integer truncation before cents, losing fractional cents."""
    output = []
    for row in rows:
        if normalize_status(row["status"]) != "PAID":
            continue
        amount = int(Decimal(row["quantity"]) * Decimal(row["unit_price"]) *
                     (1 - Decimal(row["discount_pct"]) / 100))
        output.append({"order_id": row["order_id"].strip(), "net_cents": amount * 100})
    return output
