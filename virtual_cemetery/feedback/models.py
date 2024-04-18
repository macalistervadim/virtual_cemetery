import pathlib
import uuid

import django.contrib.auth
import django.core.validators
import django.db
import django.forms
import django.utils.translation as translation

import core.models
import feedback.managers


def item_directory_path(instance, filename):
    ext = filename.split(".")[-1]
    filename = f"{uuid.uuid4()}.{ext}"
    feedback_id = str(instance.feedback_id)
    return pathlib.Path("feedback") / feedback_id / filename


class Feedback(core.models.AbstractModel):
    objects = feedback.managers.FeedbackManager()

    class _FeedbackTheme(django.db.models.IntegerChoices):
        ACCOUNT = 1, translation.gettext_lazy("Учетная запись")
        TECHNICAL_PROBLEMS = 2, translation.gettext_lazy("Технические проблемы")
        SUGGESTIONS = 3, translation.gettext_lazy("Отзывы и предложения")

    class _FeedbackStatus(django.db.models.IntegerChoices):
        CREATED = 1, translation.gettext_lazy("Создано")
        IN_PROCESS = 2, translation.gettext_lazy("В процессе")
        SUCCESS = 3, translation.gettext_lazy("Решено")

    user = django.db.models.OneToOneField(
        django.contrib.auth.models.User,
        on_delete=django.db.models.CASCADE,
    )
    theme = django.db.models.IntegerField(
        translation.gettext_lazy("тема обращения"),
        choices=_FeedbackTheme.choices,
        help_text=translation.gettext_lazy("Выберите тему обращения"),
    )
    status = django.db.models.IntegerField(
        translation.gettext_lazy("статус"),
        choices=_FeedbackStatus.choices,
    )
    text = django.db.models.TextField(
        translation.gettext_lazy("текст обращения"),
    )

    class Meta:
        ordering = ("theme",)
        verbose_name = translation.gettext_lazy("обратная связь")
        verbose_name_plural = translation.gettext_lazy("обратные связи")

    def __str__(self):
        return self.get_theme_display()


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

    class Meta:
        verbose_name = translation.gettext_lazy("дополнительный файл")
        verbose_name_plural = translation.gettext_lazy("дополнительные файлы")
