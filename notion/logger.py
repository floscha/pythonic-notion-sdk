import logging
from os import environ

logger = logging.getLogger("pythonic-notion-sdk")

logging.basicConfig(
    level=environ.get("LOGLEVEL", "INFO"),
    filename=environ.get("LOGFILE"),
    format="%(asctime)s %(levelname)s [%(module)s:%(funcName)s:%(lineno)d] %(message)s",
)
