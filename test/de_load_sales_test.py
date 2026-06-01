import pytest
from unittest.mock import patch, MagicMock
from de_load_sales import main


def _mock_main(spark):
    orders_df = spark.createDataFrame(
        [(1, "2026-01-01", "2026-01-03", "Priority", 1, 1, 1, 25000.0, 0.2, 10.0)],
        ["order_id", "order_date", "ship_date", "ship_mode",
         "customer_id", "product_id", "quantity", "price", "discount", "profit"]
    )
    customer_df = spark.createDataFrame(
        [(1, "Vinoth Ravi", "Consumer", "India", "Bangalore", "KA")],
        ["customer_id", "customer_name", "segment", "country", "city", "state"]
    )
    products_df = spark.createDataFrame(
        [(1, "Furniture", "Table", "Dining Table", "KA")],
        ["product_id", "category", "sub_category", "product_name", "state"]
    )

    mock_read = MagicMock()
    mock_read.table.side_effect = [orders_df, customer_df, products_df]
    mock_spark = MagicMock()
    mock_spark.read = mock_read

    with patch("de_load_sales.spark", mock_spark),patch("de_load_sales.write_table") as mock_write:
        result = main()

    return result, mock_write



def test_returns_success_message(spark):
    result, _ = _mock_main(spark)
    assert result == "Sales data loaded successfully"


def test_write_called_once(spark):
    _, mock_write = _mock_main(spark)
    mock_write.assert_called_once()


def test_writes_to_correct_table(spark):
    _, mock_write = _mock_main(spark)
    assert mock_write.call_args[0][2] == "ecom.sales.sales"


def test_output_columns_are_correct(spark):
    _, mock_write = _mock_main(spark)
    cols = [
        "order_id", "order_date", "ship_date", "ship_mode",
        "customer_id", "customer_name", "segment", "country", "city", "customer_state",
        "product_id", "category", "sub_category", "product_name",
        "quantity", "price", "discount", "profit"
    ]
    assert mock_write.call_args[0][1].columns == cols


def test_customer_joined_correctly(spark):
    _, mock_write = _mock_main(spark)
    row = mock_write.call_args[0][1].collect()[0]
    assert row.customer_name  == "Vinoth Ravi"
    assert row.customer_state == "KA"


def test_product_joined_correctly(spark):
    _, mock_write = _mock_main(spark)
    row = mock_write.call_args[0][1].collect()[0]
    assert row.category     == "Furniture"
    assert row.product_name == "Dining Table"


def test_row_count_matches_orders(spark):
    _, mock_write = _mock_main(spark)
    assert mock_write.call_args[0][1].count() == 1


def test_no_duplicates(spark):
    _, mock_write = _mock_main(spark)
    df = mock_write.call_args[0][1]
    assert df.count() == df.dropDuplicates().count()


def test_key_columns_are_not_null(spark):
    _, mock_write = _mock_main(spark)
    row = mock_write.call_args[0][1].collect()[0]
    for col in ["order_id", "customer_name", "category", "profit"]:
        assert row[col] is not None


def test_profit_is_float(spark):
    _, mock_write = _mock_main(spark)
    row = mock_write.call_args[0][1].collect()[0]
    assert isinstance(row.profit, float)


def test_discount_is_non_negative(spark):
    _, mock_write = _mock_main(spark)
    row = mock_write.call_args[0][1].collect()[0]
    assert row.discount >= 0