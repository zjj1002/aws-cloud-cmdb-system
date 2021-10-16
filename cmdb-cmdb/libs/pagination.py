from tornado import gen


# 分页的装饰器
def pagination_util(func):
    @gen.coroutine
    def wrap(context, *args, **kwargs):
        page = int(context.get_argument('page', default='1', strip=True))
        size = int(context.get_argument('size', default='10', strip=True))
        result = func(context, *args, **kwargs)
        data = result[(page-1) * size:page * size]
        context.write(dict(code=0, msg='success', total=len(result), data=data))
        return result
    return wrap



