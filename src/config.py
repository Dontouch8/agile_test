import os

from loguru import logger

API_KEY = "23567b218376f79d9415"
API_URL = "http://interview.agileengine.com"
HEADERS = {"Content-Type": "application/json", "user-agent": "PostmanRuntime/7.26.8"}

UPDATE_INTERVAL = 120
ROOT_PATH = os.path.dirname(os.path.abspath(__file__))

logger.add(
    f"{ROOT_PATH}/out.log",
    format="<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | <cyan>{level: <8}</cyan> <level>{message}</level>",
    level="DEBUG",
    colorize=True,
)
