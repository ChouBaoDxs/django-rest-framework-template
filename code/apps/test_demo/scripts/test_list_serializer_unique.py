"""
python manage.py runscript test_scripts --traceback --script-args args1
"""
import os

if __name__ == '__main__':
    import django
    import sys

    pwd = os.path.dirname(os.path.realpath(__file__))
    sys.path.insert(0, pwd)
    project_path = os.path.dirname(os.path.dirname(pwd))
    sys.path.insert(0, project_path)

    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "drf_template.settings")
    django.setup()

import logging

logger = logging.getLogger('default')

from rest_framework import serializers
from test_demo.models import TestListSerializerUnique


class TestListSerializerUniqueSer(serializers.ModelSerializer):
    class Meta:
        model = TestListSerializerUnique
        fields = ['id', 'code']


def run(*args):
    data_list = [
        {'code': '1'},
        {'code': '1'},
        {'code': '2'},
    ]
    ser = TestListSerializerUniqueSer(data=data_list, many=True)
    ser.is_valid(True)
    ser.save()


if __name__ == '__main__':
    run()
