import csv
import sqlite3
from pathlib import Path

import pytest
from pipeline.incremental import apply_batch, initialize, read_batch, snapshot

ROOT = Path(__file__).resolve().parents[1] / "data" / "incremental"


@pytest.fixture
def db():
    con = sqlite3.connect(":memory:")
    initialize(con)
    yield con
    con.close()


def batch(name):
    return read_batch(ROOT / name)


def expected_final():
    with (ROOT / "expected-final.csv").open(newline="", encoding="utf-8") as f:
        return [(r["order_id"], int(r["version"]), r["customer_id"], int(r["amount_cents"]))
                for r in csv.DictReader(f)]


def test_replay_is_idempotent(db):
    rows = batch("batch-01.csv")
    apply_batch(db, rows)
    first = snapshot(db)
    apply_batch(db, rows)
    assert snapshot(db) == first
    assert sum(r[3] for r in first) == 3000


def test_incremental_and_late_arrival_match_independent_oracle(db):
    for name in ("batch-01.csv", "batch-02.csv", "late-arrival.csv"):
        apply_batch(db, batch(name))
    assert snapshot(db) == expected_final()
    assert sum(r[3] for r in snapshot(db)) == 4800
    for name in ("stale-batch.csv", "batch-02.csv", "late-arrival.csv"):
        apply_batch(db, batch(name))
    assert snapshot(db) == expected_final()


def test_partial_failure_rolls_back_every_change(db):
    apply_batch(db, batch("batch-01.csv"))
    before = snapshot(db)
    with pytest.raises(RuntimeError, match="simulated load interruption"):
        apply_batch(db, batch("batch-02.csv"), interrupt_after=1)
    assert snapshot(db) == before
    apply_batch(db, batch("batch-02.csv"))
    assert snapshot(db) == [
        ("R-1", 1, "C-1", 1000),
        ("R-2", 2, "C-2", 2500),
        ("R-3", 1, "C-3", 700),
    ]


def test_same_version_conflict_is_not_silently_accepted(db):
    apply_batch(db, batch("batch-01.csv"))
    apply_batch(db, batch("batch-02.csv"))
    before = snapshot(db)
    with pytest.raises(ValueError, match="conflicting event"):
        apply_batch(db, batch("conflict.csv"))
    assert snapshot(db) == before


def test_bad_batch_cannot_partially_write(db, tmp_path):
    invalid = tmp_path / "invalid.csv"
    invalid.write_text(
        "order_id,version,customer_id,amount_cents\n"
        "X-1,1,C-1,100\nX-1,2,C-1,200\n", encoding="utf-8")
    with pytest.raises(ValueError, match="duplicate key"):
        read_batch(invalid)
    assert snapshot(db) == []
