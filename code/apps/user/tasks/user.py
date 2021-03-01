import logging

from celery import shared_task

logger = logging.getLogger('default')


@shared_task(queue='default', ignore_result=True)
def test_task(user_id: int):
    log_data = {
        'task': 'test_task',
        'user_id': user_id
    }
    logger.info(log_data)
    return user_id
