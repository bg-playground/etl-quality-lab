from decimal import Decimal, InvalidOperation, ROUND_HALF_UP

CENT = Decimal("0.01")


def transform_orders(rows: list[dict]) -> list[dict]:
    """Contract: include PAID only; revenue = quantity * price; never deduplicate silently."""
    output = []
    seen = set()
    for row in rows:
        order_id = row["order_id"].strip()
        if not order_id or order_id in seen:
            raise ValueError(f"Missing/duplicate order_id: {order_id!r}")
        seen.add(order_id)
        try:
            quantity = int(row["quantity"])
            price = Decimal(row["unit_price"])
        except (ValueError, InvalidOperation) as exc:
            raise ValueError(f"Invalid quantity or price for {order_id}") from exc
        if quantity <= 0 or not price.is_finite() or price < 0:
            raise ValueError(f"Invalid quantity or price for {order_id}")
        if row["status"].strip().upper() != "PAID":
            continue
        revenue = (quantity * price).quantize(CENT, rounding=ROUND_HALF_UP)
        output.append({"order_id": order_id, "customer_id": row["customer_id"].strip(),
                       "revenue_cents": int(revenue * 100)})
    return output
