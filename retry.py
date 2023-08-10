# 重试自定义的次数
def retry(times):
    def wrapper(func):
        def inner_wrapper(*args, **kwargs):
            i = 0
            while i < times:
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    print('重试： '+ str(i))
                    i += 1
        return inner_wrapper
    return wrapper
