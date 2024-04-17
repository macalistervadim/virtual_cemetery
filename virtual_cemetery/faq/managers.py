import django.contrib.auth.models
import django.db

import faq.models


class FaqManager(django.db.models.Manager):
    def get_faq_list(self):
        queryset = (
            self.get_queryset()
            .order_by(
                "-" + faq.models.FaqQuestions.created_on.field.name,
            )
            .only(
                faq.models.FaqQuestions.answer.field.name,
                faq.models.FaqQuestions.question.field.name,
            )
        )
        return queryset
