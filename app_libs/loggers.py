"""
    Version: 1.0.0
    Author: MSI Shafik
"""

import logging

logging.basicConfig(level=logging.DEBUG)


def log_info():
    """
    By this function will initialed log information data
    :return:
    """
    # Get an instance of a logger
    logging.basicConfig(level=logging.DEBUG)
    return logging.getLogger('general')


def log_exception():
    """
    By this function will initialed log exception data
    :return:
    """
    logging.basicConfig(level=logging.DEBUG)
    return logging.getLogger('exceptions_log')

