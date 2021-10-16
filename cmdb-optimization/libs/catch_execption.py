from tornado import gen


# 捕获异常的装饰器
def catch_exceptions_util(func):
    @gen.coroutine
    def wrap(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except:
            print('Error execute: %s' % func.__name__)
    return wrap


