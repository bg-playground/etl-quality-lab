from dataclasses import dataclass

from pipeline.extract import extract_orders
from pipeline.transform import transform_orders
from pipeline.load import load_orders


@dataclass(frozen=True)
class Reconciliation:
    expected_count: int
    actual_count: int
    missing_ids: tuple[str, ...]
    unexpected_ids: tuple[str, ...]
    mismatched_ids: tuple[str, ...]
    expected_cents: int
    actual_cents: int

    @property
    def passed(self) -> bool:
        return (not self.missing_ids and not self.unexpected_ids and not self.mismatched_ids
                and self.expected_count == self.actual_count and self.expected_cents == self.actual_cents)


def reconcile(expected: list[dict], actual: list[dict]) -> Reconciliation:
    left = {r["order_id"]: r["revenue_cents"] for r in expected}
    right = {r["order_id"]: r["revenue_cents"] for r in actual}
    return Reconciliation(
        len(expected), len(actual), tuple(sorted(left.keys() - right.keys())),
        tuple(sorted(right.keys() - left.keys())),
        tuple(sorted(k for k in left.keys() & right.keys() if left[k] != right[k])),
        sum(left.values()), sum(right.values()))


def run_quality_check(source, expected):
    source_rows = extract_orders(source)
    transformed = transform_orders(source_rows)
    con = load_orders(transformed)
    try:
        target = [{"order_id": order_id, "revenue_cents": cents} for order_id, cents in
                  con.execute("SELECT order_id, revenue_cents FROM fact_orders").fetchall()]
    finally:
        con.close()
    import csv
    with open(expected, newline="", encoding="utf-8") as stream:
        expected_rows = [{"order_id": r["order_id"], "revenue_cents": int(r["revenue_cents"])}
                         for r in csv.DictReader(stream)]
    return reconcile(expected_rows, target)
