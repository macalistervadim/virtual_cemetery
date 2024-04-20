import django.conf
import django.contrib
import django.contrib.auth.decorators
import django.shortcuts

import event.models


def all_events_view(request):
    template = "event/all_events.html"
    all_events = event.models.Event.objects.get_all_events()

    context = {
        "events": all_events,
    }

    return django.shortcuts.render(request, template, context)
