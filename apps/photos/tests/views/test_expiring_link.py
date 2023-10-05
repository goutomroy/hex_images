import shutil
from pathlib import Path

from django.utils import timezone
from model_bakery import baker
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

from apps.photos.models.expiring_link import ExpiringLink
from apps.photos.models.photo import Photo
from apps.photos.models.thumbnail_photo import ThumbnailPhoto
from apps.photos.tests.mixins import TestCaseMixin


class ExpiringLinkTestCase(TestCaseMixin, APITestCase):
    EXPIRING_LINK_LIST_PATH = reverse("photos:expiringlink-list")

    def test_expiring_link_view_is_not_allowed_for_basic_user(self):
        response = self._client_user_basic.get(self.EXPIRING_LINK_LIST_PATH)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        response = self._client_user_basic.put(self.EXPIRING_LINK_LIST_PATH, {})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        response = self._client_user_basic.patch(self.EXPIRING_LINK_LIST_PATH, {})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        response = self._client_user_basic.post(self.EXPIRING_LINK_LIST_PATH, {})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        response = self._client_user_basic.delete(self.EXPIRING_LINK_LIST_PATH)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_expiring_link_view_is_not_allowed_for_premium_user(self):
        response = self._client_user_premium.get(self.EXPIRING_LINK_LIST_PATH)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        response = self._client_user_premium.put(self.EXPIRING_LINK_LIST_PATH, {})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        response = self._client_user_premium.patch(self.EXPIRING_LINK_LIST_PATH, {})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        response = self._client_user_premium.post(self.EXPIRING_LINK_LIST_PATH, {})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        response = self._client_user_premium.delete(self.EXPIRING_LINK_LIST_PATH)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_put_is_not_allowed(self):
        response = self._client_user_enterprise.put(self.EXPIRING_LINK_LIST_PATH, {})
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_patch_is_not_allowed(self):
        response = self._client_user_enterprise.patch(self.EXPIRING_LINK_LIST_PATH, {})
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_expiring_link_create_success(self):
        photo = baker.make(Photo, user=self._user_enterprise, _create_files=True)
        baker.make(
            ThumbnailPhoto, original_image=photo, _create_files=True, _quantity=2
        )
        response = self._client_user_enterprise.post(
            self.EXPIRING_LINK_LIST_PATH, {"image": photo.id, "expiring_time": 400}
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["image"], photo.id)

        shutil.rmtree(Path(photo.image.path).parent)

    def test_expiring_link_list_success(self):
        photo = baker.make(Photo, user=self._user_enterprise, _create_files=True)
        baker.make(
            ThumbnailPhoto, original_image=photo, _create_files=True, _quantity=2
        )
        baker.make(
            ExpiringLink,
            image=photo,
            expired_at=timezone.now() + timezone.timedelta(seconds=400),
        )
        response = self._client_user_enterprise.get(self.EXPIRING_LINK_LIST_PATH)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 1)
        self.assertEqual(response.data["results"][0]["image"], photo.id)

        shutil.rmtree(Path(photo.image.path).parent)

    def test_expiring_link_retrieve_success(self):
        photo = baker.make(Photo, user=self._user_enterprise, _create_files=True)
        baker.make(
            ThumbnailPhoto, original_image=photo, _create_files=True, _quantity=2
        )
        expiring_link = baker.make(
            ExpiringLink,
            image=photo,
            expired_at=timezone.now() + timezone.timedelta(seconds=400),
        )
        response = self._client_user_enterprise.get(
            reverse("photos:expiringlink-detail", kwargs={"pk": expiring_link.id})
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["id"], str(expiring_link.id))

        shutil.rmtree(Path(photo.image.path).parent)

    def test_expiring_link_delete_success(self):
        photo = baker.make(Photo, user=self._user_enterprise, _create_files=True)
        baker.make(
            ThumbnailPhoto, original_image=photo, _create_files=True, _quantity=2
        )
        expiring_link = baker.make(
            ExpiringLink,
            image=photo,
            expired_at=timezone.now() + timezone.timedelta(seconds=400),
        )
        response = self._client_user_enterprise.delete(
            reverse("photos:expiringlink-detail", kwargs={"pk": expiring_link.id})
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        shutil.rmtree(Path(photo.image.path).parent)

    def test_expired_link_cannot_be_retrieve(self):
        photo = baker.make(Photo, user=self._user_enterprise, _create_files=True)
        baker.make(
            ThumbnailPhoto, original_image=photo, _create_files=True, _quantity=2
        )
        expiring_link = baker.make(
            ExpiringLink,
            image=photo,
            expired_at=timezone.now() - timezone.timedelta(seconds=400),
        )
        response = self._client_user_enterprise.get(
            reverse("photos:expiringlink-detail", kwargs={"pk": expiring_link.id})
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        shutil.rmtree(Path(photo.image.path).parent)
