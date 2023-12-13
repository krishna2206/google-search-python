import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.ERROR)

handler = logging.StreamHandler()
formatter = logging.Formatter('%(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)

logger.addHandler(handler)