import time
from datetime import date, datetime
from typing import Union


def get_now_s_ts() -> int:
    """
    返回当前时间戳，单位秒
    :return: int
    """
    return int(time.time())


def get_now_ms_ts() -> int:
    """
    返回当前时间戳，单位毫秒
    :return: int
    """
    return int(time.time() * 1000)


def get_min_utc_datetime():
    return datetime(1970, 1, 1)


def get_max_utc_datetime():
    return datetime(9999, 12, 31)


def get_min_utc_date():
    return date(1970, 1, 1)


def get_max_utc_date():
    return date(9999, 12, 31)


def get_today_0_hour_ts():
    today_datetime = datetime.now()
    today_0_ts = int(datetime(today_datetime.year, today_datetime.month, today_datetime.day).timestamp())
    return today_0_ts


def dt2ts(dt: datetime, return_int_with_second=True) -> Union[int, float]:
    ts = time.mktime(dt.timetuple())
    if return_int_with_second:
        return int(ts)
    return ts


def str2datetime(s: str, format='%Y-%m-%d') -> Union[datetime, None]:
    """
    日期型字符转datetime
    """
    if isinstance(s, datetime):
        return s
    try:
        return datetime.strptime(s, format)
    except:
        pass
    try:
        return datetime.strptime(s, '%Y-%m-%d %H:%M:%S')
    except:
        pass
    try:
        return datetime.fromtimestamp(int(s))
    except:
        pass
    try:
        return datetime.fromtimestamp(int(s) / 1000)
    except:
        pass
    return None
