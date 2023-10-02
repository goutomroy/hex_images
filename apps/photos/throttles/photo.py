from django.conf import settings
from rest_framework.throttling import UserRateThrottle


class PhotoCreateUserRateThrottle(UserRateThrottle):
    THROTTLE_RATES = {"user": f"{settings.PHOTO_CREATE_THROTTLE_THRESHOLD}/min"}


class PhotoDefaultUserRateThrottle(UserRateThrottle):
    THROTTLE_RATES = {"user": f"{settings.THROTTLE_THRESHOLD}/min"}
