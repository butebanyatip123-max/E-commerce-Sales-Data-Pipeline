"""
generate_data.py
Stage 1 of retail-sales-data-pipeline project.

Generates fake e-commerce data (customers, products, orders) using Faker,
and saves them as CSV files inside a local "raw/" folder — this simulates
the raw data landing zone you'd normally have in AWS S3 (s3://bucket/raw/).

Usage:
    python generate_data.py
"""

import csv
import os
import random
from datetime import datetime, timedelta
from faker import Faker

fake = Faker()
Faker.seed(42)
random.seed(42)

# ---- Config ----
NUM_CUSTOMERS = 200
NUM_PRODUCTS = 50
NUM_ORDERS = 1000
OUTPUT_DIR = "raw"

PRODUCT_CATEGORIES = [
    "Electronics", "Clothing", "Home & Kitchen", "Beauty",
    "Sports", "Books", "Toys", "Groceries"
]

ORDER_STATUSES = ["completed", "pending", "cancelled", "returned"]


def generate_customers(n):
    customers = []
    for i in range(1, n + 1):
        customers.append({
            "customer_id": i,
            "name": fake.name(),
            "email": fake.unique.email(),
            "city": fake.city(),
            "country": fake.country(),
            "signup_date": fake.date_between(start_date="-2y", end_date="-1d"),
        })
    return customers


def generate_products(n):
    products = []
    for i in range(1, n + 1):
        products.append({
            "product_id": i,
            "product_name": fake.unique.catch_phrase(),
            "category": random.choice(PRODUCT_CATEGORIES),
            "price": round(random.uniform(5, 500), 2),
        })
    return products


def generate_orders(n, num_customers, num_products):
    orders = []
    start_date = datetime.now() - timedelta(days=365)
    for i in range(1, n + 1):
        order_date = start_date + timedelta(days=random.randint(0, 365))
        quantity = random.randint(1, 5)
        product_id = random.randint(1, num_products)
        orders.append({
            "order_id": i,
            "customer_id": random.randint(1, num_customers),
            "product_id": product_id,
            "quantity": quantity,
            "order_date": order_date.strftime("%Y-%m-%d"),
            "status": random.choices(
                ORDER_STATUSES, weights=[0.75, 0.1, 0.1, 0.05]
            )[0],
        })
    return orders


def save_csv(rows, filename):
    filepath = os.path.join(OUTPUT_DIR, filename)
    if not rows:
        return
    with open(filepath, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=rows[0].keys())
        writer.writeheader()
        writer.writerows(rows)
    print(f"Saved {len(rows)} rows -> {filepath}")


def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    customers = generate_customers(NUM_CUSTOMERS)
    products = generate_products(NUM_PRODUCTS)
    orders = generate_orders(NUM_ORDERS, NUM_CUSTOMERS, NUM_PRODUCTS)

    save_csv(customers, "customers.csv")
    save_csv(products, "products.csv")
    save_csv(orders, "orders.csv")


if __name__ == "__main__":
    main()
    