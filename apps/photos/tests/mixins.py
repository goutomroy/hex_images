import tempfile
from contextlib import contextmanager

from django.contrib.auth.models import User
from django.core.cache import cache
from model_bakery import baker
from PIL import Image
from rest_framework.test import APIClient

from apps.accounts.models.account_tier import AccountTier
from apps.accounts.models.profile import Profile
from apps.photos.models.thumbnail_size import ThumbnailSize


class TestCaseMixin:
    def setUp(self) -> None:
        self._create_basic_user()
        self._create_premium_user()
        self._create_enterprise_user()
        cache.clear()

    def tearDown(self):
        cache.clear()

    def _create_basic_user(self):
        self._user_basic = baker.make(User)
        self._client_user_basic = APIClient()
        self._client_user_basic.force_authenticate(self._user_basic)

        self._account_tier_basic = baker.make(
            AccountTier,
            thumbnail_sizes=[self._get_thumbnail_size(200)],
        )
        self._profile_basic = baker.make(
            Profile, user=self._user_basic, account_tier=self._account_tier_basic
        )

    def _create_premium_user(self):
        self._user_premium = baker.make(User)
        self._client_user_premium = APIClient()
        self._client_user_premium.force_authenticate(self._user_premium)

        self._account_tier_premium = baker.make(
            AccountTier,
            thumbnail_sizes=[
                self._get_thumbnail_size(200),
                self._get_thumbnail_size(400),
            ],
            can_generate_expiring_links=False,
            presence_of_original_image=True,
        )
        self._profile_premium = baker.make(
            Profile, user=self._user_premium, account_tier=self._account_tier_premium
        )

    def _create_enterprise_user(self):
        self._user_enterprise = baker.make(User)
        self._client_user_enterprise = APIClient()
        self._client_user_enterprise.force_authenticate(self._user_enterprise)

        self._account_tier_premium = baker.make(
            AccountTier,
            thumbnail_sizes=[
                self._get_thumbnail_size(200),
                self._get_thumbnail_size(400),
            ],
            can_generate_expiring_links=True,
            presence_of_original_image=True,
        )
        self._profile_enterprise = baker.make(
            Profile, user=self._user_enterprise, account_tier=self._account_tier_premium
        )

    def _get_thumbnail_size(self, height):
        return baker.make(ThumbnailSize, height=height)

    @contextmanager
    def _generate_image_file(self, suffix=".jpg", height=100, width=100):
        with tempfile.NamedTemporaryFile(suffix=suffix) as tmp_file:
            image = Image.new("RGB", size=(width, height), color=(153, 153, 255))
            image.save(tmp_file, "jpeg")
            tmp_file.seek(0)
            yield tmp_file
