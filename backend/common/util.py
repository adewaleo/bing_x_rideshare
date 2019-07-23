import json
from flask_restful import abort
from resources.state import TODOS


def abort_if_todo_doesnt_exist(todo_id):
    if todo_id not in TODOS:
        abort(404, message="Todo {} doesn't exist".format(todo_id))

def dict_to_pretty_str(value):
    return json.dumps(value, indent=2, sort_keys=True)