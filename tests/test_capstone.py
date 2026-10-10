from pathlib import Path
from pipeline.capstone import Finding, investigate, read_rows

ROOT = Path(__file__).resolve().parents[1] / "data" / "capstone"


def rows(name):
    return read_rows(ROOT / name)


def test_incident_findings_are_deterministic_and_specific():
    findings = investigate(rows("customers.csv"), rows("orders.csv"),
                           rows("observed-report.csv"), rows("approved-report.csv"))
    assert findings == [
        Finding("DUPLICATE_CUSTOMER", "C-1", "2"),
        Finding("DUPLICATE_REPORT_ROW", "X-1", "2"),
        Finding("AMOUNT_MISMATCH", "X-1", "expected=1000,actual=2000"),
        Finding("AMOUNT_MISMATCH", "X-2", "expected=2000,actual=2500"),
    ]


def test_successful_load_does_not_imply_accurate_business_report():
    observed = rows("observed-report.csv")
    approved = rows("approved-report.csv")
    assert sum(int(x["net_cents"]) for x in observed) == 7500
    assert sum(int(x["net_cents"]) for x in approved) == 6000
    assert len(observed) == 4 and len(approved) == 3


def test_cleaned_output_has_no_incident_findings():
    customers = [{"customer_id": "C-1"}, {"customer_id": "C-2"}]
    approved = rows("approved-report.csv")
    assert investigate(customers, rows("orders.csv"), approved, approved) == []


def test_missing_and_unexpected_records_are_detected():
    approved = rows("approved-report.csv")
    observed = [{"order_id": "X-1", "net_cents": "1000"},
                {"order_id": "EXTRA", "net_cents": "300"}]
    findings = investigate([{"customer_id": "C-1"}, {"customer_id": "C-2"}],
                           rows("orders.csv"), observed, approved)
    codes = {(f.code, f.record) for f in findings}
    assert {("MISSING_ORDER", "X-2"), ("MISSING_ORDER", "X-3"),
            ("UNEXPECTED_ORDER", "EXTRA")} <= codes
