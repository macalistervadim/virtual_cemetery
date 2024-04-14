import django.contrib

import feedback.models

django.contrib.admin.site.register(feedback.models.Feedback)
django.contrib.admin.site.register(feedback.models.FeedbackFiles)
