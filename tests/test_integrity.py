from pathlib import Path
from pipeline.integrity import Finding, check_dataset

ROOT = Path(__file__).resolve().parents[1] / "data" / "integrity"


def inspect(scenario):
    root = ROOT / scenario
    return check_dataset(root / "customers.csv", root / "orders.csv")


def test_clean_baseline():
    assert inspect("clean") == []


def test_additive_schema_change_is_compatible():
    assert inspect("additive") == []


def test_required_column_removal_blocks_validation():
    assert inspect("missing") == [Finding("MISSING_COLUMN", "customers", "country")]


def test_business_integrity_failures_are_precisely_detected():
    assert inspect("broken") == [
        Finding("DUPLICATE_KEY", "customers:3", "C-1"),
        Finding("NULL_REQUIRED", "customers:4", "name"),
        Finding("ORPHAN_FK", "orders:3", "C-404"),
        Finding("DUPLICATE_KEY", "orders:4", "I-2"),
        Finding("INVALID_TYPE", "orders:4", "amount_cents"),
    ]
