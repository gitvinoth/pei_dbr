# Databricks notebook source
# MAGIC %run ../utils/utility

# COMMAND ----------

from pyspark.sql import functions as F

# COMMAND ----------

try:
    if dbutils:
        pass 
except NameError:
    from utils.utility import write_table

# COMMAND ----------

def build_enriched(spark, sales_df):
    try:
        enriched_df = sales_df \
            .withColumn("order_year", F.year(F.col("order_date"))) \
            .groupBy("customer_name", "order_year") \
            .agg(
                F.round(F.sum("profit"), 2).alias("total_profit"),
                F.countDistinct("order_id").alias("order_count")
            ) \
            .orderBy("customer_name", "order_year")

        write_table(spark, enriched_df, "ecom.sales.enriched")
        return enriched_df
    except Exception as e:
        print(f"Error in build_enriched: {e}")
        return None

# COMMAND ----------

def build_aggregate(spark, sales_df):
    try:
        agg_df = sales_df \
            .withColumn("order_year", F.year(F.col("order_date"))) \
            .groupBy("order_year", "category", "sub_category") \
            .agg(
                F.round(F.sum("profit"), 2).alias("total_profit"),
                F.countDistinct("order_id").alias("order_count")
            ) \
            .orderBy("order_year", "category", "sub_category")

        write_table(spark, agg_df, "ecom.sales.aggregate")
        return agg_df
    except Exception as e:
        print(f"Error in build_aggregate: {e}")
        return None

# COMMAND ----------

def main(spark):
    try:
        sales_df = spark.read.table("ecom.sales.sales")
        
    except Exception as e:
        print(f"Error reading sales table: {e}")
        return

    enriched_df = build_enriched(spark, sales_df)

    if enriched_df is not None:
        print(f"Enriched {enriched_df.count()} rows loaded Successfully")
    else:
        print("Error: Enriched DataFrame not created.")

    agg_df = build_aggregate(spark, sales_df)

    if agg_df is not None:
        print(f"Aggregated {agg_df.count()} rows loaded Successfully")
    else:
        print("Error: Aggregated DataFrame not created.")

# COMMAND ----------

main(spark)
