# Day 1 — Basic Concepts

## OLTP
Online Transaction Processing (OLTP) is used for maintaining online transactions and data integrity in a multi user enviornment. OLTP uses traditional RDBMS with normalized tables optimized for write-heavy operations. It manages very large number of transactions like online purchase, order processing and banking transactions, POS transaction and etc.

## OLAP
On-Line Analytical Processing(OLAP)is used for analysis of database information from multiple sources. OLAP is designed for complex data analysis and reporting.OLAP supports complex queries for sales analysis, forecasting, market research, budgeting, and business intelligence. OLAP uses data warehouses with denormalized tables optimized for read-heavy analytical queries.

## Fact
A fact represents something measurable that happened. For example if I say I charged my ev with 32kWh which cost me Rs 485 and took 45 minutes. Here it explain the amount Ev charged and amount paid and how much time taken for the same.

## Dimension
A dimension provides the context to the fact. For example in above case I am (customer), Date, time,charging operator,charging point, locatioin, all dimensions. Fact says what happend and dimension explains who did it, when and where it being done.

## KPI
Key performance indicator(KPI)  is a measurable value that shows progress toward a desired result. Organizations use KPIs to evaluate performance, guide decision‑making, and ensure alignment with strategic objectives. 
In our EV charging platform a few KPI will be Total Energy consumed, Total transactioins, Total revenue, Total vehicles, Total CPs, etc

## Dashboard
 Dashboard serves as a centralized platform or decession making interface where users can access important information about business, or system in real time.

## ETL
ETL stands for Extraction >Transform ->Load is a crucial process in data science and data management that involves three main stages:

Extract: Gathering data from various sources, such as databases, cloud storage, and web APIs.
Transform: Cleaning, organizing, and preparing the data for analysis, including removing duplicates and formatting it to a consistent format.
Load: Transferring the processed data into a target system, such as a data warehouse or data lake, for storage and analysis.

## Data Warehouse
Data warehousing is a crucial component of data science and analytics, providing a centralized repository for data integration and analysis. Data warehousing a system designed primarily for analytical workloads rather than day-to-day transactions