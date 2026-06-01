# Databricks notebook source
from pyspark.sql import functions as F

# COMMAND ----------

# MAGIC %run ../utils/utility

# COMMAND ----------

try:
    if dbutils:
        pass 
except NameError:
    from utils.utility import write_table

# COMMAND ----------

# DBTITLE 1,Define main function
def main():

    orders_df   = spark.read.table("ecom.sales.order")
    customer_df = spark.read.table("ecom.sales.customer")
    products_df = spark.read.table("ecom.sales.product")
    
    sales_df = orders_df \
        .join(
            customer_df.withColumnRenamed("state", "customer_state"),
            on="customer_id", how="left"
        ) \
        .join(
            products_df.withColumnRenamed("state", "product_state"),
            on="product_id", how="left"
        ) \
        .select(
            "order_id",
            "order_date",
            "ship_date",
            "ship_mode",
            "customer_id",
            "customer_name",
            "segment",
            "country",
            "city",
            "customer_state",
            "product_id",
            "category",
            "sub_category",
            "product_name",
            "quantity",
            "price",
            "discount",
            "profit"
        )
    
    # Write to target table
    write_table(spark, sales_df, "ecom.sales.sales")
    
    return "Sales data loaded successfully"

# COMMAND ----------

# DBTITLE 1,Execute main function
if __name__ == "__main__":
    result = main()
    print(result)