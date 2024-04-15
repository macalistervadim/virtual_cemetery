import django.contrib.auth.models
import django.db

import animals.models


class AnimalManager(django.db.models.Manager):
    def get_animals_list(self):
        queryset = (
            self.get_queryset()
            .order_by(
                animals.models.Animal.created_on.field.name,
            )
            .only(
                animals.models.Animal.name.field.name,
                animals.models.Animal.main_image.field.name,
            )
        )
        return queryset

    def get_animal_detail(self, pk):
        queryset = (
            self.get_queryset()
            .filter(
                pk=pk,
            )
            .select_related("user")
            .only(
                "user__first_name",
                animals.models.Animal.name.field.name,
                animals.models.Animal.main_image.field.name,
                animals.models.Animal.biography.field.name,
                animals.models.Animal.date_of_birth.field.name,
                animals.models.Animal.date_of_death.field.name,
            )
        )
        return queryset
