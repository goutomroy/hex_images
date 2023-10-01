from django.conf import settings
from rest_framework.exceptions import ValidationError


def validate_image_extension(value):
    valid_formats = ["png", "jpg"]
    if not any([True if value.name.endswith(i) else False for i in valid_formats]):
        raise ValidationError(f"{value.name} is not a valid image format.")


def validate_image_size(value):
    if value.size > settings.MAX_UPLOAD_SIZE:
        raise ValidationError(
            f"File size exceeds the limit. Max {settings.MAX_UPLOAD_SIZE / (1024 * 1024)} MB is allowed."  # noqa
        )
