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