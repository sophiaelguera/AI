import csv
import os
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.neighbors import KNeighborsRegressor
import numpy as np
from sklearn.preprocessing import StandardScaler
import joblib
from sklearn.model_selection import GridSearchCV
import json
import sys


def time_to_mins_past_midnight(time_str):  # function to convert from HH:MM time to mins past midnight
    if pd.isnull(time_str) or not time_str:
        return np.nan
    hours, mins = map(int, time_str.split(':'))
    return 60*hours + mins


def process_journey(journey_df):
    df = pd.DataFrame(journey_df[1:], columns=['rid', 'tpl', 'pta', 'ptd', 'wta', 'wtp', 'wtd', 'arr_et', 'arr_wet',
                                               'arr_atRemoved', 'pass_et','pass_wet', 'pass_atRemoved', 'dep_et',
                                               'dep_wet', 'dep_atRemoved', 'arr_at', 'pass_at', 'dep_at', 'cr_code',
                                               'lr_code'])

    desired_columns = ['tpl', 'pta', 'arr_at']
    df_cleaned = df[desired_columns].copy()  # filters out unwanted data

    df_cleaned = df_cleaned.replace('', pd.NA)  # replaces any empty data with NaN
    df_cleaned = df_cleaned.dropna(how='any')  # drops rows with NaN data

    for col in ['pta', 'arr_at']:
        df_cleaned[col] = df_cleaned[col].apply(time_to_mins_past_midnight)  # converts time data to mins past midnight

    df_cleaned['arr_delay'] = df_cleaned['arr_at'] - df_cleaned['pta']  # creates delay col using arr_at and pta

    for i in range(len(df_cleaned)):
        tpl = df_cleaned.iloc[i]['tpl']
        df_cleaned[tpl] = df_cleaned.iloc[i]['arr_at'] - df_cleaned.iloc[i]['pta']

    exc_cols = ['tpl', 'pta', 'arr_at']
    sel_cols = df_cleaned.columns.difference(exc_cols)
    df_cleaned = df_cleaned.loc[~(df_cleaned[sel_cols].abs() > 60).any(axis=1)]

    if df_cleaned.empty:
        return None
    else:
        return df_cleaned


def database_generator():  # grabs and processes all the weymouth csvs
    processed_dfs = []
    keyword = "WEYMTH"
    for filename in os.listdir("WEYMTH_DATA"):
        file_path = os.path.join("WEYMTH_DATA", filename)
        print(file_path)
        with open(file_path) as file_obj:
            dataset = []
            reader_obj = csv.reader(file_obj)
            for row in reader_obj:
                if keyword in row:
                    dataset.append(row)
                    x = process_journey(dataset)
                    if x is not None:
                        processed_dfs.append(x)
                    dataset = []
                dataset.append(row)
    return processed_dfs


def knn_generator():
    processed_dfs = database_generator()
    database = pd.concat(processed_dfs, ignore_index=True)
    database = database.fillna(0)

    label_encoder = LabelEncoder()  # initialise label encoder
    database['tpl'] = label_encoder.fit_transform(database['tpl'])  # creates unique label for each tpl

    tpl_dict = dict(zip(label_encoder.classes_, label_encoder.transform(label_encoder.classes_)))
    # creates tpl_dict for DelayPrediction to use model correctly

    X = database[['tpl', 'arr_delay']]  # relevant attributes
    exc_cols = ['tpl', 'pta', 'ptd', 'arr_delay', 'dep_delay', 'dep_at', 'arr_at']
    sel_cols = database.columns.difference(exc_cols)
    y = database[sel_cols]

    scaler = StandardScaler()  # initialise scaler

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.2, random_state = 0)
    #  create training set and testing set

    X_train_scaled = scaler.fit_transform(X_train)  # scale features to standardise them
    X_test_scaled = scaler.transform(X_test)

    hyper_parameters = {'n_neighbors': np.arange(1, 10)}
    knn = KNeighborsRegressor()
    knn_cv_applied = GridSearchCV(knn, hyper_parameters, cv=5)  # performs hyperparameter tuning our model by utilising
    #  5-fold cross-validation
    knn_cv_applied.fit(X_train_scaled, y_train)
    joblib.dump(knn_cv_applied, 'knn_model.pkl')  # saves model to .pkl
    tpl_dict = {k: int(v) for k, v in tpl_dict.items()}
    with open('tpl_dict.txt', 'w') as file:  # writes tpl_dict to a .txt
        json.dump(tpl_dict, file)


knn_generator()