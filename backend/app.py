from argparse import ArgumentParser
from flask import Flask
from flask_restful import Api

from resources.endpoints import PlaceAutocomplete, Recommendations, PointToAddress
from common.bing_maps import main_method

app = Flask(__name__)
api = Api(app)


## setup the Api resource routing here

api.add_resource(PlaceAutocomplete, '/place_autocomplete/<query>')
api.add_resource(PointToAddress, '/point_to_address/<query>')
api.add_resource(Recommendations, '/recommendations')


if __name__ == '__main__':
    # python backend/app.py --help
    parser = ArgumentParser(description="Run the server or run tests by adding `--test`")
    parser.add_argument('--test', action='store_true', help="If flag is supplied, run tests instead of server")

    args = parser.parse_args()

    if not args.test:
        app.run(debug=True)
    else:
        # run tests here..... feel to comment as needed.
        main_method()
