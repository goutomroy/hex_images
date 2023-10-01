from django.contrib import admin
from django.contrib.admin import ModelAdmin

from apps.accounts.models.account_tier import AccountTier
from apps.accounts.models.profile import Profile


@admin.register(Profile)
class ProfileAdmin(ModelAdmin):
    list_display = ("user", "account_tier")
    list_filter = ("account_tier",)


@admin.register(AccountTier)
class AccountTierAdmin(ModelAdmin):
    list_display = (
        "name",
        "can_generate_expiring_links",
        "presence_of_original_image",
    )
    list_filter = ("name", "can_generate_expiring_links", "presence_of_original_image")
