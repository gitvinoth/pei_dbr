# Databricks notebook source
# MAGIC %run ../utils/utility

# COMMAND ----------

from pyspark.sql import functions as F

# COMMAND ----------

def build_enriched(spark, sales_df):
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

# COMMAND ----------

def build_aggregate(spark, sales_df):
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

# COMMAND ----------

def main(spark):
    sales_df = spark.read.table("ecom.sales.sales")

    enriched_df = build_enriched(spark, sales_df)
    print(f"Enriched {enriched_df.count()} rows loaded Successfully")

    agg_df = build_aggregate(spark, sales_df)
    print(f"Aggregated {agg_df.count()} rows loaded Successfully")

# COMMAND ----------

main(spark)