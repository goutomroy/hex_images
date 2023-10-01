from django.db import models

from apps.core.models import BaseModel
from apps.photos.models.thumbnail_size import ThumbnailSize


class AccountTier(BaseModel):
    name = models.CharField(max_length=100)
    thumbnail_sizes = models.ManyToManyField(ThumbnailSize, blank=True)
    can_generate_expiring_links = models.BooleanField(default=False)
    presence_of_original_image = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    @property
    def get_thumbnail_sizes(self):
        return self.thumbnail_sizes.all()
