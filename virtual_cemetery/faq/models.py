import django.db
import django.utils.translation as translation

import faq.managers


class FaqQuestions(django.db.models.Model):
    """
    Модель частозадаваемых вопросов
    """

    objects = faq.managers.FaqManager()

    question = django.db.models.CharField(
        translation.gettext_lazy("вопрос"),
        max_length=100,
        help_text=translation.gettext_lazy("Введите частозадаваемый вопрос"),
    )
    answer = django.db.models.TextField(
        translation.gettext_lazy("ответ на вопрос"),
        max_length=350,
        help_text=translation.gettext_lazy(
            "Введите ответ на частозадаваемый вопрос (макс. 350 символов)",
        ),
    )
    created_on = django.db.models.DateField(
        translation.gettext_lazy("создано"),
        auto_now_add=True,
        editable=False,
    )

    class Meta:
        ordering = ("question",)
        verbose_name = translation.gettext_lazy("частозадаваемый вопрос")
        verbose_name_plural = translation.gettext_lazy("частозадаваемые вопросы")
