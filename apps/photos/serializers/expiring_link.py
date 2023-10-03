import uuid

from django.utils import timezone
from rest_framework import serializers

from apps.photos.models.expiring_link import ExpiringLink
from apps.photos.serializers.mixins import ExpiringLinkEncodeMixin
from hex_images.settings.base import MAX_EXPIRY_LINK_TIME, MIN_EXPIRY_LINK_TIME


class ExpiringLinkSerializer(ExpiringLinkEncodeMixin, serializers.ModelSerializer):
    expiring_time = serializers.IntegerField(
        max_value=MAX_EXPIRY_LINK_TIME, min_value=MIN_EXPIRY_LINK_TIME, write_only=True
    )

    class Meta:
        model = ExpiringLink
        fields = ["id", "image", "link", "expiring_time", "created", "expired_at"]
        read_only_fields = ["link", "expired_at"]

    def create(self, validated_data):
        validated_data["expired_at"] = timezone.now() + timezone.timedelta(
            seconds=validated_data["expiring_time"]
        )
        pk = uuid.uuid4()
        validated_data["id"] = pk
        validated_data["link"] = self._generate_signed_link(pk)
        validated_data = {
            k: v for k, v in validated_data.items() if k != "expiring_time"
        }
        return super().create(validated_data)
