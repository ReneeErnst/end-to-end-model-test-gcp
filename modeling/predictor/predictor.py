"""Predictions in GCP AI Platform"""
import os
import pickle

import pandas as pd


class Predictor:
    """
    Predictor to be used in AI Platform to get model predictions
    """
    def __init__(self, model, mapping_df):
        """
        Artifacts needed to make model predictions
        :param model: sklearn random forest regression model object
        :param mapping_df: dataframe with category mapping created during model
        training
        """
        self.model = model
        self.mapping_df = mapping_df

    # noinspection PyUnusedLocal
    def predict(self, instances, **kwargs):
        """
        Create custom prediction routine
        :param instances: A list of prediction input instances
        :param kwargs: dictionary of keyword args provided as additional fields
        on the predict request body. but not currently used.
        :return: A list of outputs containing the prediction results. This list
        must be JSON serializable.
        """
        # Convert passed data into a dataframe
        df = pd.DataFrame(instances)

        # Apply category mapping to that dataframe
        cat_map_columns = list(self.mapping_df.columns)
        clean_cat_map_columns = [
            column for column in cat_map_columns if '_enc' not in column]

        for var in clean_cat_map_columns:
            df_clean_cat_mapping = self.mapping_df[[
                var, f'{var}_enc']].drop_duplicates()

            df = df.merge(
                df_clean_cat_mapping,
                on=var,
                how='left'
            )

        features = [
            'city_enc',
            'county_number_enc',
            'category_enc',
            'store_number_enc',
            'item_number_enc',
            'year',
            'month',
            'day'
        ]

        estimate = self.model.predict(df[features].values)

        return estimate

    @classmethod
    def from_path(cls, model_dir):
        """
        Creates an instance of Predictor using the given path.
        :param model_dir: The local directory that contains the exported model
        file along with any additional files uploaded when creating the version
        resource.
        :return: An instance implementing this Predictor class.
        """
        model_path = os.path.join(model_dir, 'model_test.pkl')
        mapping_path = os.path.join(model_dir, 'category_mapping.hdf')

        # Model
        with open(model_path, 'rb') as f:
            model = pickle.load(f)

        # Load category mapping file
        with open(mapping_path, 'rb') as f:
            mapping_df = pd.read_hdf(
                f,
                'df_categorical_mapping'
            )

        return cls(model, mapping_df)
