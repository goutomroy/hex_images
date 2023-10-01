import os

from django.db import models

from apps.core.models import BaseModel
from apps.photos.models.photo import Photo


def upload_to(instance, filename):
    split_tuple = os.path.splitext(filename)
    new_filename = f"{instance.id}_{instance.thumbnail.height}_{instance.thumbnail.width}{split_tuple[1]}"  # noqa
    return "/".join(
        [
            "images",
            instance.original_image.user.username,
            "thumbnails",
            new_filename,
        ]
    )


class ThumbnailPhoto(BaseModel):
    original_image = models.ForeignKey(
        Photo, related_name="thumbnails", on_delete=models.CASCADE
    )
    thumbnail = models.ImageField(
        upload_to=upload_to,
        max_length=255,
    )

    class Meta:
        ordering = ("-created",)
