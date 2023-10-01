# Generated by Django 4.2.5 on 2023-10-01 16:27

import uuid

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models

import apps.photos.models.photo
import apps.photos.models.thumbnail_photo


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Photo",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("created", models.DateTimeField(auto_now_add=True)),
                ("updated", models.DateTimeField(auto_now=True)),
                (
                    "image",
                    models.ImageField(
                        max_length=255, upload_to=apps.photos.models.photo.upload_to
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "ordering": ("-created",),
            },
        ),
        migrations.CreateModel(
            name="ThumbnailSize",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("created", models.DateTimeField(auto_now_add=True)),
                ("updated", models.DateTimeField(auto_now=True)),
                ("height", models.IntegerField()),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="ThumbnailPhoto",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("created", models.DateTimeField(auto_now_add=True)),
                ("updated", models.DateTimeField(auto_now=True)),
                (
                    "thumbnail",
                    models.ImageField(
                        max_length=255,
                        upload_to=apps.photos.models.thumbnail_photo.upload_to,
                    ),
                ),
                (
                    "original_image",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="thumbnails",
                        to="photos.photo",
                    ),
                ),
            ],
            options={
                "ordering": ("-created",),
            },
        ),
    ]
