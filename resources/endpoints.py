import sys
from flask import request
from flask_restful import Resource
from common.util import handle_error, assert_equals_or_warn
from common.optimizer  import RouteOptimizer
from common.bing_maps import BingLocation, BingMaps, BingApiError, BingDateTime, BingTransportSegment, BingTransitRoute


class PlaceAutocomplete(Resource):
    def get(self, query):
        address_list = []
        bing_map = BingMaps()

        try:
            address_list = bing_map.get_possible_locations_from_string(query)
        except BingApiError as e:
            handle_error(ex=e)

        duration_list = []
        for address in address_list:
            location = address[0]
            duration = dict()
            duration['address'] = location.address_str
            duration['lat'] = location.point_list[0]
            duration['long'] = location.point_list[1]
            duration_list.append(duration)
        return duration_list, 200


class PointToAddress(Resource):
    def get(self, query):
        try:
            lat, long = query.split(",")
        except ValueError:
            msg = "Wrong lat,long format. Please supply latitude and longitude in the following format: 'lat,long'"
            handle_error(message=msg)

        bing_maps = BingMaps()

        try:
            location = bing_maps.get_location_from_point(
                lat.strip(), long.strip())
        except BingApiError as e:
            handle_error(ex=e)

        duration = dict()
        duration['address'] = location.address_str
        duration['lat'] = location.point_list[0]
        duration['long'] = location.point_list[1]

        return duration, 200


