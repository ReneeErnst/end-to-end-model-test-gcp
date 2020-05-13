"""Model Training"""
import argparse
import sys
import pickle

import pandas as pd
from google.cloud import bigquery
from google.cloud import storage

from modeling import aip_example

parser = argparse.ArgumentParser()

# --job-dir isn't needed by us, but it gets passed so we need to have this here
parser.add_argument('--job-dir')

parser.add_argument('--run_location')
parser.add_argument('--bucket')
parser.add_argument('--path')

args = parser.parse_args(sys.argv[1:])
print(vars(args))

RUN_LOCATION = args.run_location
BUCKET_NAME = args.bucket
PATH = args.path

# Get the data
if RUN_LOCATION == 'local':
    num_records = 100
else:
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

client = bigquery.Client()

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
df_cat, df_mapping = aip_example.category_columns(
    df,
    cat_vars
)

# Round sales_dollar column
df_cat = df_cat.round({'sale_dollars': 2})

# Save categorical mapping file
df_mapping.to_pickle('categorical_mapping.pkl')

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
rfr_model, importances = aip_example.fit_model(
    y_col,
    x_cols,
    df_cat,
    trees=150,
    leaves=5
)

pickle.dump(
    rfr_model,
    open('model.pkl', 'wb')
)

# Save files to GCS
if RUN_LOCATION == 'local':
    print('Running Locally - No need to save out to GCS')
else:
    storage_client = storage.Client()

    bucket = storage_client.bucket(BUCKET_NAME)

    # Save mapping file
    blob = bucket.blob(
        f'{PATH}/categorical_mapping.pkl')
    blob.upload_from_filename('categorical_mapping.pkl')

    # Save model file
    blob = bucket.blob(f'{PATH}/model.pkl')
    blob.upload_from_filename('model.pkl')
