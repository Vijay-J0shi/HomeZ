# Sets up logging to track what’s going on
# Helps me see errors and stuff

import logging

def start_log():
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )
    return logging.getLogger(__name__)