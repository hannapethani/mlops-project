import pandas as pd

import pickle

from sklearn.feature_extraction import DictVectorizer
from sklearn.linear_model import Ridge
from sklearn.metrics import mean_squared_error

import mlflow
from mlflow.tracking import MlflowClient

from hyperopt import fmin, tpe, hp, STATUS_OK, Trials
from hyperopt.pyll import scope

from prefect import flow, task
from prefect.task_runners import SequentialTaskRunner

from datetime import timedelta

@task
def read_dataframe(filename):

    df = pd.read_csv(filename)
    
    df['started_at'] = pd.to_datetime(df['started_at'])
    df['ended_at'] = pd.to_datetime(df['ended_at'])

    df['duration'] = df['ended_at'] - df['started_at']
    df.duration = df.duration.apply(lambda td: td.total_seconds() / 60)

    df = df[(df.duration >= 1) & (df.duration <= 120)]

    df[['rideable_type', 'start_station_id', 'end_station_id']] = df[['rideable_type', 'start_station_id', 'end_station_id']].fillna(-1)
    categorical = ['rideable_type', 'start_station_id', 'end_station_id']

    df[categorical] = df[categorical].astype(str)
    
    return df

@task
def add_features(df_train, df_val):

    print(f'Length - training dataset: {len(df_train)}')
    print(f'Length - validation dataset: {len(df_val)}')

    categorical = ['rideable_type', 'start_station_id', 'end_station_id']

    dv = DictVectorizer()

    train_dicts = df_train[categorical].to_dict(orient = 'records')
    X_train = dv.fit_transform(train_dicts)

    val_dicts = df_val[categorical].to_dict(orient = 'records')
    X_val = dv.transform(val_dicts)

    target = 'duration'
    y_train = df_train[target].values
    y_val = df_val[target].values

    return X_train, X_val, y_train, y_val, dv

@task
def train_model_search(X_train, y_train, X_val, y_val):

    def objective(params):
        with mlflow.start_run():

            mlflow.set_tag('model', 'Ridge')
            mlflow.log_params(params)

            lr = Ridge(**params)
            lr.fit(X_train, y_train)
            y_pred = lr.predict(X_val)
            rmse = mean_squared_error(y_val, y_pred, squared=False)
            mlflow.log_metric('rmse', rmse)

            print(f'Parameters: {params}, RMSE: {rmse}')

        return {'loss': rmse, 'status': STATUS_OK}

    intercepts = [True, False]

    search_space = {
        'fit_intercept': hp.choice('fit_intercept', intercepts),
        'alpha': hp.loguniform('alpha', -3, 0)
    }

    best_result = fmin(
        fn=objective,
        space=search_space,
        algo=tpe.suggest,
        max_evals=10,
        trials=Trials()
    )

    return best_result

@task
def train_best_model(X_train, y_train, X_val, y_val, dv, best_result):

    with mlflow.start_run():
        
        mlflow.set_tag('developer', 'hanna')

        print(f'Best result: {best_result}')
        # log best parameters
        mlflow.log_params(best_result)

        lr = Ridge(**best_result)
        lr.fit(X_train, y_train)
        y_pred = lr.predict(X_val)

        rmse = mean_squared_error(y_val, y_pred, squared=False)
        print(f'RMSE: {rmse}')
        mlflow.log_metric('rmse', rmse)

        # log the model and register as version 1
        with open('models/lin_reg.bin', 'wb') as f_out:
            pickle.dump((dv, lr), f_out)
        mlflow.sklearn.log_model(
            lr, 
            artifact_path = 'models', 
            registered_model_name='sklearn-ridge-model'
            )

        with open('models/preprocessor.b', 'wb') as f_out:
            pickle.dump(dv, f_out)
        mlflow.log_artifact('models/preprocessor.b', artifact_path='preprocessor')

        print(f'default artifacts URI: {mlflow.get_artifact_uri()}')

@flow(task_runner=SequentialTaskRunner())
def main(train_path: str = './data/202201-capitalbikeshare-tripdata.csv',
            val_path: str = './data/202202-capitalbikeshare-tripdata.csv'):

    mlflow.set_tracking_uri('sqlite:///mlflow.db')
    mlflow.set_experiment('bike-rental-experiment')

    X_train = read_dataframe(train_path)
    X_val = read_dataframe(val_path)

    X_train, X_val, y_train, y_val, dv = add_features(X_train, X_val).result()
    best_result = train_model_search(X_train, y_train, X_val, y_val)
    train_best_model(X_train, y_train, X_val, y_val, dv, best_result)

main()