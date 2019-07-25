
from common.bing_maps import BingLocation, BingDateTime, BingMaps, RideShareRoute, BingTransitRoute
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


    def get_simple_hybrid(self):
        pass