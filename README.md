# E-commerce Sales Data Pipeline

An end-to-end ETL data pipeline that generates, cleans, and loads retail sales data into a cloud data warehouse, with an interactive analytics dashboard.

## Dashboard

[View live dashboard](https://datastudio.google.com/reporting/26c60381-6452-4a8a-9d97-39e4d6637639)

## Architecture

```
Python (Faker) → generate raw data
        ↓
AWS S3 (raw/)
        ↓
Python (Pandas) → clean & validate data
        ↓
AWS S3 (cleaned/)
        ↓
Google BigQuery → data warehouse
        ↓
SQL → analytics queries
        ↓
Looker Studio → dashboard
```

## Tech stack

- **Python** — data generation (Faker) and transformation (Pandas)
- **AWS S3** — data lake for raw and cleaned data
- **Google BigQuery** — cloud data warehouse
- **SQL** — analytics queries (revenue trends, top products, customer segmentation)
- **Looker Studio** — interactive dashboard

## What this project demonstrates

- Building a data pipeline from scratch: extract, transform, load
- Data cleaning and validation with Pandas (deduplication, null handling, referential integrity checks)
- Cloud storage and data warehousing with AWS and Google Cloud
- Writing analytical SQL (joins, aggregations, window functions)
- Turning raw data into a business-facing dashboard with KPIs

## Project structure

```
retail-sales-data-pipeline/
├── generate_data.py       # Stage 1: generate fake e-commerce data
├── clean_data.py           # Stage 2: clean and validate data
├── upload_to_s3.py         # Stage 2: upload to AWS S3
├── load_to_bigquery.py     # Stage 3: load into BigQuery
├── analytics_queries.sql   # Stage 4: SQL analytics queries
├── raw/                    # raw generated data
├── cleaned/                # cleaned data ready for warehouse
└── README.md
```

## Running this project

1. Clone the repo and install dependencies: `pip install -r requirements.txt` (or install `faker`, `pandas`, `boto3`, `google-cloud-bigquery`, `python-dotenv` individually)
2. Create a `.env` file (see `.env.example`) with your own AWS and GCP credentials
3. Run the pipeline in order:
   ```
   python generate_data.py
   python clean_data.py
   python upload_to_s3.py
   python load_to_bigquery.py
   ```
4. Run the queries in `analytics_queries.sql` against your BigQuery dataset
5. Connect Looker Studio to BigQuery to build your own dashboard

## Dashboard preview

The dashboard includes:
- KPI summary cards (total revenue, orders, customers)
- Daily sales trend
- Top 10 best-selling products by revenue
- Top 10 customers by total spend
- Order status breakdown (completed / pending / cancelled / returned)

## What this project demonstrates
This project spans both Data Engineering (building the pipeline, cloud storage, data warehousing) and Data Analysis (SQL analytics, dashboard design) — showing the full journey from raw data to business insight.