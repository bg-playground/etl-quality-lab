# Instructor guide

1. Ask learners to predict whether comparing row counts will be sufficient.
2. Have them run the clean case and explain the expected 3 records and $120.00 total.
3. Introduce the defective fixture *without* initially revealing which field changed.
4. Require a short defect report with expected/actual, impact and candidate source of failure.
5. Compare decisions with `evidence/defect-examples/ETL-005.md`.
6. Discuss which evidence is observed output and which is the reviewed source of truth.

**Assessment rubric (10 points):** identifies discrepancy (2), isolates record (2), explains why row count misses it (2), preserves evidence (2), makes a defensible publication decision (2).

**Common misconception:** automation success means the pipeline was correct. Correct it by distinguishing execution success from independently verified business results.
