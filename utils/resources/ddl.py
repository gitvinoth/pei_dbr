# Databricks notebook source
catalog = "ecom"
schema = "sales"

# COMMAND ----------

ecom_sales = {
    "order": "row_id INT, order_id STRING, order_date DATE, ship_date DATE, ship_mode STRING, customer_id STRING, product_id STRING, quantity INT, price DOUBLE, discount DOUBLE, profit DOUBLE",
    "product": "product_id STRING, category STRING, sub_category STRING, product_name STRING, state STRING, price_per_product DOUBLE",
    "customer": "customer_id STRING, customer_name STRING, email STRING, phone STRING, address STRING, segment STRING, country STRING, city STRING, state STRING, postal_code STRING, region STRING",
    "sales": "row_id INT, order_id STRING, order_date DATE, order_year INT, ship_date DATE, ship_mode STRING, customer_id STRING, customer_name STRING, country STRING, product_id STRING, category STRING, sub_category STRING, quantity INT, price DOUBLE, discount DOUBLE, profit DOUBLE",
    "enriched": "customer_name STRING, order_year INT, total_profit DOUBLE, order_count BIGINT",
    "aggregate": "order_year INT, category STRING, sub_category STRING, total_profit DOUBLE, order_count BIGINT"
}

# COMMAND ----------

for table_name, schema_str in ecom_sales.items():
    spark.sql(f"""
        CREATE TABLE IF NOT EXISTS {catalog}.{schema}.{table_name} (
            {schema_str}
        )
    """)
