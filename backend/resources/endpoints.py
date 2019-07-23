from flask_restful import Resource, reqparse
from common.bing_maps import BingLocation, BingMaps
import json

class PlaceAutocomplete(Resource):
    def get(self, query):
#         return query
        address_list = []
        bing_map = BingMaps()
        address_list = bing_map.get_possible_locations_from_string(query)
#         address_list.sort(key=lambda x:x[1],reverse=True)
        address_dict_list = []
        for address in address_list:
            location = address[0]
            address_dict = dict()
            address_dict['address'] = location.address_str
            address_dict['lat'] = location.point_list[0]
            address_dict['long'] = location.point_list[1]
            address_dict_list.append(address_dict)
        return address_dict_list, 201

    def post(self):
        return "", 201
    
    
    
class Recommendations(Resource):
    def get(self, query):
        return "", 201

    def post(self):
        
        return "", 201


