# drf 不支持输入时间戳格式的DateTime，我们打个猴子补丁，参考文章：
# https://stackoverflow.com/questions/26083583/serialize-a-datetime-as-an-integer-timestamp
import datetime

from django.utils.dateparse import parse_datetime
from rest_framework import ISO_8601
from rest_framework.fields import DateTimeField
from rest_framework.settings import api_settings
from rest_framework.utils import humanize_datetime

from utils.date_and_time import str2datetime


def to_internal_value(self, value):
    input_formats = getattr(self, 'input_formats', api_settings.DATETIME_INPUT_FORMATS)

    if isinstance(value, datetime.date) and not isinstance(value, datetime.datetime):
        self.fail('date')

    # 尝试转换为日期类型
    tmp_value = str2datetime(value)
    if tmp_value:
        value = tmp_value

    if isinstance(value, datetime.datetime):
        return self.enforce_timezone(value)

    for input_format in input_formats:
        if input_format.lower() == ISO_8601:
            try:
                parsed = parse_datetime(value)
                if parsed is not None:
                    return self.enforce_timezone(parsed)
            except (ValueError, TypeError):
                pass
        else:
            try:
                parsed = self.datetime_parser(value, input_format)
                return self.enforce_timezone(parsed)
            except (ValueError, TypeError):
                pass

    humanized_format = humanize_datetime.datetime_formats(input_formats)
    self.fail('invalid', format=humanized_format)


DateTimeField.to_internal_value = to_internal_value
