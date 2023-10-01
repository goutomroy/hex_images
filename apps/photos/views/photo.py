from rest_framework import mixins, permissions, viewsets
from rest_framework.viewsets import GenericViewSet

from apps.photos.models.photo import Photo
from apps.photos.serializers.photo_serializer import (
    PhotoCreateSerializer,
    PhotoSerializer,
)


class PhotoViewSet(
    viewsets.mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
    GenericViewSet,
):
    queryset = Photo.objects.all()
    serializer_class = PhotoSerializer
    permission_classes = [permissions.IsAuthenticated]

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

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
