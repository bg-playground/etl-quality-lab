# Lab 01 — A green job can produce wrong revenue

**Duration:** 20–30 minutes. **Prerequisites:** Python 3.10+, basic SQL/Python familiarity.

## Question
Can you prove that a successful ETL load has produced correct paid-order revenue?

## Steps
1. Read [the data mapping](../../docs/source-target-mapping.md) and independently calculate the expected total.
2. Run `python -m scripts.check --dataset clean`. Record counts, total and pass/fail result.
3. Run `python -m scripts.check --dataset defective`. The exit code 1 is intentional.
4. Explain why equal row counts did not prove correctness.
5. Inspect `data/defective/orders.csv` and identify the erroneous order, amount and possible downstream impact.
6. Write a release decision with evidence; compare with [the sample answer](../../evidence/sample-test-report/quality-decision.md).
7. Run `python -m pytest -q` to see both the happy path and negative-path detection verified in CI.

## Success criteria
Learner identifies `O-1002`, the **$12.50** overstatement, and states that the affected report should not be published until the discrepancy is resolved or an authorized exception is documented.

## Reflection
Why is a business-owned expected dataset better than reconstructing the expected results with the same transformation logic that you're testing?
