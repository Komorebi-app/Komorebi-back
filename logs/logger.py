import sys

from pathlib import Path
from loguru import logger

LOG_DIR = Path(__file__).parent / "logs"
LOG_DIR.mkdir(exist_ok=True)

LOG_COLORIZED_FORMAT = "<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level}</level> | {message}"
LOG_FORMAT = "{time:YYYY-MM-DD HH:mm:ss} | {level} | {message}"

logger.remove()

logger.add(sys.stdout, colorize=True, format=LOG_COLORIZED_FORMAT)

logger.add(LOG_DIR / "app.log", rotation="1 day", retention="30 days", level="INFO", format=LOG_FORMAT)

logger.add(LOG_DIR / "errors.log", rotation="1 day", retention="60 days", level="ERROR", format=LOG_FORMAT)

logger.add(LOG_DIR / "app.json", format="{time} {level} {message}", serialize=True)
