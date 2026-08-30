"""
load_to_bigquery.py
Stage 3 of retail-sales-data-pipeline project.
 
Loads the cleaned CSV files (from cleaned/) into Google BigQuery,
creating a dataset and one table per file. This is the "Load" step into
the data warehouse, which SQL/Looker Studio will query afterwards.
 
Setup required before running:
1. Place your downloaded service-account JSON key file somewhere in this
   project folder, e.g. "gcp_key.json" (make sure its filename is listed
   in .gitignore so it never gets committed).
2. Add these lines to your .env file (create it if it doesn't exist):
 
    GOOGLE_APPLICATION_CREDENTIALS=gcp_key.json
    GCP_PROJECT_ID=your-project-id-here
    BQ_DATASET=retail_sales
 
   (Find your project ID on the Google Cloud console, next to the
   project name at the top of the page.)
 
Usage:
    python load_to_bigquery.py
"""
 
import os
from google.cloud import bigquery
from google.oauth2 import service_account
from dotenv import load_dotenv
 
load_dotenv()
 
CLEANED_DIR = "cleaned"
TABLES = {
    "customers.csv": "customers",
    "products.csv": "products",
    "orders.csv": "orders",
}
 
 
def get_bq_client():
    key_path = os.environ["GOOGLE_APPLICATION_CREDENTIALS"]
    credentials = service_account.Credentials.from_service_account_file(key_path)
    project_id = os.environ["GCP_PROJECT_ID"]
    return bigquery.Client(credentials=credentials, project=project_id)
 
 
def ensure_dataset(client, dataset_id):
    dataset_ref = f"{client.project}.{dataset_id}"
    try:
        client.get_dataset(dataset_ref)
        print(f"Dataset {dataset_ref} already exists")
    except Exception:
        dataset = bigquery.Dataset(dataset_ref)
        dataset.location = "asia-southeast1"
        client.create_dataset(dataset)
        print(f"Created dataset {dataset_ref}")
 
 
def load_csv_to_table(client, dataset_id, csv_filename, table_name):
    local_path = os.path.join(CLEANED_DIR, csv_filename)
    table_id = f"{client.project}.{dataset_id}.{table_name}"
 
    job_config = bigquery.LoadJobConfig(
        source_format=bigquery.SourceFormat.CSV,
        skip_leading_rows=1,
        autodetect=True,
        write_disposition=bigquery.WriteDisposition.WRITE_TRUNCATE,
    )
 
    with open(local_path, "rb") as f:
        job = client.load_table_from_file(f, table_id, job_config=job_config)
    job.result()  # wait for the load job to finish
 
    table = client.get_table(table_id)
    print(f"Loaded {table.num_rows} rows into {table_id}")
 
 
def main():
    client = get_bq_client()
    dataset_id = os.environ.get("BQ_DATASET", "retail_sales")
 
    ensure_dataset(client, dataset_id)
 
    for csv_filename, table_name in TABLES.items():
        load_csv_to_table(client, dataset_id, csv_filename, table_name)
 
 
if __name__ == "__main__":
    main()
 
