from .base import *  # noqa

# project constant
MAX_UPLOAD_SIZE = 3 * 1024 * 1024  # 3.0 MB
THROTTLE_THRESHOLD = 10
PHOTO_CREATE_THROTTLE_THRESHOLD = 10

# Cache
CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.redis.RedisCache",
        "LOCATION": "redis://redis:6379/0",
    }
}


LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
        },
    },
    "root": {
        "handlers": ["console"],
        "level": "DEBUG",  # Change this level as per your requirement
    },
    "loggers": {
        "django.db.backends": {
            "handlers": ["console"],
            "level": "DEBUG",  # Change this level as per your requirement
            "propagate": False,
        },
    },
}
