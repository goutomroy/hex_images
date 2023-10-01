from rest_framework import serializers

from apps.photos.models.thumbnail_photo import ThumbnailPhoto


class ThumbnailPhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ThumbnailPhoto
        fields = ["id", "thumbnail"]

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data["height"] = instance.thumbnail.height
        data["width"] = instance.thumbnail.width
        return data
