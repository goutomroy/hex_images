from django.contrib import admin
from django.contrib.admin import ModelAdmin

from apps.photos.models.expiring_link import ExpiringLink
from apps.photos.models.photo import Photo
from apps.photos.models.thumbnail_photo import ThumbnailPhoto
from apps.photos.models.thumbnail_size import ThumbnailSize


@admin.register(ThumbnailSize)
class ThumbnailSizeAdmin(ModelAdmin):
    list_display = ("height",)
    list_filter = ("height",)


@admin.register(Photo)
class PhotoAdmin(ModelAdmin):
    list_display = ("user", "image")
    list_filter = ("user",)


@admin.register(ThumbnailPhoto)
class ThumbnailPhotoAdmin(ModelAdmin):
    list_display = (
        "original_image",
        "thumbnail",
    )
    list_filter = ("original_image",)


@admin.register(ExpiringLink)
class ExpiringLinkAdmin(ModelAdmin):
    list_display = (
        "image",
        "created",
        "expired_at",
        "link",
    )
    list_filter = ("image",)
