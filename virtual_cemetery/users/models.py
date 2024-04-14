import pathlib
import uuid

import django.contrib.auth.models
import django.db
import django.utils.translation as translation
import sorl.thumbnail

import users.managers


def item_directory_path(instance, filename):
    ext = filename.split(".")[-1]
    filename = f"{uuid.uuid4()}.{ext}"
    profile_id_str = str(instance.id)
    return pathlib.Path("profile") / profile_id_str / filename


class User(django.contrib.auth.models.User):
    objects = users.managers.UserManager()

    class Meta:
        proxy = True


class Profile(django.db.models.Model):
    user = django.db.models.OneToOneField(
        django.contrib.auth.models.User,
        on_delete=django.db.models.CASCADE,
    )
    avatar = sorl.thumbnail.ImageField(
        "фотография профиля",
        upload_to=item_directory_path,
        null=True,
        blank=True,
        help_text=translation.gettext_lazy("Выберите фотографию профиля"),
    )
    attempts_count = django.db.models.PositiveIntegerField(
        "попыток входа",
        default=0,
    )
    block_date = django.db.models.DateTimeField(
        verbose_name="дата блокировки",
        blank=True,
        null=True,
    )

    class Meta:
        verbose_name = translation.gettext_lazy("дополнительное поле")
        verbose_name_plural = translation.gettext_lazy(
            "дополнительные поля",
        )
        ordering = ("user",)

    def __str__(self):
        return self.user.username[:25]

    def get_image_300x300(self):
        return sorl.thumbnail.get_thumbnail(
            self.avatar,
            "300x300",
            crop="center",
            quality=51,
        )

    def image_tmb(self):
        if self.image:
            return django.utils.html.mark_safe(
                f"<img src='{self.get_image_300x300().url}' width='50'>",
            )

        return translation.gettext_lazy("Нет аватарки")

    image_tmb.short_description = translation.gettext_lazy("превью")
    image_tmb.allow_tags = True
    image_tmb.field_name = "image_tmb"
