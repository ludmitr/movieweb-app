import logging
import os

def setup_logger():
    log_dir = 'logs'
    log_file = 'app.log'
    log_path = os.path.join(log_dir, log_file)

    logger = logging.getLogger(__name__)
    logger.setLevel(logging.ERROR)

    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    handler = logging.FileHandler(log_path)
    handler.setLevel(logging.ERROR)

    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)

    logger.addHandler(handler)

    return logger
