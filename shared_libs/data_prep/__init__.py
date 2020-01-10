import pandas as pd

from google.cloud import storage


def category_columns(
        df: pd.DataFrame,
        cat_columns: list
) -> pd.DataFrame:
    """
    Create new pandas factorized columns for list of category columns provided.
    New columns created end in _enc. Drop original columns except for those in
    the cat_keep_columns list

    :param df: Pandas Dataframe to perform operation on
    :param cat_columns: List of columns to convert to category
    :return: df_out: Dataframe with cleaned up data
    """

    df_out = df.copy()
    
    save_list = cat_columns.copy()

    for column in cat_columns:
        df_out[column] = df_out[column].astype('category')
        enc_col_nm = column + '_enc'
        save_list.append(enc_col_nm)
        df_out[column] = df_out[column].cat.add_categories('Unknown')
        df_out[column].fillna('Unknown', inplace=True)
        df_out[enc_col_nm] = pd.factorize(df_out[column])[0]
    
    df_map = df_out[save_list]
    
    return df_out, df_map


def upload_blob(bucket_name, source_file_name, destination_blob_name):
    """Uploads a file to the bucket."""
    storage_client = storage.Client()
    bucket = storage_client.get_bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)

    blob.upload_from_filename(source_file_name)

    print('File {} uploaded to {}.'.format(
      source_file_name,
      destination_blob_name))
    
    return True