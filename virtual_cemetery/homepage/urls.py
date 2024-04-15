import django.urls

import animals.views

app_name = "homepage"

urlpatterns = [
    django.urls.path("", animals.views.homepage_animals_view, name="home"),
]
