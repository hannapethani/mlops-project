from ast import main
from prefect.deployments import DeploymentSpec
from prefect.orion.schemas.schedules import CronSchedule
from prefect.flow_runners import SubprocessFlowRunner

DeploymentSpec(
    flow_location = 'score.py',
    name = 'bike-rental-experiment',
    parameters = {'run_id': 'ef2dbfbed701410eb4245d5549390ab1'},
    schedule = CronSchedule(cron = '0 3 6 * *'), # 3am on the 6th of every month 
    flow_storage = 'cf5d442f-0a41-4b81-aa44-f51b6821d741',
    flow_runner = SubprocessFlowRunner(),
    tags = ['ml']
)