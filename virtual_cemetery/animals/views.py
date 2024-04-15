import django.contrib
import django.contrib.auth.decorators
import django.shortcuts
import django.utils.translation as translation

import animals.forms
import animals.models


def homepage_animals_view(request):
    template = "homepage/home.html"
    all_animals = animals.models.Animal.objects.get_animals_list()

    context = {
        "animals": all_animals,
    }

    return django.shortcuts.render(request, template, context)


def animal_detail(request, pk):
    template = "animals/animal_detail.html"
    animal = animals.models.Animal.objects.get_animal_detail(pk=pk).first()

    context = {
        "animal": animal,
    }

    return django.shortcuts.render(request, template, context)


@django.contrib.auth.decorators.login_required
def add_new_animal(request):
    template = "animals/add_new_animal.html"

    if request.method == "POST":
        form = animals.forms.AddNewAnimalForm(request.POST or None, request.FILES or None)
        if form.is_valid():
            new_animal = form.save(commit=False)
            new_animal.user = request.user
            new_animal.save()
            django.contrib.messages.success(
                request,
                translation.gettext_lazy(
                    "Новый пост успешно добавлен.",
                ),
            )

            return django.shortcuts.redirect("animals:animal-detail", pk=new_animal.pk)

    else:
        form = animals.forms.AddNewAnimalForm()

    return django.shortcuts.render(request, template, {"form": form})
