from tornado import gen


# 分页的装饰器
def pagination_util(func):
    @gen.coroutine
    def wrap(context, *args, **kwargs):
        page = int(context.get_argument('page', default='1', strip=True))
        size = int(context.get_argument('size', default='10', strip=True))
        export_csv = context.get_argument('export_csv', default="0", strip=True)
        result = func(context, *args, **kwargs)
        data = result[(page-1) * size:page * size]
        if export_csv == "1":
            import csv
            filename = "export_report.csv"
            data_dict = data
            headers = [list(i.keys()) for i in data_dict][0]
            rows = [list(i.values()) for i in data_dict]
            with open(filename, "w", encoding="utf8", newline="") as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(headers)
                writer.writerows(rows)
            context.set_header('Content-Type', 'application/octet-stream')
            context.set_header('Content-Disposition', 'attachment; filename=' + filename)
            buf_size = 4096
            with open(filename, 'rb') as f:
                while True:
                    data = f.read(buf_size)
                    if not data:
                        break
                    context.write(data)
            context.finish()
        else:
            context.write(dict(code=0, msg='success', total=len(result), data=data))
        return result
    return wrap



