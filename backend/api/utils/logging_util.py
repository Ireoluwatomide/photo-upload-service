import logging
from logging.handlers import RotatingFileHandler


logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)  # Set the logging level for this logger

# Create a rotating file handler
handler = RotatingFileHandler(
    'backend_app.log', maxBytes=1000000, backupCount=5)

# Create a formatter and add it to the handler
formatter = logging.Formatter(
    '%(asctime)s - %(name)s - [%(levelname)s] - %(message)s')
handler.setFormatter(formatter)

# Add the handler to the logger
logger.addHandler(handler)
