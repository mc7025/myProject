import logging
from config import DEBUG
if DEBUG:
    level = logging.DEBUG
else:
    level = logging.INFO
LOGGER = logging.Logger('test_os')
LOGGER.setLevel(level)
formatter = logging.Formatter(fmt='%(asctime)s [%(threadName)s] [%(name)s:%(lineno)d] [%(module)s:%(funcName)s] [%(levelname)s]- %(message)s')
handler = logging.StreamHandler()
handler.setLevel(level)
handler.setFormatter(formatter)
LOGGER.addHandler(handler)
