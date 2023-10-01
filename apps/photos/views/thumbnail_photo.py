from rest_framework import permissions, viewsets

from apps.photos.models.thumbnail_photo import ThumbnailPhoto
from apps.photos.serializers.thumbnail_photo_serializer import ThumbnailPhotoSerializer


class ThumbnailPhotoViewSet(viewsets.ModelViewSet):
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
