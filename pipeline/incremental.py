"""Lab 04: atomic, versioned incremental ETL into SQLite.

Standalone from prior labs. Decimal money is stored as integer cents.
"""
import csv
import sqlite3
from pathlib import Path


SCHEMA = """
CREATE TABLE IF NOT EXISTS orders (
    order_id TEXT PRIMARY KEY,
    version INTEGER NOT NULL CHECK(version >= 1),
    customer_id TEXT NOT NULL,
    amount_cents INTEGER NOT NULL CHECK(amount_cents >= 0)
)
"""


def read_batch(path: Path) -> list[tuple[str, int, str, int]]:
    with Path(path).open(newline="", encoding="utf-8") as stream:
        reader = csv.DictReader(stream)
        expected = {"order_id", "version", "customer_id", "amount_cents"}
        if reader.fieldnames is None or set(reader.fieldnames) != expected:
            raise ValueError("invalid batch schema")
        rows = []
        seen = set()
        for row in reader:
            if None in row or any(value is None for value in row.values()):
                raise ValueError("malformed CSV row")
            key, customer = row["order_id"].strip(), row["customer_id"].strip()
            if not key or not customer or key in seen:
                raise ValueError("missing or duplicate key")
            seen.add(key)
            version_text, amount_text = row["version"], row["amount_cents"]
            if (not version_text.isdecimal() or str(int(version_text)) != version_text
                    or not amount_text.isdecimal() or str(int(amount_text)) != amount_text):
                raise ValueError("version and amount must be canonical nonnegative integers")
            version, amount = int(version_text), int(amount_text)
            if version < 1:
                raise ValueError("version must be positive")
            rows.append((key, version, customer, amount))
    return rows


def apply_batch(con: sqlite3.Connection, rows: list[tuple[str, int, str, int]],
                interrupt_after: int | None = None) -> None:
    """One transaction per batch. Equal versions must be identical; older events ignored."""
    if con.in_transaction:
        raise RuntimeError("unexpected open transaction")
    try:
        con.execute("BEGIN IMMEDIATE")
        for i, (key, version, customer, amount) in enumerate(rows, start=1):
            current = con.execute(
                "SELECT version, customer_id, amount_cents FROM orders WHERE order_id=?",
                (key,)).fetchone()
            if current is None:
                con.execute("INSERT INTO orders VALUES (?, ?, ?, ?)",
                            (key, version, customer, amount))
            elif version > current[0]:
                con.execute(
                    "UPDATE orders SET version=?, customer_id=?, amount_cents=? WHERE order_id=?",
                    (version, customer, amount, key))
            elif version == current[0] and (customer, amount) != current[1:]:
                raise ValueError(f"conflicting event at same version: {key}")
            if interrupt_after is not None and i == interrupt_after:
                raise RuntimeError("simulated load interruption")
        con.commit()
    except BaseException:
        con.rollback()
        raise


def snapshot(con: sqlite3.Connection) -> list[tuple[str, int, str, int]]:
    return con.execute(
        "SELECT order_id, version, customer_id, amount_cents FROM orders ORDER BY order_id"
    ).fetchall()


def initialize(con: sqlite3.Connection) -> None:
    con.execute(SCHEMA)
    con.commit()
