# Transformation business contract — v0.2

**Requirement TR-001: inclusion.** Whitespace and case in known `status` values are formatting differences; only `PAID` rows count as realized sales. Unknown statuses are rejected rather than guessed. Supported known statuses are `PAID`, `PENDING` and `CANCELLED`.

**Requirement TR-002: money.** For a paid row, calculate the line's discounted net as `quantity × unit_price × (1 − discount_pct / 100)`. Use base-10 arithmetic and a single `ROUND_HALF_UP` operation at the **final line total**, then store integer cents. Quantity must be a positive integer; prices must be finite nonnegative decimals and discounts finite decimals between 0 and 100 inclusive.

**Requirement TR-003: identity.** `order_id` is unique and nonempty after trimming. Duplicate keys are an error, not a license to silently remove orders.

| Source ID | Status | Expected net cents | Rationale |
| --- | --- | ---: | --- |
| T-2001 | ` paid ` | 1799 | 19.99 less 10% = 17.991 → 17.99 |
| T-2002 | `PAID` | 667 | 2 × 3.335 = 6.670 → 6.67 |
| T-2003 | `Pending` | excluded | Not realized revenue |
| T-2004 | ` PAID ` | 2400 | 3 × 10.00 less 20% = 24.00 |

**Approved total: 4,866 cents.** These fixtures are synthetic and pedagogical. Independently reviewed expected values should not be recalculated by the implementation being tested.

## BGSTM evidence links
Planning: financial understatement risk → Test development: boundary and negative cases → Environment: controlled fixtures → Execution: pytest → Analysis: row-level discrepancies → Reporting: [TR-002 investigation](../evidence/defect-examples/TR-002.md).
