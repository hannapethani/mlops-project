import pandas as pd

import score

data_dictionary = {
           'rideable_type': ['electric'],
           'start_station_id': [50],
           'end_station_id': [100],
       }
   
df = pd.DataFrame(data_dictionary)

print(df)

actual_features = add_features(df)