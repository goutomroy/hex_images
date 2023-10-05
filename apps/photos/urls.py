from django.urls import path
from rest_framework.routers import SimpleRouter

from apps.photos.views.expiring_link import ExpiringLinkViewSet
from apps.photos.views.expiring_link_detail import ExpiringLinkDetailView
from apps.photos.views.photo import PhotoViewSet
from apps.photos.views.thumbnail_photo import ThumbnailPhotoViewSet

router = SimpleRouter(trailing_slash=False)
router.register("photos", PhotoViewSet)
router.register("thumbnail_photos", ThumbnailPhotoViewSet)
router.register("expiring_links", ExpiringLinkViewSet)

app_name = "photos"

urlpatterns = [
    *router.urls,
    path(
        "expiring_link_view/<str:signed_link>/",
        ExpiringLinkDetailView.as_view({"get": "retrieve"}),
        name="expiring-link-detail",
    ),
]
