import logging
import logging.handlers
import os
import sys
import textwrap
from app.config import LOG_BASE_DIR

"""
filename：   用指定的文件名创建FiledHandler（后边会具体讲解handler的概念），这样日志会被存储在指定的文件中。
filemode：   文件打开方式，在指定了filename时使用这个参数，默认值为“a”还可指定为“w”。
format：      指定handler使用的日志显示格式。
datefmt：    指定日期时间格式。
level：        设置rootlogger（后边会讲解具体概念）的日志级别
stream：     用指定的stream创建StreamHandler。可以指定输出到sys.stderr,sys.stdout或者文件，默认为sys.stderr。
                  若同时列出了filename和stream两个参数，则stream参数会被忽略。
https://docs.python.org/zh-cn/3/library/logging.html#logrecord-attributes
"""


class NewLineFormatter(logging.Formatter):

    def __init__(self, fmt, datefmt=None):
        """
        Init given the log line format and date format
        """
        logging.Formatter.__init__(self, fmt, datefmt)

    def format(self, record):
        """
        Override format function
        """
        msg = logging.Formatter.format(self, record)

        if record.message != "":
            parts = msg.split(record.message)
            msg = msg.replace('\n', '\n' + parts[0])

        return msg


log_colors = {
    logging.DEBUG: "\033[1;34m",  # blue
    logging.INFO: "\033[1;32m",  # green
    logging.WARNING: "\033[1;35m",  # magenta
    logging.ERROR: "\033[1;31m",  # red
    logging.CRITICAL: "\033[1;41m",  # red reverted
}


def file_handler(log_path=LOG_BASE_DIR):
    if not os.path.exists(log_path):
        os.mkdir(log_path)

    handler = logging.handlers.RotatingFileHandler(
        filename=os.path.join(log_path, 'tp_app.log'),
        mode='a+',
        maxBytes=1024 * 1024 * 3,
        backupCount=9,
        encoding='utf-8',
    )
    my_fmt = logging.Formatter(
        fmt='%(asctime)s %(pathname)s[line:%(lineno)d] %(name)s %(levelname)-8s %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    handler.setLevel(logging.WARNING)
    handler.setFormatter(my_fmt)
    return handler


def basic_logger(level=logging.DEBUG):
    LOG_FORMAT = '%(asctime)s %(levelname_c)-8s %(message)s'
    DATE_FORMAT = '%d-%m-%Y %H:%M:%S'
    logging.basicConfig(
        level=level,
        stream=sys.stdout
    )
    formatter = NewLineFormatter(LOG_FORMAT, datefmt=DATE_FORMAT)

    orig_record_factory = logging.getLogRecordFactory()

    def record_factory(*args, **kwargs):
        record = orig_record_factory(*args, **kwargs)
        record.levelname_c = "{}{}{}".format(log_colors[record.levelno], record.levelname, "\033[0m")  # 定制LogRecord属性
        record.message_shorten = "{}".format(textwrap.shorten(record.msg, width=1000, placeholder='...'))
        return record

    logging.setLogRecordFactory(record_factory)
    logger = logging.getLogger()
    logger.handlers[0].setFormatter(formatter)
    return logger


logger = basic_logger()
logger.addHandler(file_handler())

if __name__ == '__main__':
    logger.debug("这是一条调试")
    logger.info("这是一条信息")
    logger.info("这是一条\n\t信息")
    logger.warning("这是一条警告")
    logger.error("这是一条错误")
    logger.critical("这是一条批判")
