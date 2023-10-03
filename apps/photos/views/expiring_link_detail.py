import mimetypes

from django.http import FileResponse
from django.utils import timezone
from rest_framework import mixins
from rest_framework.generics import get_object_or_404
from rest_framework.viewsets import GenericViewSet

from apps.photos.models.expiring_link import ExpiringLink
from apps.photos.serializers.mixins import ExpiringLinkDecodeMixin


class ExpiringLinkDetailView(
    ExpiringLinkDecodeMixin, mixins.RetrieveModelMixin, GenericViewSet
):
    queryset = ExpiringLink.objects.all()

    def get_queryset(self):
        return (
            super()
            .get_queryset()
            .prefetch_related("image__user")
            .filter(
                image__user=self.request.user,
                expired_at__gt=timezone.now(),
            )
        )

    def get_object(self):
        signed_link = self.kwargs.get("signed_link")
        expiring_link_id = self._decode_signed_link(signed_link)
        expiring_link = get_object_or_404(self.queryset, pk=expiring_link_id)
        return expiring_link

    def retrieve(self, request, *args, **kwargs):
        image = self.get_object().image.image
        content_type, encoding = mimetypes.guess_type(image.name)
        response = FileResponse(
            image,
            content_type=content_type,
            as_attachment=True,
            filename=image.name.split("/")[-1],
        )
        return response
