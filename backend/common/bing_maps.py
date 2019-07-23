# Location from Query: https://docs.microsoft.com/en-us/bingmaps/rest-services/locations/find-a-location-by-query
# Location and Area Types: https://docs.microsoft.com/en-us/bingmaps/rest-services/common-parameters-and-types/location-and-area-types
# Routes: https://docs.microsoft.com/en-us/bingmaps/rest-services/routes/calculate-a-route
# RouteData: https://docs.microsoft.com/en-us/bingmaps/rest-services/routes/route-data.

import datetime
import requests
from yaml import safe_load
from util import dict_to_pretty_str, is_correct_type_or_err

BING_API_CREDENTIALS = "bing.key.yaml"

def _get_api_key_from_file(filename=BING_API_CREDENTIALS):
    with open(filename, 'r') as config_file:
        config = safe_load(config_file)
    return config["queryKey"]


class BingApiError(Exception):
    pass


class BingDateTime(object):

    def __init__(self, date_time):
        self.date_time = date_time
        date = self.date_time.strftime("%m/%d/%y")
        time = self.date_time.strftime("%H:%M:%S")
        self.date_time_str = date + " " + time

    def __str__(self):
        return self.date_time_str

    @staticmethod
    def now():
        time_now = datetime.datetime.now()
        return BingDateTime(time_now)


class BingDistance(object):
    def __init__(self, value, unit):
        self.value = value
        self.unit = unit.lower()

        if self.unit != "mile":
            raise ValueError("The unit must be 'mile' or 'Mile'.")


class BingDuration(datetime.timedelta):

    @staticmethod
    def from_value_and_unit(value, unit):
        if unit.lower() == "second":
            return BingDuration(seconds=value)
        if unit.lower() == "minute":
            return BingDuration(minutes=value)
        if unit.lower() == "hour":
            return BingDuration(hours=value)
        if unit.lower() == "day":
            return BingDuration(days=value)
        else:
            raise BingApiError("Error identifying unit: {}".format(unit))



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


class BingDrivingRoute(object):

    def __init__(self, source, dest, distance, travel_duration, departure_date_time=None):
        is_correct_type_or_err(source, BingLocation)
        is_correct_type_or_err(dest, BingLocation)
        is_correct_type_or_err(distance, BingDistance)
        is_correct_type_or_err(travel_duration, BingDuration)
        if departure_date_time:
            is_correct_type_or_err(departure_date_time, BingDateTime)

        self.source = source
        self.dest = dest
        self.distance = distance
        self.travel_duration = travel_duration  # includes traffic time if applicable by API
        self.time_requested = departure_date_time

    @staticmethod
    def from_route_and_request_info(route_resource, source_location, dest_location, departure_date_time=None):
        distance = BingDistance(value=route_resource["travelDistance"], unit=route_resource["distanceUnit"])
        duration = BingDuration.from_value_and_unit(value=route_resource["travelDurationTraffic"], unit=route_resource["durationUnit"])

        return BingDrivingRoute(source_location, dest_location, distance=distance, travel_duration=duration, departure_date_time=None)


class BingMaps(object):
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

    def get_location_from_string(self, location_str):
        """
        Get's most likely address for query string from Bing Maps API and creates location object.

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

    def get_location_from_point(self, latitude, longitude):
        """
        Get Location object from point. This is helpful for getting the address of a point.
        Please do not ABUSE this method as it ALWAYS calls the Bing API.

        :param latitude: Latitude, first index in point array
        :type latitude: float
        :param longitude: Longitude, second index in point array
        :type longitude: float
        :return: Returns location
        :rtype: BingLocation
        :raises: BingApiError if no valid location was returned
        """

        latitude, longitude = str(latitude), str(longitude)
        point_str = longitude + "," + latitude

        url = "http://dev.virtualearth.net/REST/v1/Locations/{point}".format(point=point_str)
        params = {
            "key": self.key
        }
        response_dict = requests.get(url, params).json()
        location = response_dict["resourceSets"][0]["resources"][0]
        return BingLocation.from_location_resource(location)

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


    def get_driving_route(self, source_location, dest_location, departure_date_time=None):
        """
        :param source_location:
        :type BingLocation
        :param dest_location:
        :type BingLocation
        :param departure_date_time:
        :type BingDateTime
        :return:
        """

        try:
            is_correct_type_or_err(source_location, BingLocation)
            is_correct_type_or_err(dest_location, BingLocation)
            is_correct_type_or_err(departure_date_time, BingDateTime)
        except TypeError as e:
            raise BingApiError(e)

        # driving route example https://docs.microsoft.com/en-us/bingmaps/rest-services/examples/driving-route-example
        url = "http://dev.virtualearth.net/REST/V1/Routes/Driving"
        params = {
            "waypoint.0": source_location.point_as_str,  # source
            "waypoint.1": dest_location.point_as_str,    # destination
            "distanceUnit": "Mile",
            "optimize": "timeWithTraffic",
            "key": self.key
        }

        if departure_date_time:
            params["datetime"] = str(departure_date_time),
            params["timeType"] = "Departure"

        response_dict = requests.get(url, params).json()
        try:
            route = response_dict["resourceSets"][0]["resources"][0]
        except IndexError:
            error = response_dict.get("errorDetails",
                                      "No route found for specified source '{}' and dest '{}'."
                                      .format(source_location.address_str, dest_location.address_str))
            raise BingApiError(error)


        return BingDrivingRoute.from_route_and_request_info(route, source_location=source_location,
                                                            dest_location=dest_location,
                                                            departure_date_time=departure_date_time)




