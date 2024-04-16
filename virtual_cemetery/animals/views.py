import django.conf
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


@django.contrib.auth.decorators.login_required(login_url="users:login")
def add_new_animal(request):
    template = "animals/add_new_animal.html"

    if request.method == "POST":
        form = animals.forms.AddNewAnimalForm(request.POST, request.FILES)
        if form.is_valid():
            new_animal = form.save(commit=False)
            new_animal.user = request.user
            if "main_image" in request.FILES:
                new_animal.main_image = request.FILES["main_image"]
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


@django.contrib.auth.decorators.login_required(login_url="users:login")
def change_current_animal(request, pk):
    animal = django.shortcuts.get_object_or_404(animals.models.Animal, pk=pk)
    template = "animals/change_current_animal.html"

    if request.method == "POST":
        form = animals.forms.AddNewAnimalForm(request.POST, request.FILES, instance=animal)
        if form.is_valid():
            form.save()
            django.contrib.messages.success(
                request,
                translation.gettext_lazy(
                    "Запись отредактирована",
                ),
            )
            return django.shortcuts.redirect("animals:animal-detail", pk=animal.pk)
    else:
        form = animals.forms.AddNewAnimalForm(instance=animal)

    context = {
        "form": form,
        "animal": animal,
    }
    return django.shortcuts.render(request, template, context)
