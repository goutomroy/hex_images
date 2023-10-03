from rest_framework import mixins, permissions
from rest_framework.viewsets import GenericViewSet

from apps.photos.models.thumbnail_photo import ThumbnailPhoto
from apps.photos.serializers.thumbnail_photo import ThumbnailPhotoSerializer


class ThumbnailPhotoViewSet(mixins.ListModelMixin, GenericViewSet):
    queryset = ThumbnailPhoto.objects.all()
    serializer_class = ThumbnailPhotoSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return (
            super()
            .get_queryset()
            .select_related("original_image")
            .filter(original_image__user=self.request.user)
        )
