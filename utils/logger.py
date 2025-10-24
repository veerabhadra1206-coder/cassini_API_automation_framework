import logging
import os
import shutil

def setup_logger(log_dir="logs", log_file="test_run.log"):
    # Remove old logs
    if os.path.exists(log_dir):
        shutil.rmtree(log_dir)
    os.makedirs(log_dir)

    log_path = os.path.join(log_dir, log_file)

    # Get root logger
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    # Remove existing handlers (avoid duplicates)
    for handler in logger.handlers[:]:
        logger.removeHandler(handler)

    # File handler
    file_handler = logging.FileHandler(log_path)
    formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    # log to console
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    logger.info("----- New Test Run Started -----")

    return logger
