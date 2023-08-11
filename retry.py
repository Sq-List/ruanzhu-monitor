import time

from ruan_zhu_exception import RuanZhuExceptin

# 重试自定义的次数
def retry(times):
    def wrapper(func):
        def inner_wrapper(*args, **kwargs):
            i = 0
            while i < times:
                try:
                    return func(*args, **kwargs)
                except RuanZhuExceptin as e:
                    print('重试： '+ str(i))
                    i += 1
                    print('暂停10秒')
                    time.sleep(10)
        return inner_wrapper
    return wrapper
