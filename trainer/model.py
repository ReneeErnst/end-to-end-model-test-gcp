import pickle

import pandas as pd
from google.cloud import bigquery
from google.cloud import storage

import data_prep as dp
import model_train as mt

BUCKET_NAME = 'python-testing-re'

# Get the data
# ToDo: Add check if running locally or in the cloud to fill these out
# Client when running in GCP
client = bigquery.Client()

# Client when running locally
# client = bigquery.Client.from_service_account_json(
#     'C:/Users/g557202/data-science-sandbox-d3c168-94e1fa28cf2f.json',
#     location='US'
# )

# ToDo: Set size of data pull based on local vs on GCP
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
     LIMIT 100
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
# ToDo: Create function to determine where running to set this
# Client when running on GCP
storage_client = storage.Client()

# Client when running locally
# storage_client = storage.Client.from_service_account_json(
#     'C:/Users/g557202/data-science-sandbox-d3c168-94e1fa28cf2f.json'
# )

bucket = storage_client.bucket(BUCKET_NAME)
blob = bucket.blob('iowa_forecasting_artifacts/categorical_mapping.hdf')
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
blob = bucket.blob('iowa_forecasting_artifacts/model_test.pkl')
blob.upload_from_filename('model_test.pkl')
