import pathlib
import uuid

import django.contrib.auth
import django.core.validators
import django.db
import django.forms
import django.utils.translation as translation

import core.models
import event.managers


def item_directory_path(instance, filename):
    ext = filename.split(".")[-1]
    filename = f"{uuid.uuid4()}.{ext}"
    event_id = str(instance.id)
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
        related_name="winners_event"
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


class UserEvent(core.models.AbstractModel):
    """
    Участник конкурса
    """

    user = django.db.models.OneToOneField(
        django.contrib.auth.models.User,
        on_delete=django.db.models.CASCADE,
    )
    event = django.db.models.ForeignKey(
        Event,
        on_delete=django.db.models.CASCADE,
    )

    class Meta:
        ordering = ("event",)
        verbose_name = translation.gettext_lazy("участник")
        verbose_name_plural = translation.gettext_lazy("участники")

    def __str__(self):
        return self.user.username


class WorkUser(core.models.AbstractModel):
    """
    Работа участника конкурса
    """

    user = django.db.models.ForeignKey(
        UserEvent,
        on_delete=django.db.models.CASCADE,
    )
    subject = django.db.models.CharField(
        translation.gettext_lazy("название работы"),
        max_length=60,
        help_text=translation.gettext_lazy("Введите вашей название работы"),
    )
    body = django.db.models.TextField(
        translation.gettext_lazy("краткая предыстория"),
        max_length=500,
        help_text=translation.gettext_lazy("Укажите краткую предысторию по созданию работы (макс. 500 симв.)"),
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

    def __str__(self):
        return self.subject


class VoteEvent(core.models.AbstractModel):
    """
    Голосование за работы конкурса
    """

    class _EventVote(django.db.models.IntegerChoices):
        TERRIBLY = 1, translation.gettext_lazy("Ужасно")
        NOTBAD = 2, translation.gettext_lazy("Неплохо")
        NICE = 3, translation.gettext_lazy("Хорошо")
        EXCELLENT = 4, translation.gettext_lazy("Информационный")
        PERFECT = 5, translation.gettext_lazy("Восхитительно")

    user = django.db.models.OneToOneField(
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