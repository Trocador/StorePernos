import os
from utils import logger

def test_logger_creates_log_file(tmp_path):
    log_file = tmp_path / "test.log"
    logger = get_logger(log_file)

    logger.info("Mensaje de prueba")

    assert log_file.exists()
    content = log_file.read_text()
    assert "Mensaje de prueba" in content

def get_logger(log_file):
    import logging

    logger = logging.getLogger("test_logger")
    logger.setLevel(logging.INFO)

    fh = logging.FileHandler(log_file)
    fh.setLevel(logging.INFO)

    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    fh.setFormatter(formatter)

    logger.addHandler(fh)

    return logger