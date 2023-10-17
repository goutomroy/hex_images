from django.utils import timezone
from rest_framework import mixins, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import GenericViewSet

from apps.photos.models.expiring_link import ExpiringLink
from apps.photos.permissions import CanListCreateRetrieveExpiringLink
from apps.photos.serializers.expiring_link import ExpiringLinkSerializer
from apps.photos.throttles.expiring_link import ExpiringLinkUserRateThrottle


class ExpiringLinkViewSet(
    viewsets.mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
    mixins.DestroyModelMixin,
    GenericViewSet,
):
    queryset = ExpiringLink.objects.all()
    serializer_class = ExpiringLinkSerializer
    throttle_classes = (ExpiringLinkUserRateThrottle,)
    permission_classes = (
        IsAuthenticated,
        CanListCreateRetrieveExpiringLink,
    )

    def get_queryset(self):
        return (
            super()
            .get_queryset()
            .select_related("image__user")
            .filter(
                image__user=self.request.user,
                expired_at__gt=timezone.now(),
            )
        )
