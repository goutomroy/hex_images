from django.db import models

from apps.core.models import BaseModel
from apps.photos.models.photo import Photo


class ExpiringLink(BaseModel):
    image = models.ForeignKey(
        Photo, on_delete=models.CASCADE, related_name="expiring_link"
    )
    link = models.CharField(max_length=255, blank=True)
    expired_at = models.DateTimeField(blank=True)

    class Meta:
        ordering = ("-created",)