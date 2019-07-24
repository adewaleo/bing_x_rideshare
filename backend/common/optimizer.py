
from common.bing_maps import BingLocation
from common.util import dict_to_pretty_str, is_correct_type_or_err

class RouteOptimizer(object):

    def __init__(self, source, dest, optimization_type):
        is_correct_type_or_err(source, BingLocation)
        is_correct_type_or_err(dest, BingLocation)

        if optimization_type.lower() not in ["cost", "time"]:
            self.optimization_type = optimization_type

        self.origin_source = source
        self.final_dest = dest


    def _init_best_worst_case(self):






    def print_route(self):
        pass