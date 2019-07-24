from flask_restful import Resource, abort
from common.bing_maps import BingLocation, BingMaps, BingApiError
from flask import request
from common.util import handle_error
import json


class PlaceAutocomplete(Resource):
    def get(self, query):
        address_list = []
        bing_map = BingMaps()

        try:
            address_list = bing_map.get_possible_locations_from_string(query)
        except BingApiError as e:
            handle_error(ex=e)

        address_dict_list = []
        for address in address_list:
            location = address[0]
            address_dict = dict()
            address_dict['address'] = location.address_str
            address_dict['lat'] = location.point_list[0]
            address_dict['long'] = location.point_list[1]
            address_dict_list.append(address_dict)
        return address_dict_list, 200


class PointToAddress(Resource):
    def get(self, query):
        try:
            lat, long = query.split(",")
        except ValueError:
            msg = "Wrong lat,long format. Please supply latitude and longitude in the following format: 'lat,long'"
            handle_error(message=msg)

        bing_map = BingMaps()

        try:
            location = bing_map.get_location_from_point(
                lat.strip(), long.strip())
        except BingApiError as e:
            handle_error(ex=e)

        address_dict = dict()
        address_dict['address'] = location.address_str
        address_dict['lat'] = location.point_list[0]
        address_dict['long'] = location.point_list[1]

        return address_dict, 200


class Recommendations(Resource):

    def post(self):
        requestData = json.loads(request.data)
        start = requestData["start"]
        dest = requestData["dest"]
        start_lat = start["lat"]
        start_long = start["long"]
        dest_lat = dest["lat"]
        dest_long = dest["long"]
        optimisation_factor = requestData["optimse_for"]

        """
        Dummy dictionary of the object [Route, Route....] 
        with one Route option.
        """
        routes_list = []
        route_dict = dict()
        segment_list = []
        segment_dict = dict()
        segment_dict["start"] = start
        segment_dict["dest"] = dest
        segment_dict["mode"] = "transit"
        segment_dict["duration"] = 600
        segment_dict["start_time"] = "07/23/2019 16:30"
        segment_dict["end_time"] = "07/23/2019 16:40"
        segment_dict["cost"] = 6.5
        segment_dict["desc"] = "Take bus 545"
        segment_list.append(segment_dict)
        route_dict["segment"] = segment_dict
        route_dict["start"] = start
        route_dict["dest"] = dest
        route_dict["start_time"] = "07/23/2019 16:30"
        route_dict["end_time"] = "07/23/2019 16:40"
        route_dict["duration"] = 600
        route_dict["cost"] = 6.5
        routes_list.append(route_dict)

        return routes_list, 201
