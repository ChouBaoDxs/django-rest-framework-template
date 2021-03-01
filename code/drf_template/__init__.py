from .celery_app import app as celery_app
from .monkey_patching import *

__all__ = ("celery_app",)

try:
    import MySQLdb  # mysqlclient
except:
    import pymysql  # pymysql

    pymysql.install_as_MySQLdb()
    pymysql.version_info = (1, 4, 4, 'final', 0)
