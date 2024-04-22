import django.urls

import event.views

app_name = "event"

urlpatterns = [
    django.urls.path("all/", event.views.all_events_view, name="all-events"),
    django.urls.path("register/", event.views.registration_event_work, name="register-work"),
    django.urls.path("work/<int:pk>/", event.views.get_current_work_event, name="current-work"),
    django.urls.path("<int:pk>/", event.views.get_current_event_view, name="current-event"),
]
