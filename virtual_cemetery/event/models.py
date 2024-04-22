import pathlib
import uuid

import django.contrib.auth
import django.core.validators
import django.db
import django.forms
import django.utils.translation as translation
import sorl.thumbnail

import core.models
import event.managers


def item_directory_path(instance, filename):
    ext = filename.split(".")[-1]
    event_id = str(instance.pk) if instance.pk else str(uuid.uuid4())
    filename = f"{event_id}.{ext}"
    return pathlib.Path("event") / event_id / filename


class Event(core.models.AbstractModel):
    objects = event.managers.EventManager()

    class _EventTheme(django.db.models.IntegerChoices):
        PHOTO = 1, translation.gettext_lazy("Фотоконкурс")
        LITERARY = 2, translation.gettext_lazy("Литературный")
        ARTISTIC = 3, translation.gettext_lazy("Художественный")
        INFO = 4, translation.gettext_lazy("Информационный")
        LEARNING = 5, translation.gettext_lazy("Образовательный")
        THEME = 6, translation.gettext_lazy("Тематический")

    class _EventCurrentStatus(django.db.models.IntegerChoices):
        STARTED = 1, translation.gettext_lazy("Стартовал")
        CLOSED = 2, translation.gettext_lazy("Завершен")

    user = django.db.models.OneToOneField(
        django.contrib.auth.models.User,
        on_delete=django.db.models.CASCADE,
    )
    theme = django.db.models.IntegerField(
        translation.gettext_lazy("тема конкурса"),
        choices=_EventTheme.choices,
        help_text=translation.gettext_lazy("Выберите тему конкурса"),
    )
    status = django.db.models.IntegerField(
        translation.gettext_lazy("статус конкурса"),
        choices=_EventCurrentStatus.choices,
        default=_EventCurrentStatus.STARTED,
    )
    subject = django.db.models.CharField(
        translation.gettext_lazy("название конкурса"),
        max_length=60,
    )
    body = django.db.models.CharField(
        translation.gettext_lazy("краткое описание конкурса"),
        max_length=150,
    )
    winners = django.db.models.ManyToManyField(
        django.contrib.auth.models.User,
        blank=True,
        related_name="winners_event",
    )
    prize = django.db.models.CharField(
        translation.gettext_lazy("приз"),
        max_length=200,
        help_text=translation.gettext_lazy("Укажите, какой приз получат победители"),
    )
    close_date = django.db.models.DateField(
        translation.gettext_lazy("дата окончания"),
    )

    class Meta:
        ordering = ("subject",)
        verbose_name = translation.gettext_lazy("конкурс")
        verbose_name_plural = translation.gettext_lazy("конкурсы")

    def __str__(self):
        return self.subject


class WorkUser(core.models.AbstractModel):
    """
    Работа участника конкурса
    """

    objects = event.managers.UserWorksManager()

    user = django.db.models.ForeignKey(
        django.contrib.auth.models.User,
        on_delete=django.db.models.CASCADE,
    )
    event = django.db.models.ForeignKey(
        Event,
        on_delete=django.db.models.CASCADE,
        verbose_name=translation.gettext_lazy("Выберите конкурс"),
    )
    subject = django.db.models.CharField(
        translation.gettext_lazy("название работы"),
        max_length=60,
        help_text=translation.gettext_lazy("Введите вашей название работы"),
    )
    body = django.db.models.TextField(
        translation.gettext_lazy("краткая предыстория"),
        max_length=500,
        help_text=translation.gettext_lazy(
            "Укажите краткую предысторию по созданию работы (макс. 500 симв.)",
        ),
    )
    files = django.db.models.FileField(
        translation.gettext_lazy("работа"),
        upload_to=item_directory_path,
        help_text=translation.gettext_lazy("Загрузите вашу работу"),
    )

    class Meta:
        ordering = ("subject",)
        verbose_name = translation.gettext_lazy("работа участника конкурса")
        verbose_name_plural = translation.gettext_lazy("работы участников конкурсов")
        unique_together = ("user", "event")

    def __str__(self):
        return self.subject

    def get_files_200x200(self):
        return sorl.thumbnail.get_thumbnail(
            self.files,
            "200x200",
            crop="center",
            quality=51,
        )

    def get_files_500x500(self):
        return sorl.thumbnail.get_thumbnail(
            self.files,
            "500x500",
            crop="center",
            quality=100,
        )

    def image_tmb(self):
        if self.files:
            return django.utils.html.mark_safe(
                f"<img src='{self.get_image_200x200().url}' width='50'>",
            )

        return translation.gettext_lazy("Нет загруженной работы")

    image_tmb.short_description = translation.gettext_lazy("превью")
    image_tmb.allow_tags = True
    image_tmb.field_name = "image_tmb"


class VoteEvent(core.models.AbstractModel):
    """
    Голосование за работы конкурса
    """

    class _EventVote(django.db.models.IntegerChoices):
        TERRIBLY = 1, translation.gettext_lazy("Ужасно")
        NOTBAD = 2, translation.gettext_lazy("Неплохо")
        NICE = 3, translation.gettext_lazy("Хорошо")
        EXCELLENT = 4, translation.gettext_lazy("Отлично")
        PERFECT = 5, translation.gettext_lazy("Восхитительно")

    user = django.db.models.ForeignKey(
        django.contrib.auth.models.User,
        on_delete=django.db.models.CASCADE,
    )
    work = django.db.models.ForeignKey(
        WorkUser,
        on_delete=django.db.models.CASCADE,
    )
    score = django.db.models.IntegerField(
        translation.gettext_lazy("оценка работы"),
        choices=_EventVote.choices,
        help_text=translation.gettext_lazy("Выберите подходящую оценку для работы"),
    )

    class Meta:
        ordering = ("work",)
        verbose_name = translation.gettext_lazy("оценка работы")
        verbose_name_plural = translation.gettext_lazy("оценки работ")

    def __str__(self):
        return self.user.username
