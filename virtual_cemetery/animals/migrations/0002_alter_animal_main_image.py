# Generated by Django 5.0.3 on 2024-04-15 16:06

import animals.models
import sorl.thumbnail.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("animals", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="animal",
            name="main_image",
            field=sorl.thumbnail.fields.ImageField(
                blank=True,
                help_text="Загрузите изображение вашего питомца",
                null=True,
                upload_to=animals.models.item_directory_path,
                verbose_name="Изображение питомца",
            ),
        ),
    ]
