import uuid

from django.core import signing
from rest_framework.exceptions import ValidationError
from rest_framework.reverse import reverse


class PhotoSerializerMixin:
    def get_extra_kwargs(self):
        kwargs = super().get_extra_kwargs()
        if not self.context[
            "request"
        ].user.profile.account_tier.presence_of_original_image:
            kwargs["image"] = {"write_only": True}
        return kwargs


class ExpiringLinkEncodeMixin:
    def _generate_signed_link(self, pk: uuid):
        signed_link = signing.dumps(str(pk))
        full_url = reverse(
            "photos:expiring-link-detail",
            kwargs={"signed_link": signed_link},
            request=self.context["request"],
        )
        return full_url


class ExpiringLinkDecodeMixin:
    def _decode_signed_link(self, signed_link):
        try:
            return signing.loads(signed_link)
        except signing.BadSignature:
            raise ValidationError("Invalid signed link")
