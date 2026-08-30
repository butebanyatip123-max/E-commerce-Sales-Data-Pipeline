"""
clean_data.py
Stage 2 of retail-sales-data-pipeline project.

Reads the raw CSV files from raw/, cleans and validates them with Pandas,
and saves the cleaned versions into cleaned/ — this simulates the
"Transform" step of an ETL pipeline (raw/ = S3 raw zone, cleaned/ = S3
cleaned zone).

Usage:
    python clean_data.py
"""

import os
import pandas as pd

RAW_DIR = "raw"
CLEANED_DIR = "cleaned"


def clean_customers(df):
    before = len(df)
    df = df.drop_duplicates(subset="customer_id")
    df = df.dropna(subset=["customer_id", "email"])
    df["email"] = df["email"].str.lower().str.strip()
    df["signup_date"] = pd.to_datetime(df["signup_date"], errors="coerce")
    print(f"customers: {before} -> {len(df)} rows after cleaning")
    return df


def clean_products(df):
    before = len(df)
    df = df.drop_duplicates(subset="product_id")
    df = df.dropna(subset=["product_id", "price"])
    df = df[df["price"] > 0]
    df["price"] = df["price"].round(2)
    print(f"products: {before} -> {len(df)} rows after cleaning")
    return df


def clean_orders(df, valid_customer_ids, valid_product_ids):
    before = len(df)
    df = df.drop_duplicates(subset="order_id")
    df = df.dropna(subset=["order_id", "customer_id", "product_id", "quantity"])
    df = df[df["quantity"] > 0]
    # keep only orders that reference a customer/product that actually exists
    df = df[df["customer_id"].isin(valid_customer_ids)]
    df = df[df["product_id"].isin(valid_product_ids)]
    df["order_date"] = pd.to_datetime(df["order_date"], errors="coerce")
    df = df.dropna(subset=["order_date"])
    print(f"orders: {before} -> {len(df)} rows after cleaning")
    return df


def main():
    os.makedirs(CLEANED_DIR, exist_ok=True)

    customers = pd.read_csv(os.path.join(RAW_DIR, "customers.csv"))
    products = pd.read_csv(os.path.join(RAW_DIR, "products.csv"))
    orders = pd.read_csv(os.path.join(RAW_DIR, "orders.csv"))

    customers_clean = clean_customers(customers)
    products_clean = clean_products(products)
    orders_clean = clean_orders(
        orders,
        valid_customer_ids=set(customers_clean["customer_id"]),
        valid_product_ids=set(products_clean["product_id"]),
    )

    customers_clean.to_csv(os.path.join(CLEANED_DIR, "customers.csv"), index=False)
    products_clean.to_csv(os.path.join(CLEANED_DIR, "products.csv"), index=False)
    orders_clean.to_csv(os.path.join(CLEANED_DIR, "orders.csv"), index=False)

    print(f"\nSaved cleaned files to '{CLEANED_DIR}/'")


if __name__ == "__main__":
    main()