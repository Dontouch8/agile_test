import time

import schedule

from agile import get_images
from config import UPDATE_INTERVAL, logger


def main():
    get_images()
    schedule.every(UPDATE_INTERVAL).minutes.do(get_images)
    logger.info("Starting scheduler")
    while True:
        schedule.run_pending()
        time.sleep(1)


if __name__ == "__main__":
    main()
