# Capstone acceptance contract — CAP-005

**CAP-001 — Business truth:** Paid-order net sales are calculated with the approved discount rules (Lab 02). The independently authored approved report contains X-1 = 1000 cents, X-2 = 2000 cents, and X-3 = 3000 cents; **total = 6000 cents**.

**CAP-002 — Identity:** Each paid order must appear exactly once in the curated reporting result. Duplicate customer rows must not multiply fact records or totals during a join.

**CAP-003 — Reconciliation:** Check row count, per-order identity, per-order amount and aggregate totals. A passing warehouse load alone is insufficient.

**CAP-004 — Explanation:** Distinguish observations from inferences: the dimension has duplicate customer ID C-1 and the report repeats X-1; a non-unique join is a plausible cause, but this fixture does not include the original faulty SQL. The report includes undiscounted X-2, consistent with failure to apply its 20% discount.

**CAP-005 — Release gate:** Hold the affected report while discrepant; require upstream dimension cleanup or enforced uniqueness, corrected pricing transformation, rerun and independent reconciliation evidence.

**Out of scope:** Full forensic provenance for the missing original ETL SQL, external lineage systems, production revenue materiality policy, and actual deployment approval. The capstone is synthetic and instructional.
