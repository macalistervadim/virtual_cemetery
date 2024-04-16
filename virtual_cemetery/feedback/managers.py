import django.contrib.auth.models
import django.db

import feedback.models


class FeedbackManager(django.db.models.Manager):
    def get_feedbacks_list(self, user):
        queryset = (
            self.get_queryset()
            .filter(
                user=user,
            )
            .order_by(
                "-" + feedback.models.Feedback.created_on.field.name,
            )
            .only(
                feedback.models.Feedback.theme.field.name,
                feedback.models.Feedback.id.field.name,
            )
        )
        return queryset
