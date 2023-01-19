import io

import pytest
import requests
from scipy.io import wavfile

TEST_PROD = False


def pytest_configure():
    if TEST_PROD:
        pytest.url = 'https://doordash-assistant-api.onrender.com/api/'
    else:
        pytest.url = 'http://127.0.0.1:5000/api/'


def prepare_data(path=""):
    fs, data = wavfile.read(path)
    data_bytes = io.BytesIO()
    wavfile.write(data_bytes, fs, data)
    return data_bytes.read()


def post_stream(data, endpoint="transcribe"):
    r = requests.post(url=pytest.url + endpoint, data=data,
                      headers={'Content-Type': 'application/octet-stream'})
    return r
