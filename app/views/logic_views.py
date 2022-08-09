from app import app

from flask import request, jsonify


@app.route('/logic/greater', methods=['POST'])
def greater():
    ret = {
        'code': 200,
        'msg': 'ok',
        'data': {}
    }
    arg1 = request.json.get('arg1')
    arg2 = request.json.get('arg2')
    if arg1 is None or arg2 is None:
        ret.update({
            "code": 500,
            "msg": "参数必须"
        })
        return jsonify(ret)
    if int(arg1) > int(arg2):
        ret.update({
            "code": 500,
            "msg": "arg1 不能大于 arg2"
        })
    return jsonify(ret)


@app.route('/logic/less', methods=['POST'])
def less():
    ret = {
        'code': 200,
        'msg': 'ok',
        'data': {}
    }
    arg1 = request.json.get('arg1')
    arg2 = request.json.get('arg2')
    if arg1 is None or arg2 is None:
        ret.update({
            "code": 500,
            "msg": "参数必须"
        })
        return jsonify(ret)
    if int(arg1) < int(arg2):
        ret.update({
            "code": 500,
            "msg": "arg1 不能小于 arg2"
        })
    return jsonify(ret)


@app.route('/logic/equal', methods=['POST'])
def equal():
    ret = {
        'code': 200,
        'msg': 'ok',
        'data': {}
    }
    arg1 = request.json.get('arg1')
    arg2 = request.json.get('arg2')
    if arg1 is None or arg2 is None:
        ret.update({
            "code": 500,
            "msg": "参数必须"
        })
        return jsonify(ret)
    if int(arg1) == int(arg2):
        ret.update({
            "code": 500,
            "msg": "arg1 不能等于 arg2"
        })
    return jsonify(ret)


@app.route('/logic/specific', methods=['POST'])
def specific():
    ret = {
        'code': 200,
        'msg': 'ok',
        'data': {}
    }
    arg1 = request.json.get('arg1')
    arg2 = request.json.get('arg2')
    if arg1 is None or arg2 is None:
        ret.update({
            "code": 500,
            "msg": "参数必须"
        })
        return jsonify(ret)
    if int(arg1) == 1 and int(arg2) == 2:
        ret.update({
            "code": 500,
            "msg": "arg1不能等于1 arg2不能等于2"
        })
        return jsonify(ret)
    return jsonify(ret)
