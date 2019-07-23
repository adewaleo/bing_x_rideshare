# Location from Query: https://docs.microsoft.com/en-us/bingmaps/rest-services/locations/find-a-location-by-query
# Location and Area Types: https://docs.microsoft.com/en-us/bingmaps/rest-services/common-parameters-and-types/location-and-area-types
# Routes: https://docs.microsoft.com/en-us/bingmaps/rest-services/routes/calculate-a-route

import json
import requests
from yaml import safe_load
from util import dict_to_pretty_str

BING_API_CREDENTIALS = "bing.key.yaml"

def _get_api_key_from_file(filename=BING_API_CREDENTIALS):
    with open(filename, 'r') as config_file:
        config = safe_load(config_file)
    return config["queryKey"]

class BingApiError(Exception):
    pass

class BingLocation(object):
    def __init__(self, point, address):
        self.point_list = point  # list of latitude and longiturde
        self.point_as_str = ",".join(self.point_list)
        self.address_str = address

    @staticmethod
    def from_location_resource(resource):
        try:
            point = resource["point"]["coordinates"]
            address = resource["address"]["formattedAddress"]
        except KeyError:
            raise BingApiError("The following location does not has the expected format:\n{}"
                               .format(dict_to_pretty_str(resource)))

        return BingLocation(point=point, address=address)

    @staticmethod
    def multiple_from_location_resources(resources, include_confidence=True):
        """

        :param resources:
        :param include_confidence:
        :return: list of tuples of bing location and confidence from high = 2 to low = 0 or
                 list of bing locations
        """
        results = []

        try:
            for loc in resources:
                bing_location = BingLocation.from_location_resource(loc)

                if not include_confidence:
                    results.append(bing_location)
                else:
                    confidence = loc["confidence"].lower()
                    if confidence == "high":
                        confidence = 2
                    elif confidence == "medium":
                        confidence = 1
                    elif confidence == "low":
                        confidence = 0
                    else:
                        raise BingApiError("Unknown Confidence:\n{}".format(dict_to_pretty_str(loc)))
                    results.append((bing_location, confidence)) # append the tuple

        except KeyError:
            raise BingApiError("The following location does not has the expected format:\n{}"
                                   .format(dict_to_pretty_str(loc)))

        return results





class BingMaps(object):
    def __init__(self, api_key=None):
        self.key = api_key or _get_api_key_from_file()

    def _get_locations_for_query(self, location_str):
        url = "http://dev.virtualearth.net/REST/v1/Locations"
        params = {
            "query": location_str,
            "inclnb": 1,
            "key": self.key
        }
        response_dict = requests.get(url, params).json()
        locations = response_dict["resourceSets"][0]["resources"]
        return locations

    def get_location_from_string(self, location_str):
        """
        :param location_str: Place we are trying to get concrete location for
        :type location_str: str
        :return: Returns location of highest confidence if one exists
        :rtype: BingLocation
        :raises: BingApiError if no valid location was returned
        """
        locations = self._get_locations_for_query(location_str)

        if not locations:
            raise BingApiError("No locations match the query string")

        return BingLocation.from_location_resource(locations[0])

    def get_possible_locations_from_string(self, location_str):
        """
        :param location_str: Place we are trying to get concrete location for
        :type location_str: str
        :return: Returns list of tuples of location of highest confidence alongside their
        :rtype: [BingLocation, confidence_as_int]
        :raises: BingApiError if no valid location was returned
        """
        locations = self._get_locations_for_query(location_str)
        if not locations:
            raise BingApiError("No locations match the query string")

        return BingLocation.multiple_from_location_resources(locations)





