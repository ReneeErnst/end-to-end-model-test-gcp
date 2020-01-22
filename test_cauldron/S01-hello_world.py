"""
Test notebook for remote executing w/Cauldron Notebooks on AI Platform
"""
# noinspection PyPackageRequirements
import cauldron as cd

from google.cloud import bigquery

# Test pulling data from bigquery

# noinspection SqlNoDataSourceInspection
query = """
    SELECT sale_dollars,
           city,
           county_number,
           category,
           store_number,
           item_number,
           date
      FROM `bigquery-public-data.iowa_liquor_sales.sales`
     LIMIT 10
"""

client = bigquery.Client()

query_job = client.query(query)

df = query_job.to_dataframe()

cd.display.table(df.head())
