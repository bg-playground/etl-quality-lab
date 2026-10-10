# Incremental-load and recovery contract — v0.4

**INC-001 Replay safety:** Given the same event key, version, and values, replay must not change the target. `order_id` is the unique business key.

**INC-002 Version ordering:** For a key, only strictly newer positive integer versions update a record. Older versions do not overwrite current rows. A repeated version with conflicting customer/amount data is rejected rather than silently accepted.

**INC-003 Atomicity:** All rows in one batch commit together. A simulated interruption or validation failure leaves the previously committed target unchanged.

**INC-004 Late arrivals:** A new key can appear after earlier batches; a late update with a higher version changes an existing key even if it arrives in a subsequent batch.

**INC-005 Independent reconciliation:** Final identity/version/customer/amount must match `data/incremental/expected-final.csv`, totaling 4,800 cents. The expected fixture must never be derived from the system under test.

**INC-006 Input contract:** Batch headers must be precisely `order_id,version,customer_id,amount_cents`. Keys and customer IDs cannot be blank; keys cannot repeat within a batch; versions are canonical positive integers and amounts canonical nonnegative integer cents. Read and validate the full batch before any write.

### Boundaries

This is a single-process SQLite teaching model; it does not claim exactly-once transport guarantees, distributed transactions, change-data-capture semantics, time zone handling, concurrent writers, or crash-consistent filesystem recovery beyond SQLite transactions.

## BGSTM traceability

Planning: incomplete recovery risks missing or duplicated sales → Test Case Development: reruns, stale versions, conflict, interruption, late arrival → Environment Preparation: deterministic versioned CSV fixtures → Execution: isolated in-memory database and pytest → Results Analysis: compare before/after snapshots and oracle → Results Reporting: publication gate and [INC-004 investigation](../evidence/defect-examples/INC-004.md).
