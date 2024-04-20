import django.contrib.auth.models
import django.db

import event.models


class EventManager(django.db.models.Manager):
    def get_all_events(self):
        queryset = (
            self.get_queryset()
            .order_by(
                "-" + event.models.Event.created_on.field.name,
            )
            .only(
                event.models.Event.theme.field.name,
                event.models.Event.subject.field.name,
                event.models.Event.body.field.name,
                event.models.Event.close_date.field.name,
            )
        )
        return queryset