import django.contrib.auth.models
import django.db

import animals.models


class AnimalManager(django.db.models.Manager):
    def get_animals_list(self):
        queryset = (
            self.get_queryset()
            .order_by(
                "-" + animals.models.Animal.created_on.field.name,
            )
            .only(
                animals.models.Animal.name.field.name,
                animals.models.Animal.main_image.field.name,
            )
        )
        return queryset

    def get_animal_detail(self, pk):
        animal_queryset = (
            self.get_queryset()
            .filter(pk=pk)
            .select_related("user")
            .only(
                "user__first_name",
                "name",
                "main_image",
                "biography",
                "date_of_birth",
                "date_of_death",
            )
        )

        comment_queryset = (
            animals.models.AnimalComments.objects.filter(animal_id=pk)
            .select_related("user")
            .only(
                "user__first_name",
                "comment",
            )
        )

        animal = animal_queryset.first()
        animal.comments = comment_queryset

        return animal

    def get_animal_current_user(self, user):
        queryset = self.get_animals_list().filter(
            user=user,
        )
        return queryset
