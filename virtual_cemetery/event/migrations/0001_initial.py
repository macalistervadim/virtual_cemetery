# Generated by Django 5.0.3 on 2024-04-21 13:10

import django.db.models.deletion
import event.models
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Event",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True, primary_key=True, serialize=False, verbose_name="ID"
                    ),
                ),
                ("created_on", models.DateTimeField(auto_now_add=True, verbose_name="создано")),
                ("updated_on", models.DateTimeField(auto_now=True, verbose_name="изменено")),
                (
                    "theme",
                    models.IntegerField(
                        choices=[
                            (1, "Фотоконкурс"),
                            (2, "Литературный"),
                            (3, "Художественный"),
                            (4, "Информационный"),
                            (5, "Образовательный"),
                            (6, "Тематический"),
                        ],
                        help_text="Выберите тему конкурса",
                        verbose_name="тема конкурса",
                    ),
                ),
                (
                    "status",
                    models.IntegerField(
                        choices=[(1, "Стартовал"), (2, "Завершен")],
                        default=1,
                        verbose_name="статус конкурса",
                    ),
                ),
                ("subject", models.CharField(max_length=60, verbose_name="название конкурса")),
                (
                    "body",
                    models.CharField(max_length=150, verbose_name="краткое описание конкурса"),
                ),
                (
                    "prize",
                    models.CharField(
                        help_text="Укажите, какой приз получат победители",
                        max_length=200,
                        verbose_name="приз",
                    ),
                ),
                ("close_date", models.DateField(verbose_name="дата окончания")),
                (
                    "user",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL
                    ),
                ),
                (
                    "winners",
                    models.ManyToManyField(
                        blank=True, related_name="winners_event", to=settings.AUTH_USER_MODEL
                    ),
                ),
            ],
            options={
                "verbose_name": "конкурс",
                "verbose_name_plural": "конкурсы",
                "ordering": ("subject",),
            },
        ),
        migrations.CreateModel(
            name="UserEvent",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True, primary_key=True, serialize=False, verbose_name="ID"
                    ),
                ),
                ("created_on", models.DateTimeField(auto_now_add=True, verbose_name="создано")),
                ("updated_on", models.DateTimeField(auto_now=True, verbose_name="изменено")),
                (
                    "event",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="event.event"
                    ),
                ),
                (
                    "user",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL
                    ),
                ),
            ],
            options={
                "verbose_name": "участник",
                "verbose_name_plural": "участники",
                "ordering": ("event",),
            },
        ),
        migrations.CreateModel(
            name="WorkUser",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True, primary_key=True, serialize=False, verbose_name="ID"
                    ),
                ),
                ("created_on", models.DateTimeField(auto_now_add=True, verbose_name="создано")),
                ("updated_on", models.DateTimeField(auto_now=True, verbose_name="изменено")),
                (
                    "subject",
                    models.CharField(
                        help_text="Введите вашей название работы",
                        max_length=60,
                        verbose_name="название работы",
                    ),
                ),
                (
                    "body",
                    models.TextField(
                        help_text="Укажите краткую предысторию по созданию работы (макс. 500 симв.)",
                        max_length=500,
                        verbose_name="краткая предыстория",
                    ),
                ),
                (
                    "files",
                    models.FileField(
                        help_text="Загрузите вашу работу",
                        upload_to=event.models.item_directory_path,
                        verbose_name="работа",
                    ),
                ),
                (
                    "event",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="event.event"
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="event.userevent"
                    ),
                ),
            ],
            options={
                "verbose_name": "работа участника конкурса",
                "verbose_name_plural": "работы участников конкурсов",
                "ordering": ("subject",),
                "unique_together": {("user", "event")},
            },
        ),
        migrations.CreateModel(
            name="VoteEvent",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True, primary_key=True, serialize=False, verbose_name="ID"
                    ),
                ),
                ("created_on", models.DateTimeField(auto_now_add=True, verbose_name="создано")),
                ("updated_on", models.DateTimeField(auto_now=True, verbose_name="изменено")),
                (
                    "score",
                    models.IntegerField(
                        choices=[
                            (1, "Ужасно"),
                            (2, "Неплохо"),
                            (3, "Хорошо"),
                            (4, "Информационный"),
                            (5, "Восхитительно"),
                        ],
                        help_text="Выберите подходящую оценку для работы",
                        verbose_name="оценка работы",
                    ),
                ),
                (
                    "user",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL
                    ),
                ),
                (
                    "work",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="event.workuser"
                    ),
                ),
            ],
            options={
                "verbose_name": "оценка работы",
                "verbose_name_plural": "оценки работ",
                "ordering": ("work",),
            },
        ),
    ]
