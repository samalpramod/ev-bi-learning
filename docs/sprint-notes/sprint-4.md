# Sprint 4 — ETL Automation + Dashboard Foundation

## Sprint Objective

Build a reusable ETL pipeline that extracts data from the EV charging OLTP database, transforms and validates the data, and loads it into the BI star schema.

The sprint will also establish the foundation for a Streamlit dashboard and introduce Power BI and DAX.

## Development Workflow

This sprint follows:

1. Learn
2. Design
3. Implement
4. Test
5. Document
6. Commit
7. Push
8. Verify clean working tree

The sprint is complete only after all required artifacts are committed and pushed to GitHub.

## Current Architecture

```text
EV Charging OLTP MySQL
          |
          | Extract
          v
     Python ETL
          |
    +-----+-----+
    |           |
Transform    Validate
    |           |
    +-----+-----+
          |
          | Load
          v
     BI Star Schema
          |
     +----+----+
     |         |
     v         v
Streamlit   Power BI
Dashboard   Dashboard

## Sprint 4 Final Validation

### ETL Pipeline

The Sprint 4 ETL pipeline loads data from the MySQL OLTP database into the PostgreSQL star schema.

Pipeline:

MySQL OLTP
    |
    +--> dim_operator
    +--> dim_location
    +--> dim_charge_point
    +--> dim_customer
    +--> dim_date
    |
    +--> fact_charging
            |
            +--> dim_date
            +--> dim_operator
            +--> dim_location
            +--> dim_charge_point
            +--> dim_customer

### Final Row Counts

| Table | Rows |
|---|---:|
| dim_operator | 10 |
| dim_location | 50 |
| dim_charge_point | 200 |
| dim_customer | 1,000 |
| dim_date | 609 |
| fact_charging | 50,000 |

### Relationship Validation

All fact table foreign-key relationships were validated against the dimension tables.

Result:

- Orphan dimension keys: 0
- Invalid dimension references: 0

### Source-to-Target Reconciliation

| Metric | Source MySQL | Target PostgreSQL |
|---|---:|---:|
| Transactions | 50,000 | 50,000 |
| Energy (kWh) | 2,128,019.598 | 2,128,019.598 |
| Revenue | 38,304,352.30 | 38,304,352.30 |
| Average Transaction Value | 766.09 | 766.09 |
| Average Duration (minutes) | 95.23 | 95.23 |

### Dimension Mapping

The fact table uses PostgreSQL surrogate keys while preserving source-system identifiers in the dimensions.

Mappings:

- transaction charge_point_id -> dim_charge_point -> charge_point_key
- charge point location_id -> dim_location -> location_key
- location operator_id -> dim_operator -> operator_key
- transaction customer_id -> dim_customer -> customer_key
- transaction start date -> dim_date -> date_key

### Sprint 4 Outcome

Sprint 4 successfully established the PostgreSQL analytical star schema and completed the initial MySQL-to-PostgreSQL ETL pipeline.

Completed components:

- PostgreSQL star schema
- Source and target database connections
- Operator dimension ETL
- Location dimension ETL
- Charge point dimension ETL
- Customer dimension ETL
- Date dimension ETL
- Charging fact ETL
- Source-to-target reconciliation
- Dimension relationship validation

The analytical database is now ready for BI queries and dashboard development.

### Git Status

All Sprint 4 ETL and documentation changes must be committed and pushed to the main branch before starting the next sprint.