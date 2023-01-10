import os

REDIS_CONFIG = {
    'host': os.getenv('REDIS_HOST', 'localhost'),
    'port': os.getenv('REDIS_PORT', '6379'),
    'password': os.getenv('REDIS_PASSWORD', '123456'),
}

CACHES = {
    'default': {
        'BACKEND': 'redis_cache.RedisCache',
        'LOCATION': [
            f'{REDIS_CONFIG["host"]}:{REDIS_CONFIG["port"]}'
        ],
        'OPTIONS': {
            # 'SERIALIZER_CLASS': 'redis_cache.serializers.JSONSerializer',
            'DB': 0,
            'PASSWORD': REDIS_CONFIG['password'] or None,
            'PARSER_CLASS': 'redis.connection.HiredisParser',
            'CONNECTION_POOL_CLASS': 'redis.BlockingConnectionPool',
            'CONNECTION_POOL_CLASS_KWARGS': {
                'max_connections': 100,
                'timeout': 20,
            },
            'MAX_CONNECTIONS': 100,
            'PICKLE_VERSION': -1,
        },
    },
}
