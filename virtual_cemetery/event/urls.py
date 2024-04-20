import django.urls

import event.views

app_name = "event"

urlpatterns = [
    django.urls.path("all/", event.views.all_events_view, name="all-events"),
]
