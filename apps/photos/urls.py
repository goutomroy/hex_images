from rest_framework.routers import SimpleRouter

from apps.photos.views.photo import PhotoViewSet
from apps.photos.views.thumbnail_photo import ThumbnailPhotoViewSet

router = SimpleRouter(trailing_slash=False)
router.register("photos", PhotoViewSet)
router.register("thumbnail_photos", ThumbnailPhotoViewSet)


app_name = "photos"
urlpatterns = router.urls
