import mlflow

# mlflow.set_tracking_uri(uri='http://localhost:5000')

run_id = '9fc54afcb89441829aa9057175c279a8'
logged_model = './mlruns/4/9fc54afcb89441829aa9057175c279a8/artifacts/models'
model_uri = f'runs:/{run_id}/models'
mlflow.pyfunc.load_model(logged_model)
