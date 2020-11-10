import os

from loguru import logger

UPDATE_INTERVAL = 120
ROOT_PATH = os.path.dirname(os.path.abspath(__file__))
print(ROOT_PATH)

logger.add(
    f"{ROOT_PATH}/out.log",
    format="<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | <cyan>{level: <8}</cyan> <level>{message}</level>",
    level="DEBUG",
    colorize=True,
)
