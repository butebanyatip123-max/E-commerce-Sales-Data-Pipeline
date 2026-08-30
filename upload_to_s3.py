"""
upload_to_s3.py
Stage 2 (part 2) of retail-sales-data-pipeline project.

Uploads the cleaned CSV files (from cleaned/) to an AWS S3 bucket.
This is the "Load" step of the pipeline: local cleaned/ -> S3 cleaned/ zone.

Credentials are NEVER hardcoded here. They are loaded from a local .env
file (which is excluded from git via .gitignore) using python-dotenv.

Setup required before running:
1. Create a file named ".env" in the project root (same folder as this
   script) with the following content (replace with your real values):

    AWS_ACCESS_KEY_ID=your_access_key_here
    AWS_SECRET_ACCESS_KEY=your_secret_key_here
    AWS_REGION=ap-southeast-2
    S3_BUCKET_NAME=retail-sales-pipeline-ben2026

2. Make sure ".env" is listed in .gitignore so it never gets committed.

Usage:
    python upload_to_s3.py
"""

import os
import boto3
from dotenv import load_dotenv

load_dotenv()  # reads variables from the local .env file

CLEANED_DIR = "cleaned"
S3_PREFIX = "cleaned"  # folder inside the bucket, e.g. s3://bucket/cleaned/

FILES_TO_UPLOAD = ["customers.csv", "products.csv", "orders.csv"]


def get_s3_client():
    return boto3.client(
        "s3",
        aws_access_key_id=os.environ["AWS_ACCESS_KEY_ID"],
        aws_secret_access_key=os.environ["AWS_SECRET_ACCESS_KEY"],
        region_name=os.environ.get("AWS_REGION", "ap-southeast-2"),
    )


def upload_files():
    bucket_name = os.environ["S3_BUCKET_NAME"]
    s3 = get_s3_client()

    for filename in FILES_TO_UPLOAD:
        local_path = os.path.join(CLEANED_DIR, filename)
        if not os.path.exists(local_path):
            print(f"Skipping {filename} (not found in {CLEANED_DIR}/)")
            continue

        s3_key = f"{S3_PREFIX}/{filename}"
        s3.upload_file(local_path, bucket_name, s3_key)
        print(f"Uploaded {local_path} -> s3://{bucket_name}/{s3_key}")


if __name__ == "__main__":
    upload_files()
