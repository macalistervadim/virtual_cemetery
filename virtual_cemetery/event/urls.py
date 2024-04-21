import django.urls

import event.views

app_name = "event"

urlpatterns = [
    django.urls.path("all/", event.views.all_events_view, name="all-events"),
    django.urls.path("<pk>/", event.views.get_current_event_view, name="current-event"),
]
