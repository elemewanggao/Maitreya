# -*- coding:utf-8 -*-
"""全局的一些配置."""


# 跨域请求配置
CORS_CONF = {r'/*': {'origins': '*'}}

# 日志设置
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'root': {
        'handlers': ['all', 'console'],
        'level': 'INFO'
    },
    'handlers': {
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'uniform',
        },
        'all': {
            'class': 'logging.handlers.RotatingFileHandler',
            'level': 'INFO',
            'formatter': 'uniform',
            'filename': '/data/log/Maitreya/maitreya.log',
            'mode': 'a',
            'maxBytes': 262144000,  # 200M
            'backupCount': 10,
        },
    },
    'formatters': {
        'uniform': {
            'format': '%(asctime)s %(levelname)-6s %(name)s[%(process)d]: '
                      '%(module)s => %(funcName)s ##  %(message)s',
        }
    }
}

# 数据库设置
MYSQL = {
    'merchant_clear': {
        'user': 'root',
        'passwd': 'root',
        'host': 'localhost',
        'port': 3306,
        'db': 'talaris_merchant_clear',
    },
    'team_clear': {
        'user': 'root',
        'passwd': 'root',
        'host': 'localhost',
        'port': 3306,
        'db': 'talaris_team_clear',
    },
    'data_center_clear': {
        'user': 'root',
        'passwd': 'root',
        'host': 'localhost',
        'port': 3306,
        'db': 'lpd_data_center'
    },
    'ares_icon': {
        'user': 'root',
        'passwd': 'root',
        'host': 'localhost',
        'port': 3306,
        'db': 'ares',
    }
}


DEBUG = False
