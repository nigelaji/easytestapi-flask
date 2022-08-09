# coding:utf-8
from flask import Flask
from flask_sqlalchemy import SQLAlchemy  # https://docs.sqlalchemy.org/en/14/core/expression_api.html
from flask_restful import Api
from app.config import SQLALCHEMY_DATABASE_URI, SECRET_KEY, LOG_CONF
from logging.config import dictConfig

dictConfig(LOG_CONF)
app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True  # 如果没有这行会有警告
app.config["SECRET_KEY"] = SECRET_KEY  # 如果没有，在生成表单的时候，会出现 CRSF 相关错误

db = SQLAlchemy(engine_options={"echo": True})
db.init_app(app)
api = Api(app)

# 创建所有表
with app.app_context():
    from app.models.testerModels import Tester, TesterOpRecord
    # print(db.execute())
    db.create_all()  # 创建所有表
    # 加载redis内容

# from . import views  # 这里面可以放公共视图
from app.restapis import restful_blue

from app.register_api import register_api
register_api(api)

from app import views  # 先有app才能导入views
