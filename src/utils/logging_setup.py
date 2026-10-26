import os
import logging
from logging.handlers import RotatingFileHandler

def setup_logging():
    log_dir = "logs"
    os.makedirs(log_dir, exist_ok=True)  # 'dtype=str' yahan se hata diya gaya hai
    log_file = os.path.join(log_dir, "supportpearlz.log")
    
    # Logger configuration
    logger = logging.getLogger("SupportPearlzLogger")
    logger.setLevel(logging.INFO)
    
    if not logger.handlers:
        # File handler (Rotating)
        file_handler = RotatingFileHandler(log_file, maxBytes=5*1024*1024, backupCount=3)
        file_formatter = logging.Formatter('%(asctime)s - %(levelname)s - [%(filename)s:%(lineno)d] - %(message)s')
        file_handler.setFormatter(file_formatter)
        logger.addHandler(file_handler)
        
        # Console handler
        console_handler = logging.StreamHandler()
        console_formatter = logging.Formatter('%(levelname)s: %(message)s')
        console_handler.setFormatter(console_formatter)
        logger.addHandler(console_handler)
        
    return logger

logger = setup_logging()