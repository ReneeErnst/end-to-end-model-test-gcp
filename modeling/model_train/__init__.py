import pandas as pd

from sklearn.ensemble import RandomForestRegressor


def split_train_test(
        df: pd.DataFrame,
        months_split_var: str,
        months: int
):
    """
    Function to split train and test data
    :param df: passing in pandas dataframe
    :param months_split_var: variable used to split data by months
    :param months: used to determine where to split test and train
        (typically 24)
    :return: train_df, test_df: train and test DataFrames
    :rtype: train_df, test_df: (pd.DataFrame, pd.DataFrame)
    """
    # df_rfr_split = df[df[rfr_split_var] == rfr_split_level]

    split_month = df[months_split_var].max() - months

    train_df = df[
        df[months_split_var] <= split_month
    ]
    test_df = df[
        df[months_split_var] > split_month
    ]
    return train_df, test_df


def create_xy_ind(df, y_column, x_columns):
    """
    Creates the x and y inputs in format needed for random forest
    :param df: Pandas dataframe with model input data
    :param y_column: Value we are predicting for
    :param x_columns: Features used to predict outcome variable (y)
    :return: Values as needed for input into random forest model
    """
    y = df[y_column].values
    
    features = df[x_columns]
    
    x = features.values
    return [x, y]


def feature_importances(rf, x_cols, score):
    """
    Creates dataframe with feature importances from model run
    :param rf: random forest model
    :param x_cols: Features utilized in model
    :param score: Output from random forest model
    :return: Dataframe with feature importance results
    """
    feature_importance = list(
        zip(x_cols, rf.feature_importances_)
    )
    df_feature_importance = pd.DataFrame(feature_importance, columns=[
        'feature_cd',
        'importance_nbr'
    ])
    df_feature_importance['r2_nbr'] = score
    return df_feature_importance


def fit_model(
        y_col,
        x_cols,
        actual,
        trees=100,
        leaves=1,
        jobs=1,
        importances=True
 ):
    """
    Creates random forest model and importances if importances=True
    :param y_col: Variable model is predicting for
    :param x_cols: Features used in model
    :param actual: Actuals data
    :param trees: Number of trees to run
    :param leaves: Min size of rfr leaf
    :param jobs: Number of jobs to run in parallel
    :param importances: Indicator for if importances should be calculated
    :return: Random forest model and importances if indicated
    """
    if len(actual) > 0:
        x_train, y_train = create_xy_ind(actual, y_col, x_cols)

        rf = RandomForestRegressor(
            random_state=1,
            n_estimators=trees,
            min_samples_leaf=leaves,
            n_jobs=jobs
        )
        rf.fit(x_train, y_train)

        score = rf.score(x_train, y_train)
        # only calculate importances when needed (non-category model_
        if importances:
            importances = feature_importances(rf, x_cols, score)
            return rf, importances
        else:
            return rf
    else:
        if importances:
            return None, None
        else:
            return None

        
def model_predict(rf, df_plan, y_col, x_cols):
    """
    Outputs predicted values based on model
    :param rf: Random forest model
    :param df_plan: Plan data that we want to create predictions for
    :param y_col: Variable we are predicting for
    :param x_cols: List of features used by model
    :return: Dataframe with predictions on plan data
    """
    df_results = df_plan.copy(deep=True)

    df_features = df_plan.copy(deep=True)
    df_features = df_features[x_cols]
    x_predict = df_features.values
    estimate = rf.predict(x_predict)

    col_predicted = 'predicted_{}'.format(y_col)
    df_results[col_predicted] = estimate

    return df_results
