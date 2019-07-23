from argparse import ArgumentParser
from flask import Flask
from flask_restful import Api

from resources.todo import Todo, TodoList
from common.bing_maps import main_method

app = Flask(__name__)
api = Api(app)


## setup the Api resource routing here
api.add_resource(TodoList, '/todos')
api.add_resource(Todo, '/todos/<todo_id>')


if __name__ == '__main__':
    # python backend/app.py --help
    parser = ArgumentParser(description="Run the server or run tests by adding `--tests`")
    parser.add_argument('--test', action='store_true', help="If flag is supplied, run tests instead of server")

    args = parser.parse_args()

    if not args.test:
        app.run(debug=True)


    # run tests here..... feel to comment as needed.
    main_method()
