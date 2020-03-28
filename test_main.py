import pytest
from main import *


def get_test_load_data():
        return ['data_1k.json', 'data_2k.json', 'data_5k.json', 'data_10k.json']

@pytest.mark.parametrize('data', get_test_load_data())
def test_load_data_type(data):
    assert type(load_data(data)) is list

@pytest.mark.parametrize('data', get_test_load_data())
def test_load_data_content_type(data):
    results = load_data(data)
    assert type(results[0]) is dict

def get_convert_epoch_to_min_data():
    return [(1585399267, 26423321), (1585332267, 26422204), (1585329267, 26422154), (1585499267, 26424987)]

@pytest.mark.parametrize('timestamp, expected', get_convert_epoch_to_min_data())
def test_convert_epoch_to_min(timestamp, expected):
    assert convert_epoch_to_minutes(timestamp) == expected

@pytest.mark.parametrize('timestamp, expected', get_convert_epoch_to_min_data())
def test_convert_epoch_to_min_type(timestamp, expected):
    assert type(convert_epoch_to_minutes(timestamp)) is int

def get_calculate_moving_average_data():
    return [(10, 7, 5, 9.4), (100, 37, 15, 95.8), (33.7, 67, 39, 34.55), (61.59, 27, 17, 59.56)]

@pytest.mark.parametrize('current_average, new_value, num_samples, expected', get_calculate_moving_average_data())
def test_calculate_moving_average(current_average, new_value, num_samples, expected):
    assert calculate_moving_average(current_average, new_value, num_samples) == expected