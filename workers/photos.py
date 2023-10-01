import os
import uuid
from io import BytesIO
from typing import List

from celery import shared_task
from django.core.files.uploadedfile import SimpleUploadedFile
from PIL import Image as PilImage


@shared_task
def create_thumbnails(original_image_id: uuid, desired_sizes: List[int]):
    from apps.photos.models.photo import Photo
    from apps.photos.models.thumbnail_photo import ThumbnailPhoto

    original_photo = Photo.objects.get(id=original_image_id)
    filename, ext = os.path.splitext(os.path.basename(original_photo.image.name))
    image_name = original_photo.image.name.split("/")[-1]
    for size in desired_sizes:
        img_file = BytesIO(original_photo.image.read())
        original_image = PilImage.open(img_file)
        desired_height = size
        desired_width = int(
            desired_height * (original_photo.image.width / original_photo.image.height)
        )
        thumbnail = original_image.resize((desired_width, desired_height))

        # Save the resized image to the path
        thumb_io = BytesIO()
        thumbnail.save(thumb_io, format="JPEG" if ext.lower() == ".jpg" else "PNG")
        thumbnail_file = SimpleUploadedFile(
            image_name,
            thumb_io.getvalue(),
            content_type="image/jpeg" if ext.lower() == ".jpg" else "image/png",
        )

        ThumbnailPhoto.objects.create(
            original_image=original_photo, thumbnail=thumbnail_file
        )
