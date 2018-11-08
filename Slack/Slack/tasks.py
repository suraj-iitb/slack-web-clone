from celery import shared_task
from celery.utils.log import get_task_logger
from workspace import views

logger=get_task_logger(__name__)

# This is the decorator which a celery worker uses
@shared_task(name="send_message_task")
def send_message_task(userid, channel_id, email,message):
    logger.info("Sent email")
    return views.send_message(userid, channel_id, email,message)
