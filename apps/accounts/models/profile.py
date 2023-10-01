from django.contrib.auth.models import User
from django.db import models

from apps.core.models import BaseModel


class Profile(BaseModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    account_tier = models.ForeignKey(
        "accounts.AccountTier",
        on_delete=models.SET_NULL,
        null=True,
        related_name="users",
    )
