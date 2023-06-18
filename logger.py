import logging

logger = logging.getLogger()
if __name__ != '__main__':
    logger = logging.getLogger('gunicorn.error')