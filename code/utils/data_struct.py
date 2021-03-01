import re

from django.utils.encoding import force_text
from django.utils.functional import Promise
from djangorestframework_camel_case.util import (
    camelize_re,
    is_iterable,
    underscore_to_camel,
)


def camelize(data):
    # from djangorestframework_camel_case.util import camelize 转成的是 OrderedDict，我们重写一个是 dict 的
    if isinstance(data, Promise):
        data = force_text(data)
    if isinstance(data, dict):
        new_dict = dict()
        for key, value in data.items():
            if isinstance(key, Promise):
                key = force_text(key)
            if isinstance(key, str) and "_" in key:
                new_key = re.sub(camelize_re, underscore_to_camel, key)
            else:
                new_key = key
            new_dict[new_key] = camelize(value)
        return new_dict
    if is_iterable(data) and not isinstance(data, str):
        return [camelize(item) for item in data]
    return data
