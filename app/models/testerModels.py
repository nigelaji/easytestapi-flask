# coding:utf-8
from datetime import datetime
from app import db

__all__ = [
    'Tester', 'TesterOpRecord'
]


def dump_datetime(datetime_obj, format_str="%Y-%m-%d %H:%M:%S"):
    """处理DateTime格式的字段，处理成json容易处理的"""
    if datetime_obj is None:
        return None
    return datetime_obj.strftime(format_str)


class Tester(db.Model):
    """测试用表"""
    __tablename__ = 'tp_tester'
    id = db.Column(db.Integer, primary_key=True)
    test_str = db.Column(db.String(30), comment='测试字符串', nullable=False)
    test_int = db.Column(db.Integer, comment='测试整型数值')
    test_float = db.Column(db.Float, comment='测试浮点数')
    test_phone = db.Column(db.String(30), comment='测试手机号', unique=True, nullable=False)
    test_dt = db.Column(db.DateTime, comment='测试日期')
    test_ts = db.Column(db.TIMESTAMP, comment='测试时间戳')
    test_enum = db.Column(db.String(1), comment='测试枚举值')
    status = db.Column(db.BOOLEAN, comment='测试状态', default=True)

    # 1对多 select ， 1对1可以dynamic, 更多参考：https://docs.sqlalchemy.org/en/14/orm/relationship_api.html

    def __init__(self, test_str, test_phone, **kwargs):
        self.test_str = test_str
        self.test_phone = test_phone
        for k, v in kwargs.items():
            setattr(self, k, v)

    @staticmethod
    def is_exist(test_phone):
        testers = Tester.query.filter(Tester.test_phone == test_phone).all()
        if len(testers) >= 1:
            return True

    def serialize(self):
        return {
            "id": self.id,
            "test_str": self.test_str,
            "test_int": self.test_int,
            "test_float": self.test_float,
            "test_phone": self.test_phone,
            "test_dt": datetime.strftime(self.test_dt, "%Y-%m-%d %H:%M:%S") if self.test_dt is not None else None,
            "test_ts": self.test_ts,
            "test_enum": self.test_enum,
        }

    def __repr__(self):
        return f"<Tester (id='{self.id}')>"


class TesterOpRecord(db.Model):
    """测试Tester操作记录"""
    __tablename__ = 'tp_tester_operate_record'
    id = db.Column(db.Integer, primary_key=True)
    tester_id = db.Column(db.Integer, comment="测试ID")
    operate_type = db.Column(db.Enum("create", "update", "delete", name="operate_type"), comment="操作类型")
    result = db.Column(db.TEXT, comment='操作结果')
    operate_time = db.Column(db.DateTime, default=datetime.now())

    def __init__(self, tester_id, operate_type, result=""):
        self.tester_id = tester_id
        self.operate_type = operate_type
        self.result = result

    def serialize(self):
        return {
            "id": self.id,
            "tester_id": self.tester_id,
            "operate_type": self.operate_type,
            "result": self.result,
            "operate_time": datetime.strftime(self.operate_time, "%Y-%m-%d %H:%M:%S"),
        }

    def __repr__(self):
        return f"<TesterOpRecord (id='{self.id}')>"
