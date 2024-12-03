import logging.config

LOGGING_CONFIG = {
    'version': 1,
    'disable_existing_loggers': False,  
    'formatters': {
        'simple': {
            'format': '%(asctime)s - %(levelname)s - %(message)s'
        },
        'detailed': {
            'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        },
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'simple'
        },
        'file': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': 'app.log',
            'formatter': 'detailed'
        },
        'rotating_file': {
            'level': 'ERROR',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': 'error.log',
            'maxBytes': 10485760,  # 10 MB
            'backupCount': 5,  
            'formatter': 'detailed'
        },
    },
    'loggers': {
        '': {  
            'handlers': ['console', 'file'],
            'level': 'DEBUG',
            'propagate': True,
        },
        'rotating_file': { 
            'handlers': ['rotating_file'],
            'level': 'ERROR',
            'propagate': False,
        },
    },
}


logging.config.dictConfig(LOGGING_CONFIG)
