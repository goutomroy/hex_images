from django.db import models

from apps.core.models import BaseModel


class ThumbnailSize(BaseModel):
    height = models.IntegerField()

    def __str__(self):
        return f"height : {self.height}"
