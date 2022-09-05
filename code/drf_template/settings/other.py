import datetime
import os

XADMIN_URL = os.getenv('XADMIN_URL', 'wZNN02Mgq0I0qQPCwQviuDvyh8Nr9lpO')

OPEN_SWAGGER = os.getenv('OPEN_SWAGGER', 'False').lower() == 'true'

# swagger
SWAGGER_SETTINGS = {
    'LOGIN_URL': '/xadmin/',
    'LOGOUT_URL': '/xadmin/logout',
    'SECURITY_DEFINITIONS': {
        'Bearer': {
            'in': 'header',
            'name': 'api-key',
            'type': 'apiKey',
        },
        'JWT': {
            'in': 'header',
            'name': 'Authorization',
            'type': 'apiKey',
        }
    }
}

# drf-extensions
REST_FRAMEWORK_EXTENSIONS = {
    'DEFAULT_CACHE_RESPONSE_TIMEOUT': 10 * 60,
    'DEFAULT_USE_CACHE': 'default',
}

# jwt
JWT_AUTH = {
    'JWT_EXPIRATION_DELTA': datetime.timedelta(days=7),
    'JWT_AUTH_HEADER_PREFIX': 'JWT',
}

# multi database
DATABASE_ROUTERS = ['drf_template.database_router.DatabaseAppsRouter']

DATABASE_APPS_MAPPING = {
    # app_name:db_name
    'admin': 'default',
    'auth': 'default',
    'contenttypes': 'default',
    'sessions': 'default',

    'xadmin': 'default',

    'user': 'default',
    'goods': 'default',
}

# cors
CORS_ORIGIN_ALLOW_ALL = True
