# Lab 05 — The job was green. The revenue report was wrong.

**Standalone capstone · 30–45 minutes · Python and pytest**

## Incident brief

A fictional retail company's overnight ETL run completed without reporting operational failure. The reporting team sees **$75.00** of revenue, while the independently approved business expectation is **$60.00**. Operations asks whether the report can be published.

Your role: QA investigator. Do **not** assume that job completion confirms correctness. Determine *which records*, *which rules*, and *which upstream conditions* explain the $15.00 overstatement.

## Evidence provided

- `data/capstone/customers.csv` — customer dimension extracted before the load
- `data/capstone/orders.csv` — sales events and discount rules
- `data/capstone/observed-report.csv` — warehouse/reporting observation
- `data/capstone/approved-report.csv` — independently authored expected result
- `pipeline/capstone.py` — explicit investigation checks, **not** the original faulty ETL source

## Your investigation

1. Write a 1-paragraph risk statement and propose release criteria.
2. Inspect the four CSV inputs before looking at the sample answer.
3. Compare keys, row counts, discounted amounts, and totals. Identify separate failure mechanisms.
4. Run `python -m pytest -q tests/test_capstone.py`. Interpret the assertion evidence.
5. Determine whether duplicate customer matches could inflate sales on a one-to-many join.
6. Determine whether the discount was applied to each paid order.
7. Write a defect report distinguishing *observed evidence*, *likely explanation*, and *unproven implementation detail*. No actual faulty join implementation is present.
8. Make a release decision and specify remediation and rerun evidence.

Compare with [the completed model investigation](../../evidence/defect-examples/CAP-005.md).

## BGSTM six-phase evidence challenge

| Phase | Deliverable |
| --- | --- |
| Planning | Materiality, source authority, release risks |
| Test Case Development | Expected/actual rules and cases |
| Environment Preparation | Reproducible synthetic inputs and independent oracle |
| Execution | Automated assertions and observed report |
| Results Analysis | Separate duplicate-join and discount failures |
| Results Reporting | Hold/release judgment and corrective verification |

**Success criteria:** Find both X-1 duplication and X-2 discount discrepancies, explain the $15.00 difference, and make a defensible hold-and-retest decision.
