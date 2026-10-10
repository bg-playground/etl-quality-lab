"""Lab 05: evidence-based ETL incident investigation, not a production loader."""
import csv
from dataclasses import dataclass
from pathlib import Path
from pipeline.business_rules import calculate_net_cents, normalize_status


@dataclass(frozen=True)
class Finding:
    code: str
    record: str
    detail: str


def read_rows(path: Path) -> list[dict[str, str]]:
    with Path(path).open(newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        if reader.fieldnames is None or len(reader.fieldnames) != len(set(reader.fieldnames)):
            raise ValueError("invalid CSV header")
        rows = list(reader)
    if any(None in row or any(value is None for value in row.values()) for row in rows):
        raise ValueError("malformed CSV record")
    return rows


def investigate(customers: list[dict], orders: list[dict],
                observed: list[dict], expected: list[dict]) -> list[Finding]:
    """Compare observed report with independent oracle, then collect causal clues."""
    findings = []
    customer_counts = {}
    for row in customers:
        key = row["customer_id"].strip()
        customer_counts[key] = customer_counts.get(key, 0) + 1
    for key, count in sorted(customer_counts.items()):
        if count != 1:
            findings.append(Finding("DUPLICATE_CUSTOMER", key, str(count)))

    expected_by_id = {r["order_id"]: int(r["net_cents"]) for r in expected}
    observed_by_id = {}
    for row in observed:
        key = row["order_id"]
        observed_by_id.setdefault(key, []).append(int(row["net_cents"]))
    for key in sorted(expected_by_id):
        values = observed_by_id.get(key, [])
        if not values:
            findings.append(Finding("MISSING_ORDER", key, "not present in report"))
        elif len(values) > 1:
            findings.append(Finding("DUPLICATE_REPORT_ROW", key, str(len(values))))
        if sum(values) != expected_by_id[key]:
            findings.append(Finding("AMOUNT_MISMATCH", key,
                                    f"expected={expected_by_id[key]},actual={sum(values)}"))
    for key in sorted(observed_by_id.keys() - expected_by_id.keys()):
        findings.append(Finding("UNEXPECTED_ORDER", key, "not in approved oracle"))

    for row in orders:
        if normalize_status(row["status"]) != "PAID":
            continue
        key = row["order_id"]
        computed = calculate_net_cents(row["quantity"], row["unit_price"], row["discount_pct"])
        if key in expected_by_id and computed != expected_by_id[key]:
            findings.append(Finding("SOURCE_CONTRACT_DISCREPANCY", key,
                                    f"source_rule={computed},approved={expected_by_id[key]}"))
    return findings
