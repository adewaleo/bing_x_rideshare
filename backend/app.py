from flask import Flask
from flask_restful import Api

from resources.todo import Todo, TodoList
from resources.endpoints import PlaceAutocomplete, Recommendations

app = Flask(__name__)
api = Api(app)


## setup the Api resource routing here
api.add_resource(TodoList, '/todos')
api.add_resource(Todo, '/todos/<todo_id>')

api.add_resource(PlaceAutocomplete, '/place_autocomplete/<query>')
api.add_resource(Recommendations, '/recommendations')


if __name__ == '__main__':
    app.run(debug=True)