from django.db import models

from apps.core.models import BaseModel


class ThumbnailSize(BaseModel):
    height = models.IntegerField()
