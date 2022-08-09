import json
from flask.app import Response
from werkzeug.exceptions import abort


def self_abort(code: int, msg: str, status=200, mimetype='application/json', **kwargs) -> abort:
    ret = {
        "code": code,
        "msg": msg
    }
    # print(ret)
    return abort(Response(json.dumps(ret), status=status, mimetype=mimetype, **kwargs))
