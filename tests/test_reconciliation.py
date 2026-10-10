from pathlib import Path

from pipeline.extract import extract_orders
from pipeline.load import load_orders
from pipeline.quality import reconcile, run_quality_check
from pipeline.transform import transform_orders

ROOT = Path(__file__).resolve().parents[1]
EXPECTED = ROOT / "data/expected/fact_orders.csv"


def test_clean_pipeline_reconciles():
    result = run_quality_check(ROOT / "data/clean/orders.csv", EXPECTED)
    assert result.passed
    assert result.expected_count == result.actual_count == 3
    assert result.expected_cents == result.actual_cents == 12000


def test_seeded_defect_is_detected_without_making_ci_red():
    result = run_quality_check(ROOT / "data/defective/orders.csv", EXPECTED)
    assert not result.passed
    assert result.mismatched_ids == ("O-1002",)
    assert result.actual_cents - result.expected_cents == 1250
    assert result.expected_count == result.actual_count


def test_cancelled_orders_are_excluded():
    data = transform_orders(extract_orders(ROOT / "data/clean/orders.csv"))
    assert "O-1003" not in {row["order_id"] for row in data}


def test_duplicate_source_keys_are_rejected():
    data = extract_orders(ROOT / "data/clean/orders.csv")
    import pytest
    with pytest.raises(ValueError, match="duplicate"):
        transform_orders(data + [data[0]])


def test_target_has_expected_schema_and_no_duplicate_keys():
    con = load_orders(transform_orders(extract_orders(ROOT / "data/clean/orders.csv")))
    try:
        assert con.execute("SELECT COUNT(*) - COUNT(DISTINCT order_id) FROM fact_orders").fetchone()[0] == 0
        assert con.execute("SELECT COUNT(*) FROM fact_orders WHERE customer_id IS NULL").fetchone()[0] == 0
    finally:
        con.close()


def test_reconcile_detects_missing_unexpected_and_value_errors():
    expected = [{"order_id": "A", "revenue_cents": 100}, {"order_id": "B", "revenue_cents": 200}]
    actual = [{"order_id": "A", "revenue_cents": 120}, {"order_id": "C", "revenue_cents": 180}]
    outcome = reconcile(expected, actual)
    assert outcome.missing_ids == ("B",)
    assert outcome.unexpected_ids == ("C",)
    assert outcome.mismatched_ids == ("A",)
    assert not outcome.passed
