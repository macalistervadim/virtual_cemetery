import django.contrib.auth.forms
import django.contrib.auth.models
import django.forms

import animals.models


class BootstrapFormMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for fieldn in self.visible_fields():
            fieldn.field.widget.attrs["class"] = "form-control"


class AddNewAnimalForm(BootstrapFormMixin, django.forms.ModelForm):
    class Meta:
        model = animals.models.Animal
        fields = (
            animals.models.Animal.name.field.name,
            animals.models.Animal.biography.field.name,
            animals.models.Animal.main_image.field.name,
            animals.models.Animal.date_of_birth.field.name,
            animals.models.Animal.date_of_death.field.name,
        )

    date_of_birth = django.forms.DateField(
        label="Дата рождения",
        help_text="Введите дату рождения вашего питомца",
        widget=django.forms.widgets.SelectDateWidget(),
        required=False,
    )
    date_of_death = django.forms.DateField(
        label="Дата смерти",
        help_text="Введите дату смерти вашего питомца",
        widget=django.forms.widgets.SelectDateWidget(),
        required=False,
    )


class AddNewAnimalComment(BootstrapFormMixin, django.forms.ModelForm):
    class Meta:
        model = animals.models.AnimalComments
        fields = (animals.models.AnimalComments.comment.field.name,)
