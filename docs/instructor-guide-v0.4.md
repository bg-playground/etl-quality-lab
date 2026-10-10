# Instructor guide — Lab 04

Ask learners whether a successful retry proves that the interrupted batch left no partial changes. Have learners describe how they would falsify that assumption, then run the rollback test.

**Assessment (10 points):** demonstrates unchanged replay (2), proves atomic rollback (2), validates late-arrival final state (2), recognizes stale-version protection and same-version conflict (2), makes traceable publication decision (2).

**Key teaching distinction:** idempotency concerns the resulting state, not the absence of re-execution. A job can re-run and still be safe; an apparently successful job can leave incorrect data. Distinguish the controlled transaction-level guarantee from end-to-end exactly-once processing.
