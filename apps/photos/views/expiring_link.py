from django.utils import timezone
from rest_framework import mixins, permissions, viewsets
from rest_framework.viewsets import GenericViewSet

from apps.photos.models.expiring_link import ExpiringLink
from apps.photos.permissions import CanListCreateRetrieveExpiringLink
from apps.photos.serializers.expiring_link import ExpiringLinkSerializer


class ExpiringLinkViewSet(
    viewsets.mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
    mixins.DestroyModelMixin,
    GenericViewSet,
):
    queryset = ExpiringLink.objects.all()
    serializer_class = ExpiringLinkSerializer
    permission_classes = [
        permissions.IsAuthenticated,
        CanListCreateRetrieveExpiringLink,
    ]

    def get_queryset(self):
        return (
            super()
            .get_queryset()
            .prefetch_related("image__user")
            .filter(
                image__user=self.request.user,
                expired_at__gt=timezone.now(),
            )
        )

    # def perform_create(self, serializer):
    #     return super().perform_create(serializer)
