import django.db
import django.utils.translation as translation


class Profile(django.db.models.Model):
    user = django.db.models.OneToOneField(
        django.contrib.auth.models.User,
        on_delete=django.db.models.CASCADE,
    )
    username = django.db.models.CharField(
        translation.gettext_lazy("имя пользователя"),
        help_text=translation.gettext_lazy("Имя пользователя"),
        max_length=50,
    )
    email = django.db.models.EmailField(
        translation.gettext_lazy("электронная почта"),
        help_text=translation.gettext_lazy("Адрес электронной почты"),
    )

    class Meta:
        verbose_name = translation.gettext_lazy("дополнительное поле")
        verbose_name_plural = translation.gettext_lazy(
            "дополнительные поля",
        )
        ordering = ("user",)

    def __str__(self):
        return self.user.username[:25]
