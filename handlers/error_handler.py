import logging

logger = logging.getLogger(__name__)

def error_handler(update, context):
    logger.error(msg="Exception while handling an update:", exc_info=context.error)
