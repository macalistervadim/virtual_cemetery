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

    def get_current_event(self, pk):
        queryset = self.get_queryset().filter(pk=pk).select_related("user")
        return queryset


class UserWorksManager(django.db.models.Manager):
    def get_current_event_works(self, pk):
        queryset = (
            self.get_queryset()
            .filter(event_id=pk)
            .select_related("user")
            .values(
                "user__username",
                event.models.WorkUser.subject.field.name,
                event.models.WorkUser.body.field.name,
                event.models.WorkUser.id.field.name,
            )
        )
        return queryset

    def get_current_work(self, pk):
        queryset = self.get_queryset().filter(pk=pk).select_related("user").first()
        return queryset
