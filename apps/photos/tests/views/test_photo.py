import os
import shutil
from pathlib import Path
from unittest.mock import patch

from django.conf import settings
from model_bakery import baker
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

from apps.photos.models.photo import Photo
from apps.photos.models.thumbnail_photo import ThumbnailPhoto
from apps.photos.tests.mixins import TestCaseMixin


class PhotoAPITestCase(TestCaseMixin, APITestCase):
    PHOTOS_LIST_PATH = reverse("photos:photo-list")

    def test_put_is_not_allowed(self):
        response = self._client_user_basic.put(
            self.PHOTOS_LIST_PATH,
            {},
        )
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_patch_is_not_allowed(self):
        response = self._client_user_basic.patch(
            self.PHOTOS_LIST_PATH,
            {},
        )
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    @patch("apps.photos.models.photo.generate_thumbnails.delay")
    def test_photo_multi_part_create_success(self, _generate_thumbnails):
        with self._generate_image_file() as image_file:
            try:
                data = {"image": image_file}
                response = self._client_user_basic.post(
                    self.PHOTOS_LIST_PATH, data, format="multipart"
                )
                self.assertEqual(response.status_code, status.HTTP_201_CREATED)
                _generate_thumbnails.assert_called_once_with(
                    response.data["id"],
                    [
                        200,
                    ],
                )

            finally:
                photo = Photo.objects.get(id=response.data["id"])
                shutil.rmtree(Path(photo.image.path).parent)

    def test_photo_list_success(self):
        photo = baker.make(Photo, user=self._user_basic, _create_files=True)
        baker.make(
            ThumbnailPhoto, original_image=photo, _create_files=True, _quantity=1
        )
        response = self._client_user_basic.get(self.PHOTOS_LIST_PATH)

        self.assertEqual(len(response.data["results"]), 1)
        self.assertTrue("image" not in response.data["results"][0])
        self.assertEqual(len(response.data["results"][0]["thumbnails"]), 1)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        shutil.rmtree(Path(photo.image.path).parent)

    def test_photo_retrieve_success(self):
        photo = baker.make(Photo, user=self._user_basic, _create_files=True)
        baker.make(
            ThumbnailPhoto, original_image=photo, _create_files=True, _quantity=1
        )
        path = reverse("photos:photo-detail", kwargs={"pk": photo.id})

        response = self._client_user_basic.get(path)

        self.assertTrue("image" not in response.data)
        self.assertEqual(len(response.data["thumbnails"]), 1)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        shutil.rmtree(Path(photo.image.path).parent)

    def test_photo_destroy_success(self):
        photo = baker.make(Photo, user=self._user_basic, _create_files=True)
        baker.make(
            ThumbnailPhoto, original_image=photo, _create_files=True, _quantity=1
        )
        path = reverse("photos:photo-detail", kwargs={"pk": photo.id})

        prev_photo_count = Photo.objects.filter(user=self._user_basic).count()
        prev_thumbnail_photo_count = ThumbnailPhoto.objects.filter(
            original_image__user=self._user_basic
        ).count()

        response = self._client_user_basic.delete(path)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        now_photo_count = Photo.objects.filter(user=self._user_basic).count()
        now_thumbnail_photo_count = ThumbnailPhoto.objects.filter(
            original_image__user=self._user_basic
        ).count()

        self.assertEqual(prev_photo_count - 1, now_photo_count)
        self.assertEqual(prev_thumbnail_photo_count - 1, now_thumbnail_photo_count)

        shutil.rmtree(Path(photo.image.path).parent)

    def test_photo_list_success_premium_user(self):
        photo = baker.make(Photo, user=self._user_premium, _create_files=True)
        baker.make(
            ThumbnailPhoto, original_image=photo, _create_files=True, _quantity=2
        )
        response = self._client_user_premium.get(self.PHOTOS_LIST_PATH)

        self.assertEqual(len(response.data["results"]), 1)
        self.assertTrue("image" in response.data["results"][0])
        self.assertEqual(len(response.data["results"][0]["thumbnails"]), 2)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        shutil.rmtree(Path(photo.image.path).parent)

    def test_photo_retrieve_success_premium_user(self):
        photo = baker.make(Photo, user=self._user_premium, _create_files=True)
        baker.make(
            ThumbnailPhoto, original_image=photo, _create_files=True, _quantity=2
        )
        path = reverse("photos:photo-detail", kwargs={"pk": photo.id})

        response = self._client_user_premium.get(path)

        self.assertTrue("image" in response.data)
        self.assertEqual(len(response.data["thumbnails"]), 2)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        shutil.rmtree(Path(photo.image.path).parent)

    def test_photo_list_success_enterprise_user(self):
        photo = baker.make(Photo, user=self._user_enterprise, _create_files=True)
        baker.make(
            ThumbnailPhoto, original_image=photo, _create_files=True, _quantity=2
        )
        response = self._client_user_enterprise.get(self.PHOTOS_LIST_PATH)

        self.assertEqual(len(response.data["results"]), 1)
        self.assertTrue("image" in response.data["results"][0])
        self.assertEqual(len(response.data["results"][0]["thumbnails"]), 2)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        shutil.rmtree(Path(photo.image.path).parent)

    def test_photo_retrieve_success_enterprise_user(self):
        photo = baker.make(Photo, user=self._user_enterprise, _create_files=True)
        baker.make(
            ThumbnailPhoto, original_image=photo, _create_files=True, _quantity=2
        )
        path = reverse("photos:photo-detail", kwargs={"pk": photo.id})

        response = self._client_user_enterprise.get(path)

        self.assertTrue("image" in response.data)
        self.assertEqual(len(response.data["thumbnails"]), 2)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        shutil.rmtree(Path(photo.image.path).parent)

    def test_photo_is_not_valid_format_when_creating(self):
        with self._generate_image_file(suffix=".jpeg") as image_file:
            data = {"image": image_file}
            response = self._client_user_basic.post(
                self.PHOTOS_LIST_PATH, data, format="multipart"
            )
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
            self.assertIn("is not a valid image format", response.data["image"][0])

    def test_photo_size_exceed_when_creating(self):
        photo_path = os.path.join(
            settings.BASE_DIR, "test_images", "big_test_image.jpg"
        )
        with open(photo_path, "rb") as photo_data:
            data = {"image": photo_data}
            response = self._client_user_basic.post(
                self.PHOTOS_LIST_PATH, data, format="multipart"
            )
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
            self.assertIn("File size exceeds the limit", response.data["image"][0])

    @patch("apps.photos.models.photo.generate_thumbnails.delay")
    def test_create_multi_part_throttle_success(self, _generate_thumbnails):
        for _ in range(settings.PHOTO_CREATE_THROTTLE_THRESHOLD):
            with self._generate_image_file() as image_file:
                data = {"image": image_file}
                response = self._client_user_basic.post(
                    self.PHOTOS_LIST_PATH, data, format="multipart"
                )

                photo = Photo.objects.get(id=response.data["id"])
                shutil.rmtree(Path(photo.image.path).parent)

        with self._generate_image_file() as image_file:
            data = {"image": image_file}
            response = self._client_user_basic.post(
                self.PHOTOS_LIST_PATH, data, format="multipart"
            )
            self.assertEqual(response.status_code, status.HTTP_429_TOO_MANY_REQUESTS)

    def test_list_throttle_success(self):
        for _ in range(settings.THROTTLE_THRESHOLD):
            self._client_user_basic.get(
                self.PHOTOS_LIST_PATH,
            )
        response = self._client_user_basic.get(
            self.PHOTOS_LIST_PATH,
        )
        self.assertEqual(response.status_code, status.HTTP_429_TOO_MANY_REQUESTS)

    def test_retrieve_throttle_success(self):
        photo = baker.make(Photo, user=self._user_basic, _create_files=True)
        path = reverse("photos:photo-detail", kwargs={"pk": photo.id})
        for _ in range(settings.THROTTLE_THRESHOLD):
            self._client_user_basic.get(path)

        response = self._client_user_basic.get(path)
        self.assertEqual(response.status_code, status.HTTP_429_TOO_MANY_REQUESTS)

        shutil.rmtree(Path(photo.image.path).parent)
