from django.conf import settings
from rest_framework.throttling import UserRateThrottle


class ExpiringLinkUserRateThrottle(UserRateThrottle):
    THROTTLE_RATES = {"user": f"{settings.THROTTLE_THRESHOLD}/min"}
