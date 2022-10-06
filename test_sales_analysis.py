import pytest
from pyspark import Row
from pyspark.sql import DataFrame, SparkSession

from sales_analysis import calculate_sales_per_country


@pytest.fixture
def spark() -> SparkSession:
    spark = SparkSession.builder.getOrCreate()
    return spark


def test_calculate_sales_per_country(spark: SparkSession):
    sales: DataFrame = spark.createDataFrame(
        [
            Row(country="The Netherlands", amount=30),
            Row(country="The Netherlands", amount=50),
            Row(country="The Netherlands", amount=20),
        ]
    )
    sales_per_country: DataFrame = calculate_sales_per_country(sales)

    expected_sales: Row = Row(country="The Netherlands", total_sales=100)
    actual_sales: Row = sales_per_country.collect()[0]
    assert actual_sales == expected_sales
