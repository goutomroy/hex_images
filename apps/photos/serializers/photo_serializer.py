from rest_framework import serializers

from apps.photos.models.photo import Photo
from apps.photos.serializers.mixins import PhotoSerializerMixin
from apps.photos.serializers.thumbnail_photo_serializer import ThumbnailPhotoSerializer
from apps.photos.validators import validate_image_extension, validate_image_size


class PhotoCreateSerializer(PhotoSerializerMixin, serializers.ModelSerializer):
    class Meta:
        model = Photo
        fields = ["id", "image"]

    def validate_image(self, value):
        validate_image_extension(value)
        validate_image_size(value)
        return value

    def create(self, validated_data):
        instance = super().create(validated_data)
        instance.create_thumbnails()
        return instance


class PhotoSerializer(PhotoSerializerMixin, serializers.ModelSerializer):
    thumbnails = ThumbnailPhotoSerializer(many=True, read_only=True)

    class Meta:
        model = Photo
        fields = ["id", "image", "thumbnails"]
