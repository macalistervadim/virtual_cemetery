import pathlib
import uuid

import django.contrib.auth.models
import django.db
import django.utils.translation as translation


def item_directory_path(instance, filename):
    ext = filename.split(".")[-1]
    filename = f"{uuid.uuid4()}.{ext}"
    profile_id_str = str(instance.id)
    return pathlib.Path("profile") / profile_id_str / filename


class Profile(django.db.models.Model):
    user = django.db.models.OneToOneField(
        django.contrib.auth.models.User,
        on_delete=django.db.models.CASCADE,
    )
    avatar = django.db.models.ImageField(
        "фотография профиля",
        upload_to=item_directory_path,
        null=True,
        blank=True,
        help_text=translation.gettext_lazy("Выберите фотографию профиля"),
    )

    class Meta:
        verbose_name = translation.gettext_lazy("дополнительное поле")
        verbose_name_plural = translation.gettext_lazy(
            "дополнительные поля",
        )
        ordering = ("user",)

    def __str__(self):
        return self.user.username[:25]
