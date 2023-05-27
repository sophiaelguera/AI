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

def time_to_mins_past_midnight(time_str):
    if pd.isnull(time_str) or not time_str:
        return np.nan
    hours, mins = map(int, time_str.split(':'))
    return 60*hours + mins


def process_journey(journey_df):
    df = pd.DataFrame(journey_df[1:], columns=['rid','tpl','pta','ptd','wta','wtp','wtd','arr_et','arr_wet','arr_atRemoved','pass_et','pass_wet','pass_atRemoved','dep_et','dep_wet','dep_atRemoved','arr_at','pass_at','dep_at','cr_code','lr_code'])
    desired_columns = ['tpl', 'pta', 'arr_at']
    df_cleaned = df[desired_columns].copy()

    df_cleaned = df_cleaned.replace('', pd.NA)
    df_cleaned = df_cleaned.dropna(how='any')

    for col in ['pta', 'arr_at']:
        df_cleaned[col] = df_cleaned[col].apply(time_to_mins_past_midnight)

    df_cleaned['arr_delay'] = df_cleaned['arr_at'] - df_cleaned['pta']

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





def database_generator():
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

    label_encoder = LabelEncoder()
    database['tpl'] = label_encoder.fit_transform(database['tpl'])

    tpl_dict = dict(zip(label_encoder.classes_, label_encoder.transform(label_encoder.classes_)))

    X = database[['tpl', 'arr_delay']]
    exc_cols = ['tpl', 'pta', 'ptd', 'arr_delay', 'dep_delay', 'dep_at', 'arr_at']
    sel_cols = database.columns.difference(exc_cols)
    y = database[sel_cols]

    scaler = StandardScaler()

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.2, random_state = 0)

    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)

    param_grid = {'n_neighbors': np.arange(1, 10)}
    knn = KNeighborsRegressor()
    knn_cv = GridSearchCV(knn, param_grid, cv=5)
    knn_cv.fit(X_train_scaled, y_train)
    print("Best Params for KNN: ", knn_cv.best_params_)
    joblib.dump(knn_cv, 'knn_model.pkl')
    tpl_dict = {k: int(v) for k, v in tpl_dict.items()}
    with open('tpl_dict.txt', 'w') as file:
        json.dump(tpl_dict, file)


knn_generator()