
class UnknownError(Exception):
    """未知错误"""
    def __init__(self, message="未知错误"):
        self.message = message
        self.code = 500


class ParamsError(UnknownError):
    """参数有误"""
    def __init__(self, message="参数有误"):
        self.message = message
        self.code = 401


class RecordNotExisted(UnknownError):
    """记录不存在"""
    def __init__(self, message="记录不存在"):
        self.message = message
        self.code = 404


class RecordExisted(UnknownError):
    """记录已存在"""
    def __init__(self, message="记录已存在"):
        self.message = message
        self.code = 405


class EnumNotExisted(UnknownError):
    """枚举值不存在"""
    def __init__(self, message="枚举值不存在"):
        self.message = message
        self.code = 406
