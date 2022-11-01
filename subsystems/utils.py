from dotenv import dotenv_values
from subsystems.exceptions import *
import requests

# get environment variables
env_vars = dotenv_values('.env')

# get api key
headers = {
    "X-TBA-Auth-Key": env_vars['X-TBA-Auth-Key']
}

def get_data(endpoint):
    response = requests.get(endpoint, headers = headers)
    data = response.json()
    if isinstance(data, dict) and "Error" in data.keys():
        raise TeamFetchException(data["Error"])
    return data