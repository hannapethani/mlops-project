# pylint: disable=duplicate-code

import pandas as pd

from score import prepare_dictionaries


def test_prepare_dictionaries():

    data_dictionary = {
        'ride_id': [' '],
        'rideable_type': ['electric'],
        'started_at': [' '],
        'ended_at': [' '],
        'start_station_name': [' '],
        'start_station_id': [50],
        'end_station_name': [' '],
        'end_station_id': [100],
        'start_lat': [' '],
        'start_lng': [' '],
        'end_lat': [' '],
        'end_lng': [' '],
        'member_casual': [' '],
    }

    df = pd.DataFrame(data_dictionary)

    actual_features = prepare_dictionaries(df)

    expected_features = {
        'ride_id': [' '],
        'rideable_type': ['electric'],
        'started_at': [' '],
        'ended_at': [' '],
        'start_station_name': [' '],
        'start_station_id': [50],
        'end_station_name': [' '],
        'end_station_id': [100],
        'start_lat': [' '],
        'start_lng': [' '],
        'end_lat': [' '],
        'end_lng': [' '],
        'member_casual': [' '],
    }

    assert actual_features == prepare_dictionaries(expected_features)
