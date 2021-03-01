import os

from kombu import Queue, Exchange

REDIS_CONFIG = {
    'host': os.getenv('REDIS_HOST', 'localhost'),
    'port': os.getenv('REDIS_PORT', '6379'),
    'password': os.getenv('REDIS_PASSWORD', '123456'),
}
if REDIS_CONFIG['password']:
    CELERY_BROKER_URL = f'redis://:{REDIS_CONFIG["password"]}@{REDIS_CONFIG["host"]}:{REDIS_CONFIG["port"]}/14'
    CELERY_RESULT_BACKEND = f'redis://:{REDIS_CONFIG["password"]}@{REDIS_CONFIG["host"]}:{REDIS_CONFIG["port"]}/15'
else:
    CELERY_BROKER_URL = f'redis://{REDIS_CONFIG["host"]}:{REDIS_CONFIG["port"]}/14'
    CELERY_RESULT_BACKEND = f'redis://{REDIS_CONFIG["host"]}:{REDIS_CONFIG["port"]}/15'
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_TIMEZONE = 'Asia/Shanghai'

CELERYD_MAX_TASKS_PER_CHILD = 100  # worker 每执行100次任务就销毁，防止内存泄漏

CELERY_QUEUES = (
    Queue('default', exchange=Exchange('default'), routing_key='default'),
)

CELERY_DEFAULT_QUEUE = 'default'
CELERY_IGNORE_RESULT = True  # 不关心任务结果
