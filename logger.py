import logging
import os
from datetime import datetime


def setup_logger(log_dir='logs'):
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    current_time = datetime.now().strftime('%Y%m%d_%H%M%S')
    log_file = os.path.join(log_dir, f'GradeChecker_{current_time}.log')

    logger = logging.getLogger('GradeChecker')
    logger.setLevel(logging.INFO)

    file_handler = logging.FileHandler(log_file)
    file_handler.setLevel(logging.INFO)

    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)

    formatter = logging.Formatter('[%(asctime)s][%(name)s][%(levelname)s] %(message)s')
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger


logger = setup_logger()
