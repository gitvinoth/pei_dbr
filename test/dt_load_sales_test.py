import pytest
from unittest.mock import patch
from pyspark.sql import functions as F
from dt_load_sales import build_enriched, build_aggregate, main


def setup_sales_df(spark):
    return spark.createDataFrame(
        [
            ("1", "2026-01-01", "Vinoth Ravi", "Furniture",  "Table",  20.0),
            ("2", "2026-03-10", "Priya Kumar", "Technology", "Phones",  8.5),
            ("3", "2026-01-15", "Vinoth Ravi", "Furniture",  "Table",  -5.0),
            ("4", "2027-11-20", "Priya Kumar", "Technology", "Phones", 15.0),
            ("5", "2026-06-30", "Vinoth Ravi", "Technology", "Phones", 30.0),
        ],
        ["order_id", "order_date", "customer_name", "category", "sub_category", "profit"]
    )


def run_enriched(spark):
    sales_df = setup_sales_df(spark)
    with patch("dt_load_sales.write_table") as _patch_write_table:
        with patch.object(spark, "sql") as _patch_sql:
            return build_enriched(spark, sales_df)


def run_aggregate(spark):
    sales_df = setup_sales_df(spark)
    with patch("dt_load_sales.write_table") as _patch_write_table:
        with patch.object(spark, "sql") as _patch_sql:
            return build_aggregate(spark, sales_df)


def test_enriched_columns(spark):
    result = run_enriched(spark)
    assert set(result.columns) == {"customer_name", "order_year", "total_profit", "order_count"}


def test_enriched_groups_by_customer_and_year(spark):
    result = run_enriched(spark)
    assert result.count() == result.select("customer_name", "order_year").distinct().count()

def test_aggregate_profit_is_not_null(spark):
    result = run_aggregate(spark)
    for row in result.collect():
        assert row["total_profit"] is not None


def test_main_calls_both_functions(spark):
    sales_df = setup_sales_df(spark)
    called = []

    def fake_enriched(s, df):
        called.append("enriched")
        return df

    def fake_aggregate(s, df):
        called.append("aggregate")
        return df

    with patch("dt_load_sales.write_table") as _patch_write_table:
        with patch.object(spark, "sql") as _patch_sql:
            with patch.object(spark.read, "table", return_value=sales_df) as _patch_table:
                with patch("dt_load_sales.build_enriched",  side_effect=fake_enriched) as _patch_enriched:
                    with patch("dt_load_sales.build_aggregate", side_effect=fake_aggregate) as _patch_aggregate:
                        main(spark)

    assert "enriched"  in called
    assert "aggregate" in called


def test_main_reads_from_sales_table(spark):
    sales_df = setup_sales_df(spark)

    with patch("dt_load_sales.write_table") as _patch_write_table:
        with patch.object(spark, "sql") as _patch_sql:
            with patch("dt_load_sales.build_enriched",  return_value=sales_df) as _patch_enriched:
                with patch("dt_load_sales.build_aggregate", return_value=sales_df) as _patch_aggregate:
                    with patch.object(spark.read, "table", return_value=sales_df) as mock_table:
                        main(spark)

    mock_table.assert_called_once_with("ecom.sales.sales")


def test_enriched_no_duplicates_and_not_null(spark):
    result = run_enriched(spark)
    dup_count = result.groupBy("customer_name", "order_year").count().filter(F.col("count") > 1).count()
    assert dup_count == 0
    for col in result.columns:
        assert result.filter(F.col(col).isNull()).count() == 0