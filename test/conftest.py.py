# Databricks notebook source
import sys
import os
import pytest
from pyspark.sql import SparkSession

# COMMAND ----------

sys.path.insert(0, "/Workspace/Users/vinothravikct95@outlook.com/PEI/etl")


# COMMAND ----------

@pytest.fixture(scope="module")
def spark():
    return SparkSession.builder.getOrCreate()