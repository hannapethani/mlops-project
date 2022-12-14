import os
import sys
import uuid
import pickle
from datetime import datetime

import mlflow
import pandas as pd
from prefect import flow, task, get_run_logger
from hyperopt import STATUS_OK, Trials, hp, tpe, fmin
from hyperopt.pyll import scope
from prefect.context import get_run_context
from sklearn.metrics import mean_squared_error
from sklearn.pipeline import make_pipeline
from sklearn.linear_model import Ridge
from dateutil.relativedelta import relativedelta
from sklearn.feature_extraction import DictVectorizer


def generate_uuids(n):
    ride_ids = []
    for i in range(n):
        ride_ids.append(str(uuid.uuid4()))
    return ride_ids


def read_dataframe(filename: str):

    df = pd.read_csv(filename)

    df['started_at'] = pd.to_datetime(df['started_at'])
    df['ended_at'] = pd.to_datetime(df['ended_at'])

    df['duration'] = df['ended_at'] - df['started_at']
    df.duration = df.duration.apply(lambda td: td.total_seconds() / 60)
    df = df[(df.duration >= 1) & (df.duration <= 120)]

    df[['rideable_type', 'start_station_id', 'end_station_id']] = df[
        ['rideable_type', 'start_station_id', 'end_station_id']
    ].fillna(-1)

    df['ride_id'] = generate_uuids(len(df))

    return df


def prepare_dictionaries(df: pd.DataFrame):

    categorical = ['rideable_type', 'start_station_id', 'end_station_id']
    df[categorical] = df[categorical].astype(str)

    dicts = df[categorical].to_dict(orient='records')

    return dicts


def load_model(run_id):

    experiment = mlflow.get_experiment_by_name('bikeshare-experiment')
    # experiment_id = experiment.experiment_id
    print(experiment)
    # print(f'Experiment id: {experiment_id}')

    logged_model = f'./mlruns/{run_id}/artifacts/models'
    model = mlflow.pyfunc.load_model(logged_model)

    return model


def preprocessor():

    with open('models/preprocessor.b', 'rb') as f_in:
        processor = pickle.load(f_in)

    return processor


def save_results(df, y_pred, run_id, output_file):

    df_result = pd.DataFrame()
    df_result['ride_id'] = df['ride_id']
    df_result['started_at'] = df['started_at']
    df_result['start_station_id'] = df['start_station_id']
    df_result['end_station_id'] = df['end_station_id']
    df_result['actual_duration'] = df['duration']
    df_result['predicted_duration'] = y_pred
    df_result['diff'] = df_result['actual_duration'] - df_result['predicted_duration']
    df_result['model_version'] = run_id

    df_result.to_csv(output_file, index=False)


@task
def apply_model(input_file, run_id, output_file):

    logger = get_run_logger()

    logger.info(f'reading the data from {input_file}...')
    df = read_dataframe(input_file)
    dicts = prepare_dictionaries(df)
    transformer = preprocessor()
    processed_dicts = transformer.transform(dicts)

    logger.info(f'loading the model with RUN_ID = {run_id}...')
    model = load_model(run_id)

    logger.info('applying the model...')
    y_pred = model.predict(processed_dicts)

    logger.info(f'saving the result to {output_file}...')

    save_results(df, y_pred, run_id, output_file)

    return output_file


def get_paths(run_date, run_id):

    prev_month = run_date - relativedelta(months=1)
    year = prev_month.year
    month = prev_month.month

    input_file = f'./data/{year:04d}{month:02d}-capitalbikeshare-tripdata.csv'
    output_file = f'./bikeshare-duration-prediction/{year:04d}/{month:02d}/{run_id}.csv'

    return input_file, output_file


@flow
def ride_duration_prediction(run_id: str, run_date: datetime = None):

    if run_date is None:
        ctx = get_run_context()
        run_date = ctx.flow_run.expected_start_time

    input_file, output_file = get_paths(run_date, run_id)

    apply_model(input_file=input_file, run_id=run_id, output_file=output_file)


def run():

    year = int(sys.argv[1])  # 2022
    month = int(sys.argv[2])  # 6

    run_id = sys.argv[3]  # abd6a134d1e546c8a0a1ea124f545a6d

    ride_duration_prediction(
        run_id=run_id, run_date=datetime(year=year, month=month, day=1)
    )


if __name__ == '__main__':
    run()
