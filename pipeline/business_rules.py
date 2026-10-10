"""Explicit business rules for Lab 02; separate from the frozen Lab 01 pipeline."""
from decimal import Decimal, InvalidOperation, ROUND_HALF_UP

CENT = Decimal("0.01")


def normalize_status(value: str) -> str:
    """Normalize formatting only; never guess an unknown business status."""
    if not isinstance(value, str):
        raise ValueError("status must be text")
    normalized = " ".join(value.strip().upper().split())
    if normalized not in {"PAID", "CANCELLED", "PENDING"}:
        raise ValueError(f"unknown status: {value!r}")
    return normalized


def calculate_net_cents(quantity: str, price: str, discount_pct: str) -> int:
    """Line-level half-up rounding after discount; percentage is 0..100."""
    try:
        qty = int(quantity)
        unit = Decimal(price)
        discount = Decimal(discount_pct)
    except (TypeError, ValueError, InvalidOperation) as exc:
        raise ValueError("invalid monetary input") from exc
    if (qty <= 0 or not unit.is_finite() or unit < 0 or
            not discount.is_finite() or not Decimal(0) <= discount <= Decimal(100)):
        raise ValueError("invalid monetary input")
    result = (Decimal(qty) * unit * (Decimal(1) - discount / Decimal(100)))
    return int(result.quantize(CENT, rounding=ROUND_HALF_UP) * 100)


def transform_sales(rows: list[dict]) -> list[dict]:
    """Generate sale facts; reject duplicate IDs rather than silently dropping data."""
    facts = []
    seen = set()
    for row in rows:
        key = row["order_id"].strip()
        if not key or key in seen:
            raise ValueError(f"missing or duplicate order_id: {key!r}")
        seen.add(key)
        status = normalize_status(row["status"])
        if status != "PAID":
            continue
        facts.append({"order_id": key, "net_cents": calculate_net_cents(
            row["quantity"], row["unit_price"], row["discount_pct"])})
    return facts
