import logging
import os
from datetime import datetime


#log File Name
LOG_FILE_NAME = f"{datetime.now().strftime('%m_%d_%Y_%H_%M_%S')}.log"

#Log directory
LOG_FILE_DIR = os.path.join(os.getcwd(),"logs")


#create log folder if not available

os.makedirs(LOG_FILE_DIR,exist_ok=True)

#log file path

LOG_FILE_PATH = os.path.join(LOG_FILE_DIR,LOG_FILE_NAME)

logging.basicConfig(
    filename=LOG_FILE_PATH,
    format="[%(asctime)s] %(lineno)d %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)

# Testing the logger file
"""
if __name__=="__main__":
    logging.info("Testing the Logging")

    """
