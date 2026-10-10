import duckdb


def load_orders(rows: list[dict], database: str = ":memory:") -> duckdb.DuckDBPyConnection:
    con = duckdb.connect(database)
    con.execute("CREATE OR REPLACE TABLE fact_orders (order_id VARCHAR PRIMARY KEY, customer_id VARCHAR NOT NULL, revenue_cents BIGINT NOT NULL)")
    con.executemany("INSERT INTO fact_orders VALUES (?, ?, ?)",
                    [(row["order_id"], row["customer_id"], row["revenue_cents"]) for row in rows]) if rows else None
    return con
