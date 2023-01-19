import json

DISK_PATH = "/var/data"  # "tests/test_data"
SAMPLE_RATE = 48000
GOOGLE_APPLICATION_CREDENTIALS = "doordashassistant-db7ef663c57b.json"
with open('doordashprivate.json') as f:
    HEADERS = json.load(f)
MENU = ['fries', 'burger', 'chicken']  # ["cheese", "pepperoni"]  # ["sprite", "gatorade"]
STORE = 'mcdonalds'  # "joe"  # "711"
PASSWORD = "598"
