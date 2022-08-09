# coding:utf-8
import json
from flask import make_response, jsonify, Response
from app import app, db
from app.decos import times_count
from flask import render_template, request, redirect


@app.route('/')
def root():
    return redirect("index")


@app.route('/index')
def index():
    return render_template('pages/index.html')


# @app.errorhandler(404)
# def page_not_found(error):
# self_abort(404, "path 路径不存在") 调用abort时，不能调用HTTPException类的处理程序
#    return {'code': 404, 'msg': f'路径 {request.full_path[:-1]} 不存在'},404


@app.route('/get_verification_code')  # 验证码获取接口
def get_verification_code():
    ret = {
        'code': 200,
        'msg': '获取验证码',
        'data': {}
    }
    response = make_response(json.dumps(ret))
    response.headers['Content-Type'] = 'application/json'
    return response


# 三种方式返回Content-Type: application/json类型数据
@app.route('/tp/test1')  # jsonify方式
def test1():
    ret = {
        'code': 200,
        'msg': 'test1',
        'data': {}
    }
    return jsonify(ret)


@app.route('/test2')  # Response类构造方式
def test2():
    ret = {
        'code': 200,
        'msg': 'test2',
        'data': {}
    }
    return Response(json.dumps(ret), mimetype='application/json')


@app.route('/test3')  # make_response方法构造
def test3():
    ret = {
        'code': 200,
        'msg': 'test3',
        'data': {
            "obj": ""
        }
    }
    response = make_response(json.dumps(ret))
    response.headers['Content-Type'] = 'application/json'
    return response


@app.route('/init_count')
@times_count
def init_count():
    print(request.host)
    return jsonify({
        "code": 200,
        "message": "ok",
    })


@app.route('/sssss', methods=['POST'])
@times_count
def eventRcv():
    # logger.info(request.json or '空')
    print(request.remote_addr, request.json)
    return jsonify({
        "code": 200,
        "message": "success",
        "desc": "",
        "data": {}
    })


@app.route('/xxxx', methods=['POST'])
@times_count
def eventRcv1():
    # logger.info(request.json or '空')
    print(request.remote_addr, request.json)
    return jsonify({
        "code": 200,
        "message": "success",
        "desc": "",
        "data": {}
    })


from app.views import logic_views
from app.views import upload_views
