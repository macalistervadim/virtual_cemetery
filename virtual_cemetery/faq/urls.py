import django.urls

import faq.views

app_name = "faq"

urlpatterns = [
    django.urls.path("", faq.views.faq_view, name="faq"),
]
