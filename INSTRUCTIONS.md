# Instructions to running this ML project

## Requirements
1. Dependencies found in: ```requirements.txt```
2. ```./data``` folder containing these files from https://s3.amazonaws.com/capitalbikeshare-data/index.html: 
    1. 202201-capitalbikeshare-tripdata.csv
    2. 202202-capitalbikeshare-tripdata.csv
    3. 202203-capitalbikeshare-tripdata.csv
    4. 202204-capitalbikeshare-tripdata.csv
    5. 202205-capitalbikeshare-tripdata.csv
    6. 202206-capitalbikeshare-tripdata.csv
    7. 202207-capitalbikeshare-tripdata.csv
3. ```./mlruns``` folder
4. ```./models``` folder
5. For backfill, create subfolders:
    1. ```./bikeshare-duration-prediction/2022/03```
    2. ```./bikeshare-duration-prediction/2022/04```
    3. ```./bikeshare-duration-prediction/2022/05```
    4. ```./bikeshare-duration-prediction/2022/06```
    5. ```./bikeshare-duration-prediction/2022/07```

## How-to

1. Train model ----> ```python train.py```
2. Batch script ----> ```python score.py year month run_id```
    1. E.g. ```python score.py 2022 6 abd6a134d1e546c8a0a1ea124f545a6d```     
3. Deploy batch on Cron schedule ---> ```python score_deploy.py```
4. Backfill ---> ```python score_backfill.py```
5. Monitoring ---> ```python prefect_monitoring.py```