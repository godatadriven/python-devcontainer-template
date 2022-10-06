from pyspark.sql import DataFrame


def calculate_sales_per_country(sales: DataFrame):
    return (
        sales.groupBy("country")
        .sum()
        .withColumnRenamed("sum(amount)", "total_sales")
    )
