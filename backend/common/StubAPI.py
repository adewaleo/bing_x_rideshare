# -*- coding: utf-8 -*-

import requests
from bing_maps import BingLocation, BingMaps
from yaml import safe_load

BING_API_CREDENTIALS = "bing.key.yaml"


def _get_api_key_from_file(filename=BING_API_CREDENTIALS):
    with open(filename, 'r') as config_file:
        config = safe_load(config_file)
    return config["queryKey"]

class StubAPI(object):
    def __init__(self, api_key=None):
        self.key = api_key or _get_api_key_from_file()

    def _get_locations_for_query(self, location_str):
        url = "http://dev.virtualearth.net/REST/v1/Locations"
        params = {
            "query": location_str,
            "key": self.key
        }
        response_dict = requests.get(url, params).json()
        locations = response_dict["resourceSets"][0]["resources"]
        return locations
        
    def get_matching_locations_for_str(self,location_str):
        """
        :param location_str: Place we are trying to get concrete location for
        :return: Returns list of tuples of bing location with descending confidence
        :rtype: [BingLocation, confidence_as_int]
        """
        address_list = []
        bing_maps = BingMaps()
        address_list = bing_maps.get_possible_locations_from_string(location_str)
        address_list.sort(key=lambda x:x[1],reverse=True)
        return address_list
    