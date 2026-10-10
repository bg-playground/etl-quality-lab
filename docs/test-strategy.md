# BGSTM test strategy: v0.1

## Planning
**Business risk:** the warehouse can report incorrect revenue even when extraction and loading succeed. The reporting data must not be published until material discrepancies have been investigated.

## Test conditions
- Paid-only inclusion and cancelled-order exclusion.
- One warehouse record per unique source order ID; fail on duplicate source keys.
- Deterministic decimal calculation, stored as integer cents.
- Source-to-target record identity, count, per-order revenue, and grand-total reconciliation.
- Detect a deliberately seeded source value mismatch.

## Environment preparation
Use the committed synthetic fixtures in `data/clean`, `data/defective`, and `data/expected`. No network, credentials, or external database required after dependency installation.

## Execution
Run `python -m pytest -q` for automated acceptance; use `python -m scripts.check --dataset defective` to see failure evidence. The intentionally failing demo command is not a failing unit test.

## Results analysis and reporting
A pass requires agreement on identifiers **and** amounts. If a discrepancy occurs, retain actual and expected totals, affected IDs, and the source/contract context. Hold affected publishing until triaged; do not silently edit the target to make the test pass.

## Explicit non-goals
Performance benchmarking, orchestration, production-grade governance, and live customer integrations are outside v0.1.
