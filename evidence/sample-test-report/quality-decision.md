# Example BGSTM results report — synthetic fixture

**Run scope:** paid orders in the ETL lab. **Method:** independent per-order and aggregate reconciliation.

| Check | Clean | Defective |
| --- | --- | --- |
| Row count | 3/3 | 3/3 |
| Missing/unexpected keys | None | None |
| Revenue total | $120.00/$120.00 | $132.50 actual vs $120.00 expected |
| Per-order differences | None | `O-1002` (+$12.50) |
| Gate | Pass | Fail |

**Decision:** The clean baseline meets v0.1 acceptance. The intentionally defective dataset fails reconciliation even though the ETL load succeeds. Hold publication of the affected output and investigate the input-price discrepancy. These are deterministic example expectations; run commands locally or in CI to generate actual execution evidence.
