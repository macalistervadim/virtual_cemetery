# Generated by Django 5.0.3 on 2024-04-20 14:18

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("event", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="event",
            name="close_date",
            field=models.DateField(
                default=django.utils.timezone.now, verbose_name="дата окончания"
            ),
            preserve_default=False,
        ),
    ]
