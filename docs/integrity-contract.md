# Data integrity and schema evolution contract — Lab 03

**Requirement INT-001 — required schema.** Customers require `customer_id`, `name`, and `country`. Orders require `order_id`, `customer_id`, and `amount_cents`. Removal or renaming of these columns is a breaking contract change. Additional columns are accepted by this bounded lesson, including the optional `preferred_language` field. Acceptance of new fields is not an endorsement of unrestricted schema evolution for every system.

**Requirement INT-002 — identity.** Customer and order identifiers must be nonblank after trimming and unique within their respective extracts. No silent duplicate removal.

**Requirement INT-003 — required values and foreign keys.** Customer names cannot be blank. Order customer IDs are required and must match a customer in the same loaded extract.

**Requirement INT-004 — monetary type.** Order `amount_cents` must be a nonnegative canonical integer string (for example, `375`, not `3.75`, `0375`, `-1`, or `NaN`). This intentionally strict contract is separate from the Decimal calculation rules taught in Lab 02.

## Test strategy

- Independent deterministic synthetic fixtures: `clean`, `additive`, `missing`, and `broken`.
- Assertion-based negative-path verification: the controlled broken fixtures **must** generate exactly the documented failure signals while normal CI remains green.
- Missing required headers short-circuit row checks to prevent cascading errors based on absent fields.
- Violations are reportable evidence, not silently corrected data.

## Bounded limitations

This lab checks customer names but does not yet enforce nonblank country values, temporal integrity, global uniqueness across partitions, runtime data migrations, or compatibility across deployed schema versions. CSV structural validation such as malformed row width is also outside v0.3. These are explicit future extensions, not verified behaviors.
