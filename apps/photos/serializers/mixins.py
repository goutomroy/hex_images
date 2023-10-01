class PhotoSerializerMixin:
    def get_extra_kwargs(self):
        kwargs = super().get_extra_kwargs()
        if not self.context[
            "request"
        ].user.profile.account_tier.presence_of_original_image:
            kwargs["image"] = {"write_only": True}
        return kwargs
