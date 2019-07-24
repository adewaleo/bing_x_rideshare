# Location from Query: https://docs.microsoft.com/en-us/bingmaps/rest-services/locations/find-a-location-by-query
# Location and Area Types: https://docs.microsoft.com/en-us/bingmaps/rest-services/common-parameters-and-types/location-and-area-types
# Routes: https://docs.microsoft.com/en-us/bingmaps/rest-services/routes/calculate-a-route
# RouteData: https://docs.microsoft.com/en-us/bingmaps/rest-services/routes/route-data.

import os
import datetime
import requests
from yaml import safe_load
from common.util import dict_to_pretty_str, is_correct_type_or_err

BING_API_CREDENTIALS = os.path.abspath(os.path.join(os.path.dirname(__file__), "bing.key.yaml"))

def _get_api_key_from_file(filename=BING_API_CREDENTIALS):
    with open(filename, 'r') as config_file:
        config = safe_load(config_file)
    return config["queryKey"]


class BingApiError(Exception):
    pass


class BingType(object):
    def __str__(self):
        try:
            return dict_to_pretty_str(str(self.__dict__))
        except Exception as e:
            return str(self.__dict__)

class BingDateTime(BingType):

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


class BingDistance(BingType):
    def __init__(self, value, unit):
        self.value = value
        self.unit = unit.lower()

        if self.unit != "mile":
            raise ValueError("The unit must be 'mile' or 'Mile'.")


class BingDuration(datetime.timedelta, BingType):

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

class BingLocation(BingType):
    def __init__(self, point, address):
        self.point_list = point  # list of latitude and longiturde
        self.point_as_str = ",".join([str(coord) for coord in self.point_list])
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


class BingDepartArrive(BingType):
    def __init__(self, mt=None, names=None, coords=None):
        self.manType=mt
        self.names = names
        self.coords = coords


class BingWalkSegment(BingType):
    def __init__(self, coords = None, mantype= None,dist= None,duration=None,cost= None):
        self.coords = coords
        self.manType = mantype
        self.dist = dist
        self.duration = duration
        self.cost = 0


class BingTransportSegment(BingType):
    def __init__(self, typeoftransport = None, departdetails = None, arrivedetails = None, mantype= None,text= None, dist= None,duration=None, txt = None, cost = None):
        self.typeofTransport = typeoftransport
        self.departDetails = departdetails
        self.arriveDetails = arrivedetails
        self.dist = dist
        self.duration = duration
        self.manType = mantype
        self.text = txt


class BingDrivingRoute(BingType):

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
        point_str = latitude + "," + longitude

        url = "http://dev.virtualearth.net/REST/v1/Locations/{point}".format(point=point_str)
        params = {
            "key": self.key
        }
        response_dict = requests.get(url, params).json()
        location = response_dict["resourceSets"][0]["resources"][0]
        return BingLocation.from_location_resource(location)


    def get_segments(self, source, destination):
        url = "http://dev.virtualearth.net/REST/v1/Routes/Transit"
        params = {
            "wayPoint.1": source,
            "wayPoint.2": destination,
            "distanceUnit": "Mile",
            "dateTime": "07/24/2019 05:42:00",
            "travelMode": "Transit",
            "timeType": "Departure",
            "key": BING_API_KEY
        }
        response_dict = requests.get(url, params).json()
        walkSegmentResults = []
        transportSegmentResults = []
        segments = response_dict["resourceSets"][0]["resources"][0]["routeLegs"][0]["itineraryItems"]

        for segmentItem in segments:
            if 'childItineraryItems' not in segmentItem:
                walkSegment = BingWalkSegment()
                walkSegment.coords = segmentItem["maneuverPoint"]["coordinates"]
                walkSegment.manType = segmentItem["details"][0]["maneuverType"]
                walkSegment.dist = segmentItem["travelDistance"]
                walkSegment.duration = segmentItem["travelDuration"]
                walkSegmentResults.append(walkSegment)
            else:
                transportSegment = BingTransportSegment()
                transportSegment.manType = segmentItem["details"][0]["maneuverType"]
                transportSegment.dist = segmentItem["travelDistance"]
                transportSegment.duration = segmentItem["travelDuration"]
                transportSegment.text = segmentItem["instruction"]["text"]
                depart = BingDepartArrive()
                depart.manType = segmentItem["childItineraryItems"][0]["details"][0]["maneuverType"]
                depart.names = segmentItem["childItineraryItems"][0]["instruction"]["text"]
                depart.coords = segmentItem["childItineraryItems"][0]["maneuverPoint"]["coordinates"]
                arrive = BingDepartArrive()
                arrive.manType = segmentItem["childItineraryItems"][1]["details"][0]["maneuverType"]
                arrive.names = segmentItem["childItineraryItems"][1]["instruction"]["text"]
                arrive.coords = segmentItem["childItineraryItems"][1]["maneuverPoint"]["coordinates"]
                transportSegment.departDetails = depart
                transportSegment.arriveDetails = arrive
                transportSegmentResults.append(transportSegment)
        return walkSegmentResults, transportSegmentResults

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
            if departure_date_time:
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



def main_method():
    # run python common/bing_maps.py

    map_api = BingMaps()

    query = input("Enter the query string: ").strip()
    print([(tup[0].address_str, tup[1]) for tup in map_api.get_possible_locations_from_string(query)])

    source = input("Enter the source address: ").strip()
    destination = input("Enter the destination address: ").strip()

    source = map_api.get_location_from_string(source)
    destination = map_api.get_location_from_string(destination)

    print(str(map_api.get_driving_route(source, destination)))

    print("Source {} has latitude {} and longitude {}.".format(source, source.point_list[0], source.point_list[1]))

    print("Getting point address from latitude and longitude")

    print(map_api.get_location_from_point(source.point_list[0], source.point_list[1]).address_str)

    print("---- Getting segments of a transit route  -----")

    transitsource = input("Enter the source address: ").strip()
    transitdestination = input("Enter the destination address: ").strip()

    transitsource = map_api.get_location_from_string(transitsource)
    transitdestination = map_api.get_location_from_string(transitdestination)

    walkSegments, transportSegments = map_api.get_segments(transitsource, transitdestination)
    print("******* Walk Segments in the Route *******")
    print(walkSegments)
    print("******* Transport Segments in the Route *******")
    print(transportSegments)