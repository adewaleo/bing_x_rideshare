
from common.bing_maps import (BingMaps, BingLocation, BingDateTime, RideShareRoute, BingTransitRoute,
                              BingTransportSegment, BingComplexRoute)
from common.util import dict_to_pretty_str, is_correct_type_or_err


class RouteOptimizer(object):

    def __init__(self, source, dest, optimization_type, depart_time):
        is_correct_type_or_err(source, BingLocation)
        is_correct_type_or_err(dest, BingLocation)
        is_correct_type_or_err(depart_time, BingDateTime)

        if optimization_type.lower() not in ["cost", "time"]:
            self.optimization_type = optimization_type

        self.origin_source = source
        self.final_dest = dest

        self.bing_maps = BingMaps()
        self.depart_time = depart_time

        self.uber_route = None
        self.lyft_route = None
        self._init_routes()


    def _init_routes(self):
        routes = RideShareRoute.from_source_dest(self.origin_source, self.final_dest, self.depart_time)
        self.uber_route = routes["uber"]
        self.lyft_route = routes["lyft"]

        transit_routes = self.bing_maps.get_transit_routes(self.origin_source.address_str, self.final_dest.address_str)
        self.basic_transit_routes = transit_routes


    def get_simple_hybrid(self, transit_route):
        def _replace_simple_complex_route(last_segment, possible_complex_routes, transit_route):
            rs_source = last_segment.depart_details.coords
            rs_depart_time = last_segment.depart_details.time
            ride_share_route = RideShareRoute.from_source_dest(rs_source, self.final_dest, rs_depart_time)
            # possible_complex_routes.append(BingComplexRoute([transit_route, ride_share_route["lyft"]]))
            possible_complex_routes.append(BingComplexRoute([transit_route, ride_share_route["uber"]]))

        if len(transit_route.segments) <= 1:
            return []

        possible_complex_routes = []
        while len(transit_route.segments) > 1:
            # get last segment, this is the start of the rideshare.
            last_segment = transit_route.segments[-1]

            # update transit route by removing last segment
            transit_route = transit_route.get_route_without_last_segment()

            # if there is another transport segment beforehand
            if isinstance(last_segment, BingTransportSegment):
                _replace_simple_complex_route(last_segment, possible_complex_routes, transit_route)
            else:
                del last_segment
                # in this case last segment is walk segment... so use previous transit segment to determine departure time.
                try:
                    second_to_last_segment = transit_route.segments[-1]
                except IndexError:
                    continue
                if isinstance(second_to_last_segment, BingTransportSegment):
                    rs_source = second_to_last_segment.arrive_details.coords
                    rs_depart_time = second_to_last_segment.arrive_details.time
                    ride_share_route = RideShareRoute.from_source_dest(rs_source, self.final_dest, rs_depart_time)
                    # possible_complex_routes.append(BingComplexRoute([transit_route, ride_share_route["lyft"]]))
                    possible_complex_routes.append(BingComplexRoute([transit_route, ride_share_route["uber"]]))

        return possible_complex_routes

