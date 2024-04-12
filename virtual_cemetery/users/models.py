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


class UserManager(django.contrib.auth.models.UserManager):
    CANONICAL_DOMAINS = {
        "ya.ru": "yandex.ru",
    }

    DOTS = {
        "yandex.ru": "-",
        "gmail.com": "",
    }

    def get_queryset(self):
        user_related = django.contrib.auth.models.User.profile.related.name
        return (
            super()
            .get_queryset()
            .select_related(
                user_related,
            )
        )

    def active(self):
        return self.get_queryset().filter(is_active=True)

    def by_mail(self, mail):
        normilized_email = self.normalize_email(mail)
        return self.active().get(email=normilized_email)

    @classmethod
    def normalize_email(cls, email):
        email = super().normalize_email(email).lower()
        try:
            email_name, domain_part = email.strip().rsplit("@", 1)
            domain_part = cls.CANONICAL_DOMAINS.get(domain_part, domain_part)

            email_name = email_name.replace(
                ".",
                cls.DOTS.get(domain_part, "."),
            )
        except ValueError:
            pass
        else:
            email = email_name + "@" + domain_part.lower()

        return email


class User(django.contrib.auth.models.User):
    objects = UserManager()

    class Meta:
        proxy = True


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
    attempts_count = django.db.models.PositiveIntegerField(
        "Попыток входа",
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
