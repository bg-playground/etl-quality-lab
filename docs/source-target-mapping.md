# Source-to-target mapping and oracle

| Source column | Target column | Rule |
| --- | --- | --- |
| `order_id` | `fact_orders.order_id` | Trim, required, unique across source |
| `customer_id` | `fact_orders.customer_id` | Trim, preserve for included rows |
| `status` | inclusion rule | Include only `PAID` (case-insensitive) |
| `quantity`, `unit_price` | `revenue_cents` | Positive integer quantity × nonnegative decimal price, rounded half-up to cent; store integer cents |

## Expected results

The `data/expected/fact_orders.csv` file represents a reviewed business fixture and must not be regenerated from pipeline output. Three paid orders are expected, totaling 12,000 cents. Order `O-1003` is cancelled and excluded.

If a new business rule changes expected results, require review of the mapping, fixtures and tests together; do not simply accept whatever the transform generated.
