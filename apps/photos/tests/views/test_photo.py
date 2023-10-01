import os
import shutil
import tempfile
import unittest
from contextlib import contextmanager
from pathlib import Path
from unittest.mock import patch, MagicMock

from django.conf import settings
from django.contrib.auth.models import User
from model_bakery import baker
from PIL import Image
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APIClient, APITestCase

from apps.accounts.models.account_tier import AccountTier
from apps.accounts.models.profile import Profile
from apps.photos.models.photo import Photo
from apps.photos.models.thumbnail_size import ThumbnailSize



class PhotoAPITestCase(APITestCase):
    PHOTOS_LIST_PATH = reverse("photos:photo-list")

    def setUp(self) -> None:
        self._create_basic_user()
        self._create_premium_user()
        self._create_enterprise_user()

    def test_put_is_not_allowed(self):
        response = self._client_user_basic.put(
            self.PHOTOS_LIST_PATH, {}, format="multipart"
        )
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_patch_is_not_allowed(self):
        response = self._client_user_basic.patch(
            self.PHOTOS_LIST_PATH, {}, format="multipart"
        )
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    @unittest.skip("Work in progress")
    @patch("apps.photos.models.photo.create_thumbnails.delay")
    def test_photo_create_success(self, _create_thumbnails: MagicMock):
        with self._generate_image_file() as image_file:
            try:
                data = {"image": image_file}
                response = self._client_user_basic.post(
                    self.PHOTOS_LIST_PATH, data, format="multipart"
                )
                self.assertEqual(response.status_code, status.HTTP_201_CREATED)
                # _create_thumbnails.delay.assert_called_with(response.data["id"], [200,])
                _create_thumbnails.delay.delay.assert_called_once()
            finally:
                photo = Photo.objects.get(id=response.data["id"])
                shutil.rmtree(Path(photo.image.path).parent)

    def test_photo_not_valid_format(self):
        with self._generate_image_file(suffix=".jpeg") as image_file:
            data = {"image": image_file}
            response = self._client_user_basic.post(
                self.PHOTOS_LIST_PATH, data, format="multipart"
            )
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
            self.assertIn("is not a valid image format", response.data["image"][0])

    def test_photo_size_exceed(self):
        photo_path = os.path.join(settings.MEDIA_ROOT, 'big_test_image.jpg')
        with open(photo_path, 'rb') as photo_data:
            data = {"image": photo_data}
            response = self._client_user_basic.post(
                self.PHOTOS_LIST_PATH, data, format="multipart"
            )
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
            self.assertIn("File size exceeds the limit", response.data["image"][0])

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
            image = Image.new("RGB", size=(width, height), color = (153, 153, 255))
            image.save(tmp_file, "jpeg")
            tmp_file.seek(0)
            yield tmp_file
