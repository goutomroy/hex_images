from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_cookie
from rest_framework import mixins, permissions, viewsets
from rest_framework.viewsets import GenericViewSet

from apps.photos.models.photo import Photo
from apps.photos.serializers.photo import PhotoCreateSerializer, PhotoSerializer
from apps.photos.throttles.photo import (
    PhotoCreateUserRateThrottle,
    PhotoDefaultUserRateThrottle,
)


class PhotoViewSet(
    viewsets.mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
    mixins.DestroyModelMixin,
    GenericViewSet,
):
    queryset = Photo.objects.all()
    serializer_class = PhotoSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        return (
            super()
            .get_queryset()
            .prefetch_related("thumbnails")
            .filter(user=self.request.user)
        )

    def get_serializer_class(self):
        if self.action == "create":
            return PhotoCreateSerializer
        return self.serializer_class

    def get_throttles(self):
        if self.action == "create":
            custom_throttle_classes = [PhotoCreateUserRateThrottle]
        else:
            custom_throttle_classes = [PhotoDefaultUserRateThrottle]
        return [throttle() for throttle in custom_throttle_classes]

    # With cookie: cache requested url for each user for 3 minutes
    @method_decorator(cache_page(60 * 3))
    @method_decorator(vary_on_cookie)
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
