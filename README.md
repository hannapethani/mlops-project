# mlops-project
Repository for mlops-zoomcamp project

# Problem description
Capital Bikeshare is a bicycle sharing system that serves various areas in the United States. The bikes are owned by the local governments of the areas being served and  There are limited number of vehicles available for sharing among a growing community. 

**This project aims to predict duration (in minutes) of each ride time.**

This information can in turn support updates to the business plan based on predicted ride time:
* Allocate bikes to various areas 
* Change bike models
* Modify pricing plans 
* Forecast future earnings

As this information is not required in real-time, the ML model deployment runs in batch mode. 

## Data source

Capital Bikeshare data was obtained from: https://s3.amazonaws.com/capitalbikeshare-data/index.html

## Files

|File name              |Description                         |
|-----------------------|------------------------------------|
|1 train.py             |Training and validation script      |
|2 score.py             |Batch script                        |
|3 score_deploy.py      |Deploy batch script on Cron schedule|
|4 score_backfill.py    |Backfill predictions from score.py  |
|5 prefect_monitoring.py|Model monitoring metrics            |