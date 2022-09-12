from datetime import datetime
from dateutil.relativedelta import relativedelta

from prefect import flow

import score

@flow
def ride_duration_prediction_backfill():
    start_date = datetime(year=2022, month=4, day=1)
    end_date = datetime(year=2022, month=8, day=1)

    d = start_date

    while d <= end_date:
        score.ride_duration_prediction(run_id = '8ed0e2cc3fe34622b9b3101c82d4add4', run_date = d)

        d = d + relativedelta(months =  1)

if __name__ == '__main__':
    ride_duration_prediction_backfill()