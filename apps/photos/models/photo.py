import os

from django.contrib.auth.models import User
from django.db import models

from apps.accounts.models.profile import Profile
from apps.core.models import BaseModel
from apps.workers.photos import generate_thumbnails


def upload_to(instance, filename):
    split_tuple = os.path.splitext(filename)
    new_filename = str(instance.id) + split_tuple[1]
    return "/".join(["images", instance.user.username, new_filename])


class Photo(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(
        upload_to=upload_to,
        max_length=255,
    )

    class Meta:
        ordering = ("-created",)

    def create_thumbnails(self) -> None:
        profile = Profile.objects.get(user=self.user.id)

        sizes = [
            thumbnail_size.height
            for thumbnail_size in profile.account_tier.thumbnail_sizes.all()
        ]
        generate_thumbnails.delay(str(self.id), sizes)
