from decimal import Decimal
import json
import re

from django.forms.models import model_to_dict
from djangorestframework_camel_case.util import (
    camelize_re,
    underscore_to_camel,
)


def json2str(obj_or_list, intent=4, ensure_ascii=False):
    return json.dumps(obj_or_list, indent=intent, ensure_ascii=ensure_ascii)


def generate_response_str(data, message='ok', code=200):
    return json2str({'code': code, 'message': message, 'data': data})


def str2decimal(s) -> Decimal:
    try:
        result = Decimal(str(s))
    except:
        result = Decimal()
    return result


def underline_2_hump(s: str):
    return re.sub(camelize_re, underscore_to_camel, s)
