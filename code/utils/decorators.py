import functools
import time


def retry(stop_max_attempt_number=3, wait_fixed: float = 2, raise_exception=None):
    """
    方法重试装饰器
    :param stop_max_attempt_number: 最大重试次数
    :param wait_fixed: 重试间隔(单位秒）
    :param raise_exception: 需要主动抛出的异常
    """

    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kw):
            retry_num = 0
            while retry_num < stop_max_attempt_number:
                rs = None
                try:
                    rs = func(*args, **kw)
                    break
                except Exception as e:
                    retry_num += 1
                    time.sleep(wait_fixed)
                    if retry_num == stop_max_attempt_number:
                        raise raise_exception or Exception(e)
                finally:
                    if rs:
                        return rs

        return wrapper

    return decorator
