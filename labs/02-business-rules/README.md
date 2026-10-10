# Lab 02 — Correct code, wrong business result?

**Standalone lab:** Requires Python 3.10+, pytest; no DuckDB or Lab 01 completion required.

## Business contract
For each uniquely keyed order, normalize known status labels by trimming whitespace and uppercasing; include **PAID** only. Calculate net revenue as `quantity × unit_price × (1 − discount_pct / 100)`, and round **once per line** to cents using `ROUND_HALF_UP`. Reject invalid quantity, negative prices, discounts outside 0–100, non-finite monetary inputs, unknown statuses and duplicate keys.

The approved synthetic source-to-target mapping is [documented here](../../docs/transformation-contract.md). The expected result is independently specified in `data/transformation/expected.csv`, not generated using the code under test.

## Exercise
1. Read the contract and calculate each expected paid-order amount by hand.
2. Run `python -m pytest -q tests/test_business_rules.py`.
3. Compare `pipeline/business_rules.py` with **deliberately faulty** `pipeline/transform_lab.py`.
4. Identify which rule the faulty algorithm violates and which rows are affected.
5. Record expected and observed amounts and decide whether reporting may be published.
6. Compare your diagnosis with [TR-002](../../evidence/defect-examples/TR-002.md).

## Observed fixture expectations

| Check | Approved value | Faulty demonstration |
| --- | ---: | ---: |
| Included sales | 3 | 3 |
| Total net | $48.66 | $47.00 |
| T-2001 | $17.99 | $17.00 |
| T-2002 | $6.67 | $6.00 |
| T-2004 | $24.00 | $24.00 |

The buggy implementation truncates dollar amounts before converting to cents. Test assertions *expect to detect* this mistake; their success leaves CI green. Do not use the buggy implementation for actual ETL processing.

## BGSTM reflection
- **Planning:** Which reporting decisions are exposed to rounding errors?
- **Test Case Development:** Why test halfway-cent and discount cases?
- **Environment Preparation:** Why should approved expected results be independent of code?
- **Execution:** Does green CI prove the buggy function is safe to publish?
- **Results Analysis:** What business rule is violated and where?
- **Results Reporting:** What evidence justifies holding the affected report?
