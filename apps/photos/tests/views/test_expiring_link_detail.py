import shutil
import uuid
from pathlib import Path

from django.conf import settings
from model_bakery import baker
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

from apps.photos.models.photo import Photo
from apps.photos.models.thumbnail_photo import ThumbnailPhoto
from apps.photos.tests.mixins import TestCaseMixin


class ExpiringLinkDetailTestCase(TestCaseMixin, APITestCase):
    EXPIRING_LINK_LIST_PATH = reverse("photos:expiringlink-list")
    EXPIRING_LINK_DETAIL_PATH = reverse(
        "photos:expiring-link-detail", kwargs={"signed_link": uuid.uuid4()}
    )

    def test_expiring_link_detail_view_is_not_allowed_for_basic_user(self):
        response = self._client_user_basic.get(self.EXPIRING_LINK_DETAIL_PATH)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        response = self._client_user_basic.put(self.EXPIRING_LINK_DETAIL_PATH, {})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        response = self._client_user_basic.patch(self.EXPIRING_LINK_DETAIL_PATH, {})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        response = self._client_user_basic.post(self.EXPIRING_LINK_DETAIL_PATH, {})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        response = self._client_user_basic.delete(self.EXPIRING_LINK_DETAIL_PATH)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_expiring_link_detail_view_is_not_allowed_for_premium_user(self):
        response = self._client_user_premium.get(self.EXPIRING_LINK_DETAIL_PATH)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        response = self._client_user_premium.put(self.EXPIRING_LINK_DETAIL_PATH, {})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        response = self._client_user_premium.patch(self.EXPIRING_LINK_DETAIL_PATH, {})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        response = self._client_user_premium.post(self.EXPIRING_LINK_DETAIL_PATH, {})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        response = self._client_user_premium.delete(self.EXPIRING_LINK_DETAIL_PATH)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_post_is_not_allowed(self):
        response = self._client_user_enterprise.post(self.EXPIRING_LINK_DETAIL_PATH, {})
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_put_is_not_allowed(self):
        response = self._client_user_enterprise.put(self.EXPIRING_LINK_DETAIL_PATH, {})
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_patch_is_not_allowed(self):
        response = self._client_user_enterprise.patch(
            self.EXPIRING_LINK_DETAIL_PATH, {}
        )
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_delete_is_not_allowed(self):
        response = self._client_user_enterprise.delete(
            self.EXPIRING_LINK_DETAIL_PATH, {}
        )
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_retrieve_success(self):
        photo = baker.make(Photo, user=self._user_enterprise, _create_files=True)
        baker.make(
            ThumbnailPhoto, original_image=photo, _create_files=True, _quantity=2
        )
        response = self._client_user_enterprise.post(
            self.EXPIRING_LINK_LIST_PATH, {"image": photo.id, "expiring_time": 400}
        )
        response = self._client_user_enterprise.get(response.data["link"])
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        shutil.rmtree(Path(photo.image.path).parent)

    def test_throttle_retrieve_success(self):
        photo = baker.make(Photo, user=self._user_enterprise, _create_files=True)
        baker.make(
            ThumbnailPhoto, original_image=photo, _create_files=True, _quantity=2
        )
        post_response = self._client_user_enterprise.post(
            self.EXPIRING_LINK_LIST_PATH, {"image": photo.id, "expiring_time": 400}
        )
        for _ in range(settings.THROTTLE_THRESHOLD-1):
            response = self._client_user_enterprise.get(post_response.data["link"])
            self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = self._client_user_enterprise.get(post_response.data["link"])
        self.assertEqual(response.status_code, status.HTTP_429_TOO_MANY_REQUESTS)

        shutil.rmtree(Path(photo.image.path).parent)
