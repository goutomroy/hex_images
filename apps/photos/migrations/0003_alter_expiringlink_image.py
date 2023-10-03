# Generated by Django 4.2.5 on 2023-10-03 15:28

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("photos", "0002_expiringlink"),
    ]

    operations = [
        migrations.AlterField(
            model_name="expiringlink",
            name="image",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="expiring_link",
                to="photos.photo",
            ),
        ),
    ]
