# utils/logger.py
import logging
from config.settings import LOG_FILE

_loggers = {}  # Guardamos los loggers por path

def setup_logger(log_path: str):
    """Crea o retorna un logger asociado a log_path"""
    if log_path in _loggers:
        return _loggers[log_path]

    logger = logging.getLogger(log_path)
    logger.setLevel(logging.INFO)

    # Evitar duplicar handlers
    if not logger.handlers:
        handler = logging.FileHandler(log_path)
        formatter = logging.Formatter("%(asctime)s [%(levelname)s] %(message)s", "%Y-%m-%d %H:%M:%S")
        handler.setFormatter(formatter)
        logger.addHandler(handler)

    _loggers[log_path] = logger
    return logger

def get_logger(log_path: str):
    """Retorna un logger previamente configurado con setup_logger"""
    return _loggers.get(log_path)

def log_info(message: str):
    logging.info(message)

def log_error(message: str):
    logging.error(message)

def log_warning(message: str):
    logging.warning(message)