class Recommendations(Resource):

    def post(self):
        self.bing_maps = BingMaps()


        _request_body = request.json
        start = _request_body["start"]
        dest = _request_body["dest"]
        optimisation_type = _request_body["optimise_for"].lower()

        start_point = start.split(",")
        dest_point = dest.split(",")

        is_lat_long = True
        if len(start_point) != len(dest_point) or len(start_point) != 2:
            start_point = None
            dest_point = None
            is_lat_long = False

        if is_lat_long:
            start_location = self.bing_maps.get_location_from_point(start_point[0], start_point[1])
            dest_location = self.bing_maps.get_location_from_point(dest_point[0], dest_point[1])
        else:
            start_location = self.bing_maps.get_location_from_string(start)
            dest_location = self.bing_maps.get_location_from_string(dest)


        depart_time = BingDateTime.now()

        optimizer = RouteOptimizer(start_location, dest_location, optimisation_type, depart_time)

        response_list = []
        optimized_list = []

        uber_route = optimizer.uber_route
        lyft_route = optimizer.lyft_route
        transit_routes = optimizer.basic_transit_routes

        uber_route_dict = self._process_ride_share_route(uber_route)
        lyft_route_dict = self._process_ride_share_route(lyft_route)

        # largest cost should be the cheapest rideshare
        max_cost = min(uber_route_dict["cost"], lyft_route_dict["cost"])
        max_duration = max(uber_route_dict["duration"], lyft_route_dict["duration"])

        for t_route in transit_routes:
            transit_dict = self._process_transit_route(t_route)
            response_list.append(transit_dict)

            # longest duration should be a regular transit route
            max_duration = max(transit_dict["duration"], max_duration)

            complex_routes = optimizer.get_simple_hybrid(t_route)
            for cmp_route in complex_routes:
                optimized_list.append(self._process_complex_route(cmp_route))

        response_list.append(uber_route_dict)
        response_list.append(lyft_route_dict)


        # filter suggested routes that are too slow or costly
        optimized_list = list(filter(lambda route: route["cost"] < max_cost and route["duration"] < max_duration, optimized_list))
        response_list.extend(optimized_list)


        return response_list




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
        segment_dict["description"] = "Take bus 545"
        segment_list.append(segment_dict)
        route_dict["segments"] = segment_dict
        route_dict["start"] = start
        route_dict["dest"] = dest
        route_dict["start_time"] = "07/23/2019 16:30"
        route_dict["end_time"] = "07/23/2019 16:40"
        route_dict["duration"] = 600
        route_dict["cost"] = 6.5
        routes_list.append(route_dict)

        return routes_list, 201

    def _process_ride_share_route(self, bing_ride_share):
        segment_dict = {}
        segment_dict["mode"] = "rideshare"
        segment_dict["duration"] = bing_ride_share.duration.total_seconds()

        segment_dict["start"] = bing_ride_share.source.address_dict()
        segment_dict["dest"] = bing_ride_share.dest.address_dict()

        segment_dict["start_time"] = bing_ride_share.time_requested.date_time_str
        end_time = bing_ride_share.time_requested.date_time + bing_ride_share.duration
        segment_dict["end_time"] = BingDateTime(end_time).date_time_str

        segment_dict["cost"] = bing_ride_share.fare
        segment_dict["description"] = "Use {} (factor in pickup/drop time).".format(bing_ride_share.type)

        result = {
            "segments": [segment_dict],
            "cost": segment_dict["cost"],
            "start": segment_dict["start"],
            "dest": segment_dict["dest"],
            "start_time": segment_dict["start_time"],
            "end_time": segment_dict["end_time"],
            "duration": segment_dict["duration"],
            "type": "only_ride_share"
        }

        return result

    def _process_transit_segment(self, bing_transit_segment):
        segment_dict = {}
        segment_dict["mode"] = "transit" if isinstance(bing_transit_segment, BingTransportSegment) else "walk"
        segment_dict["duration"] = bing_transit_segment.duration.total_seconds()


        if isinstance(bing_transit_segment, BingTransportSegment):
            segment_dict["start"] = bing_transit_segment.depart_details.coords.address_dict()
            segment_dict["dest"] = bing_transit_segment.arrive_details.coords.address_dict()
        else:
            segment_dict["start"] = bing_transit_segment.start_location.address_dict()
            segment_dict["dest"] = None

        if isinstance(bing_transit_segment, BingTransportSegment):
            segment_dict["start_time"] = bing_transit_segment.depart_details.time.date_time_str
            segment_dict["end_time"] = bing_transit_segment.arrive_details.time.date_time_str
        else:
            segment_dict["start_time"] = None
            segment_dict["end_time"] = None

        segment_dict["cost"] = bing_transit_segment.cost
        segment_dict["description"] = bing_transit_segment.text
        return segment_dict

    def _process_transit_route(self, bing_transit_route):
        segments = []

        for seg in bing_transit_route.segments:
            segments.append(self._process_transit_segment(seg))

        result = {
            "segments": segments,
            "cost": bing_transit_route.fare,
            "start": bing_transit_route.start_location.address_dict(),
            "dest": bing_transit_route.end_location.address_dict(),
            "start_time": bing_transit_route.start_time.date_time_str,
            "end_time": bing_transit_route.end_time.date_time_str,
            "duration": bing_transit_route.duration.total_seconds(),
            "type": "only_transit"
        }

        return result

    def _process_complex_route(self, bing_complex_route):
        total_duration = 0.0
        total_fare = 0
        segments = []

        complex_routes = []

        for route in bing_complex_route.routes:
            if isinstance(route, BingTransitRoute):
                route = self._process_transit_route(route)
            else:
                route = self._process_ride_share_route(route)

            total_duration += route["duration"]
            total_fare += route["cost"]
            segments.extend(route['segments'])

            # add the route_dict
            complex_routes.append(route)


        start_location = complex_routes[0]["start"]
        dest_location = complex_routes[-1]["dest"]

        start_time = complex_routes[0]["start_time"]
        end_time = complex_routes[-1]["end_time"]

        assert_equals_or_warn(start_location, segments[0]["start"])
        assert_equals_or_warn(dest_location, segments[-1]["dest"])
        assert_equals_or_warn(start_time, segments[0]["start_time"])
        assert_equals_or_warn(end_time, segments[-1]["end_time"])
        assert_equals_or_warn(total_duration, bing_complex_route.total_duration.total_seconds())


        result = {
            "start": start_location,
            "dest": dest_location,
            "start_time": start_time,
            "end_time": end_time,
            "cost": total_fare,
            "duration": total_duration,
            "segments": segments,
            "type": "complex"
        }

        return result



