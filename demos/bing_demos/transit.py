# Location and Area Types: https://docs.microsoft.com/en-us/bingmaps/rest-services/common-parameters-and-types/location-and-area-types
# Routes: https://docs.microsoft.com/en-us/bingmaps/rest-services/routes/calculate-a-route

import json
import datetime
import requests
from yaml import safe_load

BING_API_CREDENTIALS = "bing.key.yaml"
BING_API_KEY=None

def get_api_key_from_file(filename=BING_API_CREDENTIALS):
    with open(filename, 'r') as config_file:
        config = safe_load(config_file)
    return config["queryKey"]

def get_point_from_location_query(query):
    url = "http://dev.virtualearth.net/REST/v1/Locations"
    params = {
        "query": query,
        "inclnb": 1,
        "incl": "queryparse",
        "maxResults": 5,
        "key": BING_API_KEY
    }

    coords = requests.get(url, params).json()["resourceSets"][0]["resources"][0]["point"]["coordinates"]

    return [str(item) for item in coords]

def get_bing_formatted_current_time():
    now = datetime.datetime.now()

    date = now.strftime("%m/%d/%y")
    time = now.strftime("%H:%M:%S")
    date_time_str = date + " " + time

    print("Time now is: " + date_time_str)
    return date_time_str


if __name__ == "__main__":

    BING_API_KEY = get_api_key_from_file()

    while True:
        source = input("Enter the source address: ").strip()
        destination = input("Enter the destination address: ").strip()


        source_point = get_point_from_location_query(source)
        destination_point = get_point_from_location_query(destination)

        url = "http://dev.virtualearth.net/REST/v1/Routes/Transit"
        params = {
            "wayPoint.1": ",".join(source_point),
            "wayPoint.2": ",".join(destination_point),
            "distanceUnit": "Mile",
            "datetime": get_bing_formatted_current_time(),
            "timeType": "Departure",
            "key": BING_API_KEY
        }

        response_dict = requests.get(url, params).json()

        print(json.dumps(response_dict, indent=2, sort_keys=True))