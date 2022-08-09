# coding:utf-8
import datetime
from flask_restful import Resource
from .libs.selfreqparser import SelfRequestParser
from app import db, app
from app.models.testerModels import Tester, TesterOpRecord
from sqlalchemy import and_, desc
import re
from app.exceptions import ParamsError, RecordNotExisted, UnknownError, RecordExisted, EnumNotExisted


def phone_validator(phone_number):
    if re.match(r"^((13[0-9])|(14(5\|7))|(15([0-3]|[5-9]))|(18[0,5-9]))\d{8}$", phone_number):
        pass
    else:
        raise ParamsError("'The phone number does not meet the specification'")
    if Tester.is_exist(phone_number):
        raise RecordExisted("'test_phone' existed")


def fields_not_null_or_empty_validator(**fields):
    for field_name, val in fields.items():
        if not isinstance(val, str) or not val:
            raise ParamsError(f'{field_name} not null or empty string')


def tester_not_existed_by_id(_id):
    tester = Tester.query.filter_by(id=id, status=True).first()
    if not tester:
        raise RecordNotExisted(f"the tester not existed")


def enum_not_existed(v):
    if v not in ['A', 'B', 'C']:
        raise EnumNotExisted(f'{v} enum mot exist')


def record_tester(sb, op_type, msg):
    try:
        record = TesterOpRecord(sb, op_type, msg)
        db.session.add(record)
        db.session.commit()
    except Exception as e:
        app.logger.debug(f'table <TesterOpRecord> write db error: {e}')


def transform_paginate(paginate_obj):
    return {
        "page": paginate_obj.page,
        "pages": paginate_obj.pages,
        "per_page": paginate_obj.per_page,
        "total": paginate_obj.total,
        "items": [obj.serialize() for obj in paginate_obj.items]
    }


class TesterListAPI(Resource):

    def get(self):
        ret = {
            'code': 200,
            'data': {},
            'msg': 'ok',
        }
        parse = SelfRequestParser()
        parse.add_argument('page', type=int, location='args')
        parse.add_argument('per_page', type=int, location='args')
        parse.add_argument('test_str', type=str, location='args')
        parse.add_argument('test_phone', type=str, location='args')
        kwargs = parse.parse_args()
        page = kwargs.get('page') or 1
        per_page = kwargs.get('per_page') or 10
        test_str = kwargs.get('test_str')
        test_phone = kwargs.get('test_phone')
        app.logger.debug(f'request params: {kwargs}')
        try:
            filters = [Tester.status == True]
            if test_str:
                filters.append(Tester.test_str.like(f"%{test_str}%"))
            if test_phone:
                filters.append(Tester.test_phone.like(f"%{test_phone}%"))
            testers = Tester.query.filter(
                and_(*filters)
            ).order_by(Tester.id).paginate(page=page, per_page=per_page, error_out=False)
            ret['data'] = transform_paginate(testers)
        # except ParamsError as pe:
        #     ret = {
        #         'code': pe.code,
        #         'msg': pe.message
        #     }
        except UnknownError as e:
            ret = {
                'code': e.code,
                'msg': e.message
            }
        return ret

    def post(self):
        ret = {
            'code': 200,
            'data': {},
            'msg': 'ok',
        }
        parse = SelfRequestParser()
        parse.add_argument('test_str', type=str, required=True, help='required', location='json')
        parse.add_argument('test_int', type=int, location='json')
        parse.add_argument('test_float', type=str, location='json')
        parse.add_argument('test_phone', type=str, required=True, help='required', location='json')
        parse.add_argument('test_dt', type=str, location='json')
        parse.add_argument('test_ts', type=str, location='json')
        parse.add_argument('test_enum', type=str, location='json')
        kwargs = parse.parse_args()
        tester_id = None
        try:
            fields_not_null_or_empty_validator(test_str=kwargs.get('test_str'), test_phone=kwargs.get('test_phone'))
            phone_validator(kwargs.get('test_phone'))
            enum_not_existed(kwargs.get('test_enum'))
            test_dt = kwargs.get("test_dt")
            if test_dt is not None:
                test_dt_convert = datetime.datetime.strptime(test_dt, "%Y-%m-%d %H:%M:%S")
                kwargs.update({"test_dt": test_dt_convert})
            app.logger.debug(f'request params: {kwargs}')
            tester = Tester(**kwargs)
            db.session.add(tester)
            db.session.commit()  # commit之后，下面的tester才能得到id属性
            tester_id = tester.id
            ret['data'].update({
                'id': tester_id
            })
        except ParamsError as pe:
            ret = {'code': pe.code, 'msg': pe.message}
        except UnknownError as e:
            # print(e.with_traceback())
            ret = {'code': e.code, 'msg': e.message}
        record = TesterOpRecord(tester_id, 'create', ret['msg'])
        db.session.add(record)
        db.session.commit()
        return ret


