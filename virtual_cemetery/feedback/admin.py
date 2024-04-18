import django.contrib

import feedback.models


@django.contrib.admin.register(feedback.models.Feedback)
class FeedbackAdmin(django.contrib.admin.ModelAdmin):
    readonly_fields = [
        "created_on",
        "updated_on",
    ]


django.contrib.admin.site.register(feedback.models.FeedbackFiles)
