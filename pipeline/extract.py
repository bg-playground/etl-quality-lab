import csv
from pathlib import Path


def extract_orders(path: Path) -> list[dict]:
    with Path(path).open(newline="", encoding="utf-8") as stream:
        records = list(csv.DictReader(stream))
    required = {"order_id", "customer_id", "quantity", "unit_price", "status"}
    if not records or not required.issubset(records[0]):
        raise ValueError("Missing required source columns or empty source")
    return records
