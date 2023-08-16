import datetime
import os
import sys

from contrib.grpc.interceptors import TraceRequestDataInterceptor

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
    'django_socio_grpc_quickstart': 'default',
    'generate_crud_code_example': 'default',
}

# cors
CORS_ORIGIN_ALLOW_ALL = True

IS_GRPC_SERVER = 'grpcrunserver' in ''.join(sys.argv)

if IS_GRPC_SERVER:
    GRPC_FRAMEWORK = {
        'ROOT_HANDLERS_HOOK': 'django_socio_grpc_quickstart.apis.handlers.grpc_handlers',
        'GRPC_CHANNEL_PORT': 50051,
        'SERVER_INTERCEPTORS': [TraceRequestDataInterceptor()],
    }

    from .opentelemetry import OTEL_PYTHON_DJANGO_INSTRUMENT

    if OTEL_PYTHON_DJANGO_INSTRUMENT:
        from opentelemetry.instrumentation.grpc import GrpcInstrumentorServer, server_interceptor

        GrpcInstrumentorServer().instrument()

        # 或者 GRPC_FRAMEWORK['SERVER_INTERCEPTORS'] = [server_interceptor()]
