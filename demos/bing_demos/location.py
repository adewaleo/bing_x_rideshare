# Location from Query: https://docs.microsoft.com/en-us/bingmaps/rest-services/locations/find-a-location-by-query

import json
import requests
from yaml import safe_load

BING_API_CREDENTIALS = "bing.key.yaml"

def get_api_key_from_file(filename=BING_API_CREDENTIALS):
    with open(filename, 'r') as config_file:
        config = safe_load(config_file)
    return config["queryKey"]


if __name__ == "__main__":

    BING_API_KEY = get_api_key_from_file()

    while True:
        query = input("Enter the location: ").strip()

        url = "http://dev.virtualearth.net/REST/v1/Locations"
        params = {
            "query": query,
            "inclnb": 1,
            "incl": "queryparse",
            "maxResults": 5,
            "key": BING_API_KEY
        }

        response_dict = requests.get(url, params).json()

        print(json.dumps(response_dict, indent=2, sort_keys=True))


