import logging
import time

from celery import shared_task

logger = logging.getLogger('default')


# @shared_task(queue='default', ignore_result=True)
@shared_task(queue='default')  # celery 默认会把结果保留 24 小时
def test_task(user_id: int):
    log_data = {
        'task': 'test_task',
        'user_id': user_id
    }
    logger.info(log_data)
    time.sleep(10)  # 模拟耗时操作
    log_data.update({'msg': '任务完成'})
    logger.info(log_data)
    return user_id
