from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
from model_bakery import baker

from apps.accounts.models.account_tier import AccountTier
from apps.accounts.models.profile import Profile
from apps.photos.models.thumbnail_size import ThumbnailSize


class Command(BaseCommand):
    help = "Create test users(basic, premium, enterprise) for showing demo"

    def handle(self, *args, **kwargs):
        self._create_thumbnail_sizes()
        self._create_basic_user()
        self._create_premium_user()
        self._create_enterprise_user()

    def _create_basic_user(self):
        if not User.objects.filter(username="hex_basic").exists():
            self._user_basic = User.objects.create_user(
                username="hex_basic",
                email="hex_basic@x.com",
                is_superuser=True,
                is_staff=True,
                password="hex_basic_2023",
            )

            self._account_tier_basic = baker.make(
                AccountTier,
                name="Basic",
                thumbnail_sizes=[self._thumbnail_200],
            )
            baker.make(
                Profile, user=self._user_basic, account_tier=self._account_tier_basic
            )

    def _create_premium_user(self):
        if not User.objects.filter(username="hex_premium").exists():
            self._user_premium = User.objects.create_user(
                username="hex_premium",
                email="hex_premium@x.com",
                is_superuser=True,
                is_staff=True,
                password="hex_premium_2023",
            )

            self._account_tier_premium = baker.make(
                AccountTier,
                name="Premium",
                thumbnail_sizes=[self._thumbnail_200, self._thumbnail_400],
                can_generate_expiring_links=False,
                presence_of_original_image=True,
            )
            baker.make(
                Profile,
                user=self._user_premium,
                account_tier=self._account_tier_premium,
            )

    def _create_enterprise_user(self):
        if not User.objects.filter(username="hex_enterprise").exists():
            self._user_enterprise = User.objects.create_user(
                username="hex_enterprise",
                email="hex_enterprise@x.com",
                is_superuser=True,
                is_staff=True,
                password="hex_enterprise_2023",
            )
            self._account_tier_premium = baker.make(
                AccountTier,
                name="Enterprise",
                thumbnail_sizes=[self._thumbnail_200, self._thumbnail_400],
                can_generate_expiring_links=True,
                presence_of_original_image=True,
            )
            baker.make(
                Profile,
                user=self._user_enterprise,
                account_tier=self._account_tier_premium,
            )

    def _create_thumbnail_sizes(self):
        self._thumbnail_200 = baker.make(ThumbnailSize, height=200)
        self._thumbnail_400 = baker.make(ThumbnailSize, height=400)
