# Lab 03 — Schema evolution and data integrity

**Standalone lab:** You can complete this without completing Labs 01 or 02.

## Scenario

A fictional order reporting pipeline receives customer and order CSV extracts. The publisher says the nightly job finished, but downstream quality requirements still have to be verified. One upstream change adds an optional customer field; another removes a required column. Separately, an extract has duplicate customers, an orphaned order, a blank customer name, a duplicate order, and malformed money data.

## Contract

Read the [independent data contract](../../docs/integrity-contract.md). Learn why a compatible additive field is acceptable while an unexpected removal of a required field is not.

## Steps

1. Examine the four fixture directories in `data/integrity/` and predict which should pass.
2. Run `python -m pytest -q tests/test_integrity.py`.
3. Compare the expected explicit finding codes in the tests with `pipeline/integrity.py`.
4. Explain why adding `preferred_language` is compatible in this lab.
5. Explain why the missing `country` field fails before row validation.
6. Triage the five reported findings from the broken fixture, identify possible business impact, and propose a publication decision.
7. Compare your report with [INT-003](../../evidence/defect-examples/INT-003.md).

## Expected outcomes

| Fixture | Expected result | Quality decision |
| --- | --- | --- |
| `clean` | No findings | Eligible for this integrity gate |
| `additive` | No findings | Compatible under the agreed policy |
| `missing` | MISSING_COLUMN: customers.country | Hold |
| `broken` | Duplicate keys, null name, orphan FK, invalid type | Hold |

**Important:** A passing schema and integrity check establishes only that these rules hold; it does not independently establish all downstream business correctness.

## BGSTM exercise

Document: business risk (Planning); rule-specific test conditions (Test Case Development); controlled fixtures (Environment Preparation); test output (Execution); precise discrepancy assessment (Results Analysis); and supported publication recommendation (Results Reporting).
