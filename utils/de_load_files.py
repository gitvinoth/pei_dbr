# Databricks notebook source
# MAGIC %run ../utils/utility

# COMMAND ----------

from pyspark.sql import functions as F

# COMMAND ----------

customer = "file:/Workspace/Users/vinothravikct95@outlook.com/PEI/src/Customer.xlsx"
orders ="file:/Workspace/Users/vinothravikct95@outlook.com/PEI/src/Orders.json"
products = "file:/Workspace/Users/vinothravikct95@outlook.com/PEI/src/Products.csv"

# COMMAND ----------

# DBTITLE 1,customer
customer_raw = read_xlsx(spark, customer)

customer_df = customer_raw \
    .withColumnRenamed("Customer ID",   "customer_id") \
    .withColumnRenamed("Customer Name", "customer_name") \
    .withColumnRenamed("email",         "email") \
    .withColumnRenamed("phone",         "phone") \
    .withColumnRenamed("address",       "address") \
    .withColumnRenamed("Segment",       "segment") \
    .withColumnRenamed("Country",       "country") \
    .withColumnRenamed("City",          "city") \
    .withColumnRenamed("State",         "state") \
    .withColumnRenamed("Postal Code",   "postal_code") \
    .withColumnRenamed("Region",        "region")


write_table(spark, customer_df, "ecom.sales.customer")   

# COMMAND ----------

# DBTITLE 1,Order
orders_raw = read_json(spark, orders)

orders_df = orders_raw \
    .withColumnRenamed("Row ID",      "row_id") \
    .withColumnRenamed("Order ID",    "order_id") \
    .withColumnRenamed("Order Date",  "order_date") \
    .withColumnRenamed("Ship Date",   "ship_date") \
    .withColumnRenamed("Ship Mode",   "ship_mode") \
    .withColumnRenamed("Customer ID", "customer_id") \
    .withColumnRenamed("Product ID",  "product_id") \
    .withColumnRenamed("Quantity",    "quantity") \
    .withColumnRenamed("Price",       "price") \
    .withColumnRenamed("Discount",    "discount") \
    .withColumnRenamed("Profit",      "profit") \
    .withColumn("order_date", F.to_date(F.col("order_date"), "d/M/yyyy")) \
    .withColumn("ship_date",  F.to_date(F.col("ship_date"),  "d/M/yyyy"))


write_table(spark, orders_df, "ecom.sales.order")


# COMMAND ----------

# DBTITLE 1,product
products_df = read_csv(spark, products).toDF(
    "product_id", "category", "sub_category",
    "product_name", "state", "price_per_product"
)
write_table(spark, products_df, "ecom.sales.product")