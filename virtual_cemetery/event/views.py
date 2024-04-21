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


def get_current_event_view(request, pk):
    template = "event/current_event.html"
    curr_event = event.models.Event.objects.get_current_event(pk=pk).first()
    curr_event_works = event.models.WorkUser.objects.get_current_event_works(pk=pk)

    context = {
        "event": curr_event,
        "works": curr_event_works,
    }

    return django.shortcuts.render(request, template, context)
