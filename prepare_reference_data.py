import pandas as pd

data_files = ['./data/202203-capitalbikeshare-tripdata.csv', './data/202204-capitalbikeshare-tripdata.csv']
output_file = './data/2022-03to04-capitalbikeshare-tripdata.csv'

df = pd.DataFrame()
for file in data_files:
    data = pd.read_csv(file)
    df = pd.concat([data, df], ignore_index=True)

df.to_csv(
    output_file,
    compression=None,
    index=False
)