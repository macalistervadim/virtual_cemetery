import django.urls

import animals.views

app_name = "animals"

urlpatterns = [
    django.urls.path("detail/<pk>/", animals.views.animal_detail, name="animal-detail"),
    django.urls.path("add-new-animal/", animals.views.add_new_animal, name="add-animal"),
]
