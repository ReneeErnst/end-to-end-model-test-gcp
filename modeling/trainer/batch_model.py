"""Model Training"""
import argparse
import sys
import pickle
import os

import pandas as pd
from google.cloud import bigquery
from google.cloud import storage

from modeling import model_train as mt, data_prep as dp

parser = argparse.ArgumentParser()

# --job-dir isn't needed by us, but it gets passed so we need to have this here
parser.add_argument('--job-dir')

# passed in info on if running locally
parser.add_argument('--run_location')

# passed in name of bucket
parser.add_argument('--bucket')

args = parser.parse_args(sys.argv[1:])
print(vars(args))

RUN_LOCATION = args.run_location
BUCKET_NAME = args.bucket


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
df_cat, df_mapping = dp.category_columns(
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
rfr_model, importances = mt.fit_model(
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
        'ai_platform_test/iowa_forecasting_artifacts/categorical_mapping.pkl')
    blob.upload_from_filename('categorical_mapping.pkl')

    # Save model file
    blob = bucket.blob('ai_platform_test/iowa_forecasting_artifacts/model.pkl')
    blob.upload_from_filename('model.pkl')


#Train and Test Data
df_train_rfr, df_test_rfr = mt.split_train_test(
    df_cat,
    'month',
    3
)

print('Length of Training Data: ', len(df_train_rfr))
print('Length of Test Data: ', len(df_test_rfr))

# Create model object and importances
rfr_model, importances = mt.fit_model(
    y_col,
    x_cols,
    df_train_rfr,
    trees=150,
    leaves=5
)

#Model results
df_results = mt.model_predict(
    rfr_model,
    df_test_rfr,
    y_col,
    x_cols
)

#Save results to BigQuery
project_path = os.path.expanduser('~/project.txt')
with open(project_path) as f:
    PROJECT_NAME = f.read().strip()

table_id = 'ai_platform_test.df_results_table'
project_id = PROJECT_NAME
df_results.to_gbq(table_id, project_id)