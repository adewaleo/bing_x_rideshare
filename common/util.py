import sys
import json
from flask_restful import abort
from resources.state import TODOS


def abort_if_todo_doesnt_exist(todo_id):
    if todo_id not in TODOS:
        abort(404, message="Todo {} doesn't exist".format(todo_id))

def dict_to_pretty_str(value):
    return json.dumps(value, indent=2, sort_keys=True)

def is_correct_type_or_err(obj, cls):
    if not isinstance(obj, cls):
        raise TypeError("{} is not an instance of type {}".format(obj, cls))

def handle_error(ex=None, status_code=400, message=None):
    data = {
        "message": message or ex.message if hasattr(ex, 'message') else str(ex)
    }
    abort(status_code, **data)

def assert_equals_or_warn(a, b):
    pass
    # try:
    #     assert a == b
    # except AssertionError:
    #     print("{} is not equal to {}".format(a, b), file=sys.stderr)
