from flask import jsonify

# @log # make_return = log(make_return)
def make_return(success, message='', data={}):
    """
    success: 返回标志
    message: 提示信息
    data: 返回数据
    """
    rv = {
        'success': success,
        'message': message,
        'data': data
    }
    return jsonify(rv)


def log(func):
    def wrapper(*args, **kw):
        app.logger.info('call %s():' % func.__name__)
        return func(*args, **kw)
    return wrapper