import django.urls

import animals.views

app_name = "animals"

urlpatterns = [
    django.urls.path("detail/<pk>/", animals.views.animal_detail, name="animal-detail"),
    django.urls.path("add-new-animal/", animals.views.add_new_animal, name="add-animal"),
    django.urls.path("change/<pk>/", animals.views.change_current_animal, name="change-animal"),
    django.urls.path("delete-comment/<pk>/", animals.views.delete_comment, name="delete-comment"),
    django.urls.path("delete-animal/<pk>/", animals.views.delete_animal, name="delete-animal"),
]
