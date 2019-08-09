import logging.config


conf = {
    'version': 1,
    'disable_existing_logger': False,
    'formatters': {
        'standard': {
            'format': '%(asctime)s [%(threadName)s:%(thread)d] [%(name)s:%(lineno)d] [%(module)s:%(funcName)s] [%(levelname)s]- %(message)s'
        }
    },
    'filters': {

    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'standard',
        }
    },
    'logger': {
        'test_OS': {
            'level': 'DEBUG',
            'propagate': False,
            'handlers': ['console']
        },
        'hddl_l_sw_validation.testcases.test_sc': {
            'level': 'INFO',
            'propagate': False,
            'handlers': ['console']
        }
    }
}


logging.config.dictConfig(conf)