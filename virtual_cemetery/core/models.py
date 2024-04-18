import django.db
import django.utils.translation as translation


class AbstractModel(django.db.models.Model):
    """
    Абстрактный класс с базовыми полями
    """

    created_on = django.db.models.DateTimeField(
        translation.gettext_lazy("создано"),
        auto_now_add=True,
    )
    updated_on = django.db.models.DateTimeField(
        translation.gettext_lazy("изменено"),
        auto_now=True,
    )

    class Meta:
        abstract = True
