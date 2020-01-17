import pickle
import sys
import argparse

import pandas as pd
from google.cloud import bigquery
from google.cloud import storage

import data_prep as dp
import model_train as mt

parser = argparse.ArgumentParser()

# --job-dir isn't needed by us, but it gets passed so we need to have this here
parser.add_argument('--job-dir')
# passed in name of bucket
parser.add_argument('--bucket')
# passed in info on if running locally
parser.add_argument('--run_location')

args = parser.parse_args(sys.argv[1:])
print(vars(args))

BUCKET_NAME = args.bucket
RUN_LOCATION = args.run_location

# Get the data
if RUN_LOCATION == 'local':
    client = bigquery.Client.from_service_account_json(
        'C:/Users/g557202/data-science-sandbox-d3c168-94e1fa28cf2f.json',
        location='US'
    )
    num_records = 100
else:
    client = bigquery.Client()
    num_records = 100000

# noinspection SqlNoDataSourceInspection
query = f"""
    SELECT sale_dollars,
           city,
           county_number,
           category,
           store_number,
           item_number,
           date
      FROM `bigquery-public-data.iowa_liquor_sales.sales`
     LIMIT {num_records}
"""

query_job = client.query(query)

df = query_job.to_dataframe()

df['year'] = pd.DatetimeIndex(df['date']).year
df['month'] = pd.DatetimeIndex(df['date']).month
df['day'] = pd.DatetimeIndex(df['date']).day

df = df.drop(['date'], axis=1)

# Categorical Vars to encode
cat_vars = [
    'city',
    'category',
    'county_number',
    'store_number',
    'item_number'
]

# Create dataframe with encoded categorical variables
df_cat, df_mapping = dp.category_columns(
    df,
    cat_vars
)

# Round sales_dollar column
df_cat = df_cat.round({'sale_dollars': 2})

# Save categorical mapping file
df_mapping.to_hdf(
    'categorical_mapping.hdf',
    'df_cat_map',
    format='table',
    mode='w'
)

# Save mapping to storage
if RUN_LOCATION == 'local':
    storage_client = storage.Client.from_service_account_json(
        'C:/Users/g557202/data-science-sandbox-d3c168-94e1fa28cf2f.json'
    )
else:
    storage_client = storage.Client()

bucket = storage_client.bucket(BUCKET_NAME)
blob = bucket.blob(
    'ai_platform_test/iowa_forecasting_artifacts/categorical_mapping.hdf')
blob.upload_from_filename('categorical_mapping.hdf')

# Set variable we are predicting for and predictors
y_col = 'sale_dollars'
x_cols = [
    'city_enc',
    'county_number_enc',
    'category_enc',
    'store_number_enc',
    'item_number_enc',
    'year',
    'month',
    'day'
]

# Create model object and importances
rfr_model, importances = mt.fit_model(
    y_col,
    x_cols,
    df_cat,
    trees=150,
    leaves=5
)

pickle.dump(
    rfr_model,
    open('model_test.pkl', 'wb')
)

bucket = storage_client.bucket(BUCKET_NAME)
blob = bucket.blob('ai_platform_test/iowa_forecasting_artifacts/model_test.pkl')
blob.upload_from_filename('model_test.pkl')
