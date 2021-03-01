"""
python manage.py runscript test_scripts --traceback --script-args args1
"""
import os

if __name__ == '__main__':
    import django
    import sys

    pwd = os.path.dirname(os.path.realpath(__file__))
    sys.path.insert(0, pwd)
    project_path = os.path.dirname(pwd)
    sys.path.insert(0, project_path)

    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "drf_template.settings")
    django.setup()

import logging

logger = logging.getLogger('default')


def run(*args):
    logger.info(args)


if __name__ == '__main__':
    run()
