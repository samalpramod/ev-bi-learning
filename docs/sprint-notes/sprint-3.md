FactCharging Grain

One row represents one EV charging session/transaction.

The fact table contains measurable business events such as:
- Energy consumed
- Charging duration
- Revenue amount
- Transaction count

## Day 1 — Fact vs Dimension Classification

| Field | Classification | Reason |
|---|---|---|
| transaction_code | Dimension | Transaction identifier |
| customer name | Dimension | Customer descriptive attribute |
| customer city | Dimension | Customer descriptive attribute |
| operator name | Dimension | Operator descriptive attribute |
| location city | Dimension | Location descriptive attribute |
| location type | Dimension | Location descriptive attribute |
| charge point connector type | Dimension | Charge point descriptive attribute |
| charge point power_kw | Dimension | Charge point capability |
| start_time | Dimension | Event timestamp |
| end_time | Dimension | Event timestamp |
| duration_minutes | Fact | Measurable session duration |
| energy_kwh | Fact | Measurable energy consumption |
| amount | Fact | Measurable transaction amount |
| transaction status | Dimension | Categorical transaction attribute |

### Important BI Modeling Rule

A numeric field is not automatically a fact.

A fact represents a measurable business event or value at the defined fact-table grain.

A dimension contains descriptive context used to analyze facts.

## Day 2 — Fact Table Design Decisions

### FactCharging Grain

One row represents one EV charging session/transaction.

### Measures

The following columns are measurable business values:

- duration_minutes
- energy_kwh
- amount

These can be aggregated in Power BI using SUM, AVG and other calculations.

### Transaction Code

transaction_code remains directly in FactCharging.

A separate DimTransaction is not required because it does not provide additional analytical context.

transaction_code acts as a degenerate dimension / transaction identifier within the fact table.

### Initial Star Schema

Dimensions:

- DimDate
- DimOperator
- DimLocation
- DimChargePoint
- DimCustomer

Fact:

- FactCharging

Fact measures:

- duration_minutes
- energy_kwh
- amount

Fact identifiers/descriptive fields:

- transaction_code
- start_time
- end_time
- status