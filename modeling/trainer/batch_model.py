"""Model Training"""
import argparse
import sys
import pickle

import pandas as pd
from google.cloud import bigquery
from google.cloud import storage

from modeling import aip_example


def parse():
    """
    Arguments to be passed as needed for running the model
    :return: parser for needed arguments
    """
    parser = argparse.ArgumentParser()

    # --job-dir required by AI Platform Jobs
    parser.add_argument('--job-dir')

    parser.add_argument('--run_location')
    parser.add_argument('--bucket')
    parser.add_argument('--project')
    parser.add_argument('--dataset_table')

    return parser.parse_args(sys.argv[1:])


def run():
    """

    :return:
    """
    args = parse()

    run_location = args.run_location
    bucket_name = args.bucket
    project = args.project
    bq_table = args.dataset_table

    # Get the data
    if run_location == 'local':
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

    # Train and Test Data
    df_train_rfr, df_test_rfr = aip_example.split_train_test(
        df_cat,
        'month',
        3
    )

    print('Length of Training Data: ', len(df_train_rfr))
    print('Length of Test Data: ', len(df_test_rfr))

    # Create model object and importances
    rfr_model, importances = aip_example.fit_model(
        y_col,
        x_cols,
        df_train_rfr,
        trees=150,
        leaves=5
    )

    # Model results
    df_results = aip_example.model_predict(
        rfr_model,
        df_test_rfr,
        y_col,
        x_cols
    )

    # Save model object out for potential future use
    pickle.dump(
        rfr_model,
        open('model.pkl', 'wb')
    )

    # Save mapping and model object files to GCS and results to BigQuery
    if run_location == 'local':
        print('Running Locally - No need to save out to GCS')
    else:
        storage_client = storage.Client()

        bucket = storage_client.bucket(bucket_name)

        # Save mapping file
        blob = bucket.blob(
            'ai_platform_test/iowa_forecasting_artifacts/'
            'categorical_mapping.pkl')
        blob.upload_from_filename('categorical_mapping.pkl')

        # Save model file
        blob = bucket.blob(
            'ai_platform_test/iowa_forecasting_artifacts/model.pkl')
        blob.upload_from_filename('model.pkl')

        # Save results to BigQuery
        df_results.to_gbq(bq_table, project)


if __name__ == '__main__':
    run()
