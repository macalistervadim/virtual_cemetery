import pathlib
import uuid

import django.contrib.auth
import django.core.validators
import django.db
import django.forms
import django.utils.translation as translation

import feedback.managers


def item_directory_path(instance, filename):
    ext = filename.split(".")[-1]
    filename = f"{uuid.uuid4()}.{ext}"
    feedback_id = str(instance.feedback_id)
    return pathlib.Path("feedback") / feedback_id / filename


class Feedback(django.db.models.Model):
    objects = feedback.managers.FeedbackManager()

    class _FeedbackTheme(django.db.models.IntegerChoices):
        ACCOUNT = 1, translation.gettext_lazy("Учетная запись")
        TECHNICAL_PROBLEMS = 2, translation.gettext_lazy("Технические проблемы")
        SUGGESTIONS = 3, translation.gettext_lazy("Отзывы и предложения")

    user = django.db.models.OneToOneField(
        django.contrib.auth.models.User,
        on_delete=django.db.models.CASCADE,
    )
    theme = django.db.models.IntegerField(
        translation.gettext_lazy("тема обращения"),
        choices=_FeedbackTheme.choices,
        help_text=translation.gettext_lazy("Выберите тему обращения"),
    )
    text = django.db.models.TextField(
        translation.gettext_lazy("текст обращения"),
    )
    created_on = django.db.models.DateField(
        translation.gettext_lazy("создано"),
        auto_now_add=True,
        editable=False,
    )

    class Meta:
        ordering = ("theme",)
        verbose_name = translation.gettext_lazy("обратная связь")
        verbose_name_plural = translation.gettext_lazy("обратные связи")


class FeedbackFiles(django.db.models.Model):
    feedback = django.db.models.ForeignKey(
        Feedback,
        on_delete=django.db.models.CASCADE,
    )
    files = django.db.models.FileField(
        translation.gettext_lazy("дополнительные файлы"),
        null=True,
        blank=True,
        upload_to=item_directory_path,
    )
