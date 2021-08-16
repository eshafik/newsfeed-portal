"""
    Version: 1.0.0
    Author: MSI Shafik
"""

import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

__all__ = ["LOGGING"]

# checking log folder has exists or not if not create the log folder
path = BASE_DIR + "/app_logs"
if not os.path.exists(path):
    os.makedirs(path)


# LOG SETUP #
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
        },
        'debug_file': {
            'level': 'DEBUG',
            'filename': os.path.join(BASE_DIR, 'app_logs/django_debug.log'),
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'when': 'MIDNIGHT',
            'formatter': 'main_formatter'
        },
        'general_file': {
            'level': 'DEBUG',
            'filename': os.path.join(BASE_DIR, 'app_logs/app_general.log'),
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'when': 'MIDNIGHT',
            'formatter': 'main_formatter'
        },
        'exceptions_file': {
            'level': 'DEBUG',
            'filename': os.path.join(BASE_DIR, 'app_logs/exceptions.log'),
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'when': 'MIDNIGHT',
            'formatter': 'main_formatter'
        },
    },
    'formatters': {
        'main_formatter': {
            'format': '%(levelname)s | %(asctime)s | %(filename)s | %(module)s:%(funcName)s:%(lineno)d | %(message)s',
            'datefmt': "%Y-%m-%d %H:%M:%S",
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console', 'debug_file'],
            'level': 'DEBUG',
            'propagate': True,
        },
        'django.utils.autoreload': {
            'handlers': ['debug_file'],
            'level': 'ERROR',
            'propagate': True,
        },
        'django.db.backends': {
            'handlers': ['debug_file'],
            'level': 'INFO',
            'propagate': True,
        },
        'general': {
            'handlers': ['general_file'],
            'level': 'DEBUG',
            'propagate': True,
        },
        'exceptions_log': {
            'handlers': ['exceptions_file'],
            'level': 'DEBUG',
            'propagate': True,
        },

        'django.template': {
            'handlers': ['debug_file'],
            'level': 'INFO',
            'propagate': True,
        },
        'parso': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': False,
        },
    },
}
# LOG SETUP END #
