"""Independent expectations; deliberate broken algorithm must be detected."""
import csv
from pathlib import Path

import pytest

from pipeline.business_rules import calculate_net_cents, normalize_status, transform_sales
from pipeline.transform_lab import faulty_transform_sales

ROOT = Path(__file__).resolve().parents[1] / "data" / "transformation"


def fixture_rows(filename):
    with (ROOT / filename).open(newline="", encoding="utf-8") as stream:
        return list(csv.DictReader(stream))


def test_business_owned_expected_values():
    rows = fixture_rows("orders.csv")
    expected = [{"order_id": r["order_id"], "net_cents": int(r["net_cents"])}
                for r in fixture_rows("expected.csv")]
    assert transform_sales(rows) == expected
    assert sum(r["net_cents"] for r in expected) == 4866


@pytest.mark.parametrize(("qty", "price", "discount", "expected"), [
    ("1", "19.99", "10", 1799),
    ("2", "3.335", "0", 667),
    ("3", "10.00", "20", 2400),
    ("1", "0.015", "0", 2),
])
def test_money_rounds_only_at_line_total(qty, price, discount, expected):
    assert calculate_net_cents(qty, price, discount) == expected


@pytest.mark.parametrize("bad", [
    ("0", "10", "0"), ("1", "-1", "0"), ("1", "10", "-1"),
    ("1", "10", "101"), ("1", "NaN", "0"), ("1", "Infinity", "0"),
    ("x", "10", "0"), ("1", "ten", "0"),
])
def test_invalid_monetary_inputs_fail_closed(bad):
    with pytest.raises(ValueError):
        calculate_net_cents(*bad)


def test_normalization_is_format_only():
    assert normalize_status("  paid  ") == "PAID"
    assert normalize_status("PENDING") == "PENDING"
    with pytest.raises(ValueError, match="unknown status"):
        normalize_status("paid-ish")


def test_unknown_status_cannot_be_silently_included():
    rows = fixture_rows("orders.csv")
    rows[0]["status"] = "AUTHORIZED"
    with pytest.raises(ValueError, match="unknown status"):
        transform_sales(rows)


def test_duplicate_keys_are_rejected():
    rows = fixture_rows("orders.csv")
    with pytest.raises(ValueError, match="duplicate"):
        transform_sales(rows + [rows[0]])


def test_faulty_implementation_detected_without_red_ci():
    rows = fixture_rows("orders.csv")
    expected = {r["order_id"]: int(r["net_cents"]) for r in fixture_rows("expected.csv")}
    actual = {r["order_id"]: r["net_cents"] for r in faulty_transform_sales(rows)}
    mismatches = {key: (expected[key], actual[key]) for key in expected
                  if expected[key] != actual[key]}
    assert mismatches == {"T-2001": (1799, 1700), "T-2002": (667, 600)}
    assert sum(actual.values()) == 4700
    assert sum(expected.values()) == 4866