class TesterAPI(Resource):
    def get(self, id):
        ret = {
            'code': 200,
            'data': {},
            'msg': 'ok',
        }
        tester = Tester.query.filter_by(id=id, status=True).first()
        if not tester:
            ret.update({
                'code': 404,
                'msg': '资源不存在'
            })
            return ret
        ret['data'] = tester.serialize()
        return ret

    def put(self, id):
        ret = {
            'code': 200,
            'data': {},
            'msg': 'ok',
        }
        tester = Tester.query.filter_by(id=id, status=True).first()
        if not tester:
            ret.update({
                'code': 404,
                'msg': '资源不存在'
            })
            return ret
        else:
            parse = SelfRequestParser()
            parse.add_argument('test_str', type=str, required=True, help='required', location='json')
            parse.add_argument('test_int', type=int, location='json')
            parse.add_argument('test_float', type=str, location='json')
            parse.add_argument('test_phone', type=str, required=True, help='required', location='json')
            parse.add_argument('test_dt', type=str, location='json')
            parse.add_argument('test_ts', type=str, location='json')
            parse.add_argument('test_enum', type=str, location='json')
            kwargs = parse.parse_args()
            try:
                fields_not_null_or_empty_validator(test_str=kwargs.get('test_str'), test_phone=kwargs.get('test_phone'))
                if tester.test_phone != kwargs.get('test_phone'):
                    phone_validator(kwargs.get('test_phone'))
                test_dt = kwargs.get("test_dt")
                if test_dt is not None:
                    test_dt_convert = datetime.datetime.strptime(test_dt, "%Y-%m-%d %H:%M:%S")
                    kwargs.update({"test_dt": test_dt_convert})
                app.logger.debug(f'request params: {kwargs}')
                for k, v in kwargs.items():
                    setattr(tester, k, v)
                ret['data'].update({
                    'id': tester.id
                })
                db.session.add(tester)
                db.session.commit()
            except Exception as e:
                ret.update({
                    'code': 500,
                    'msg': f"{e}"
                })
            record_tester(id, 'update', ret['msg'])
            return ret

    def patch(self, id):
        ret = {
            'code': 200,
            'data': {},
            'msg': 'ok',
        }
        tester = Tester.query.filter_by(id=id, status=True).first()
        if not tester:
            ret.update({
                'code': 404,
                'msg': '资源不存在'
            })
            return ret
        else:
            parse = SelfRequestParser()
            parse.add_argument('test_str', type=str, required=True, help='required', location='json')
            parse.add_argument('test_int', type=int, location='json')
            parse.add_argument('test_float', type=str, location='json')
            parse.add_argument('test_phone', type=str, required=True, help='required', location='json')
            parse.add_argument('test_dt', type=str, location='json')
            parse.add_argument('test_ts', type=str, location='json')
            parse.add_argument('test_enum', type=str, location='json')
            kwargs = parse.parse_args()
            try:
                fields_not_null_or_empty_validator(test_str=kwargs.get('test_str'), test_phone=kwargs.get('test_phone'))
                if tester.test_phone != kwargs.get('test_phone'):
                    phone_validator(kwargs.get('test_phone'))
                test_dt = kwargs.get("test_dt")
                if test_dt is not None:
                    test_dt_convert = datetime.datetime.strptime(test_dt, "%Y-%m-%d %H:%M:%S")
                    kwargs.update({"test_dt": test_dt_convert})
                app.logger.debug(f'request params: {kwargs}')
                for k, v in kwargs.items():
                    setattr(tester, k, v)
                ret['data'].update({
                    'id': tester.id
                })
                db.session.add(tester)
                db.session.commit()
            except Exception as e:
                ret.update({
                    'code': 500,
                    'msg': f"{e}"
                })
            record_tester(id, 'update', ret['msg'])
            return ret

    def delete(self, id):
        ret = {
            'code': 200,
            'data': {},
            'msg': 'ok',
        }
        try:
            tester = Tester.query.filter_by(id=id, status=True).first()
            tester.status = False
        except Exception as e:
            ret.update({
                'code': 500,
                'msg': f"{e}"
            })
        record_tester(id, 'delete', ret['msg'])
        return ret


class TesterOpRecordListAPI(Resource):
    def get(self):
        ret = {
            'code': 200,
            'data': {},
            'msg': 'ok',
        }
        parse = SelfRequestParser()
        parse.add_argument('page', type=int, location='args')
        parse.add_argument('per_page', type=int, location='args')
        kwargs = parse.parse_args()
        page = kwargs.get('page') or 1
        per_page = kwargs.get('per_page') or 10
        try:
            tester_op_record = TesterOpRecord.query.filter().order_by(desc(TesterOpRecord.id)).paginate(
                page=page, per_page=per_page, error_out=False)
            ret['data'] = transform_paginate(tester_op_record)
        except Exception as e:
            ret.update({
                "code": 500,
                "msg": f"{e}"
            })
        return ret


tester_resources = [
    {
        'resource': TesterListAPI,
        'urls': '/testers'
    },
    {
        'resource': TesterAPI,
        'urls': '/testers/<int:id>'
    },
    {
        'resource': TesterOpRecordListAPI,
        'urls': '/tester_op_record'
    },
]
