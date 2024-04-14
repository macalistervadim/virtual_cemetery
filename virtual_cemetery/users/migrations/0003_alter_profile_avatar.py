# Generated by Django 5.0.3 on 2024-04-14 05:22

import sorl.thumbnail.fields
import users.models
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0002_user_profile_attempts_count_profile_block_date"),
    ]

    operations = [
        migrations.AlterField(
            model_name="profile",
            name="avatar",
            field=sorl.thumbnail.fields.ImageField(
                blank=True,
                help_text="Выберите фотографию профиля",
                null=True,
                upload_to=users.models.item_directory_path,
                verbose_name="фотография профиля",
            ),
        ),
    ]
