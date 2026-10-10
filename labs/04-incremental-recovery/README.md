# Lab 04 — Can a failed ETL load be safely replayed?

**Standalone:** Python 3.10+, pytest; SQLite is included with Python. Labs 01–03 are not prerequisites.

## Scenario

A fictional orders feed delivers versioned updates in batches. The second batch is interrupted after its first record; operations needs to recover without publishing partial changes, losing new orders, or double-counting revenue. A later batch contains an old correction to an existing order and a newly arrived order.

## Run

```bash
python -m pytest -q tests/test_incremental.py
```

Read [the recovery contract](../../docs/incremental-contract.md) before inspecting the implementation.

## Guided investigation

1. Predict the result of applying batch 01 twice. Compare the snapshot with a single application.
2. Apply batch 02 with a simulated interruption after the first row: explain why *neither* update should remain committed.
3. Retry batch 02 and verify both its update and insert are present.
4. Apply the late-arrival batch; compare identifiers, versions, per-order values and total with `expected-final.csv`.
5. Replay stale data: prove it cannot overwrite newer versions.
6. Submit the same version with different values; explain why it must be rejected rather than quietly ignored.
7. Write a BGSTM quality decision: what evidence proves that a rerun is safe?

## Independent expected final state

| Order | Version | Amount |
| --- | ---: | ---: |
| R-1 | 2 | $12.00 |
| R-2 | 2 | $25.00 |
| R-3 | 1 | $7.00 |
| R-4 | 1 | $4.00 |
| **Total** | | **$48.00** |

## Teaching decision

A green job status alone cannot establish recovery correctness. Compare the committed state against independently authored expected rows, demonstrate stable replay, and verify that interrupted batches leave the committed state unchanged. Review [incident INC-004](../../evidence/defect-examples/INC-004.md) as the example assessment.
