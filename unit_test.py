# pylint: disable=duplicate-code

import pandas as pd

from score import prepare_dictionaries


def test_prepare_dictionaries():

    data_dictionary = {
        'rideable_type': ['electric'],
        'start_station_id': [50],
        'end_station_id': [100],
    }

    df = pd.DataFrame(data_dictionary)
    print(df)

    actual_features = prepare_dictionaries(df)

    expected_features = {
        'rideable_type': ['electric'],
        'start_station_id': [50],
        'end_station_id': [100],
    }

    expected_features_df = pd.DataFrame(expected_features)
    
    assert actual_features == prepare_dictionaries(expected_features)
