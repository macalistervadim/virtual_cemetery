import django.contrib

import faq.models


@django.contrib.admin.register(faq.models.FaqQuestions)
class FaqQuestionsAdmin(django.contrib.admin.ModelAdmin):
    readonly_fields = [
        "created_on",
        "updated_on",
    ]
