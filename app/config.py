import os
from pathlib import Path


SECRET_KEY = '12138'
db_engine = {
    "sqlite": {
        "URI": "sqlite:///temp.db"
    },
    'local_mysql': {
        "URI": ""
        # "URI": "mysql://root:123456@localhost/flask_test"
    },
    'remote_mysql': {

    }
}
SQLALCHEMY_DATABASE_URI = db_engine.get('local_mysql')["URI"] or "sqlite:///temp.db"


# 日志存储目录
LOG_BASE_DIR = os.path.join(Path(__file__).resolve().parent.parent, 'log')
# 上传文件存储路径
UPLOAD_FILE_PATH = os.path.join(Path(__file__).resolve().parent.parent, 'upload')
# 临时存储路径
TMP_STORAGE_PATH = os.path.join(Path(__file__).resolve().parent.parent, 'tmp')

if not os.path.exists(LOG_BASE_DIR):
    os.mkdir(LOG_BASE_DIR)
if not os.path.exists(UPLOAD_FILE_PATH):
    os.mkdir(UPLOAD_FILE_PATH)
if not os.path.exists(TMP_STORAGE_PATH):
    os.mkdir(TMP_STORAGE_PATH)

# logging
LOG_CONF = {
    'version': 1,
    'formatters': {'default': {
        'format': '[%(asctime)s] %(levelname)s in %(module)s %(lineno)s: %(message)s',
    }},
    'handlers': {'wsgi': {
        'class': 'logging.StreamHandler',
        'stream': 'ext://flask.logging.wsgi_errors_stream',
        'formatter': 'default'
    }},
    'root': {
        'level': 'DEBUG',
        'handlers': ['wsgi']
    }
}

