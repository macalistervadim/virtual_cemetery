import pathlib
import uuid

import django.contrib.auth
import django.core.validators
import django.db
import django.forms
import django.utils.translation as translation
import sorl.thumbnail

import animals.managers


def item_directory_path(instance, filename):
    ext = filename.split(".")[-1]
    animal_id = str(instance.pk) if instance.pk else str(uuid.uuid4())
    filename = f"{animal_id}.{ext}"
    return pathlib.Path("animals") / animal_id / filename


class Animal(django.db.models.Model):
    objects = animals.managers.AnimalManager()

    user = django.db.models.ForeignKey(
        django.contrib.auth.models.User,
        on_delete=django.db.models.CASCADE,
        related_name="animals",
    )
    name = django.db.models.CharField(
        translation.gettext_lazy("имя питомца"),
        max_length=70,
        help_text=translation.gettext_lazy("Введите имя вашего питомца"),
    )
    biography = django.db.models.TextField(
        translation.gettext_lazy("биография питомца"),
        max_length=1200,
        help_text=translation.gettext_lazy("Введите биографию вашего питомца"),
        null=True,
        blank=True,
    )
    date_of_birth = django.db.models.DateField(
        translation.gettext_lazy("дата рождения"),
        help_text=translation.gettext_lazy("Введите дату рождения вашего питомца"),
        blank=True,
        null=True,
    )
    date_of_death = django.db.models.DateField(
        translation.gettext_lazy("дата смерти"),
        help_text=translation.gettext_lazy("Введите дату смерти вашего питомца"),
        blank=True,
        null=True,
    )
    created_on = django.db.models.DateField(
        translation.gettext_lazy("создано"),
        auto_now_add=True,
        editable=False,
    )
    main_image = sorl.thumbnail.ImageField(
        translation.gettext_lazy("Изображение питомца"),
        help_text=translation.gettext_lazy("Загрузите изображение вашего питомца"),
        blank=True,
        null=True,
        upload_to=item_directory_path,
    )

    class Meta:
        ordering = ("name",)
        verbose_name = translation.gettext_lazy("питомец")
        verbose_name_plural = translation.gettext_lazy("питомцы")

    def get_image_200x200(self):
        return sorl.thumbnail.get_thumbnail(
            self.main_image,
            "200x200",
            crop="center",
            quality=51,
        )

    def get_image_500x500(self):
        return sorl.thumbnail.get_thumbnail(
            self.main_image,
            "500x500",
            crop="center",
            quality=100,
        )

    def image_tmb(self):
        if self.main_image:
            return django.utils.html.mark_safe(
                f"<img src='{self.get_image_200x200().url}' width='50'>",
            )

        return translation.gettext_lazy("Нет изображения питомца")

    image_tmb.short_description = translation.gettext_lazy("превью")
    image_tmb.allow_tags = True
    image_tmb.field_name = "image_tmb"


class AnimalImages(django.db.models.Model):
    animal = django.db.models.ForeignKey(
        Animal,
        on_delete=django.db.models.CASCADE,
        related_name="animal_images",
    )
    files = django.db.models.ImageField(
        translation.gettext_lazy("дополнительные изображения"),
        null=True,
        blank=True,
        upload_to=item_directory_path,
    )


class AnimalComments(django.db.models.Model):
    animal = django.db.models.ForeignKey(
        Animal,
        on_delete=django.db.models.CASCADE,
    )
    user = django.db.models.OneToOneField(
        django.contrib.auth.models.User,
        on_delete=django.db.models.CASCADE,
    )
    comment = django.db.models.CharField(
        translation.gettext_lazy("комментарий"),
        max_length=200,
        help_text=translation.gettext_lazy("Введите комментарий"),
    )
