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
                animals.models.Animal.name.field.name,
                animals.models.Animal.main_image.field.name,
                animals.models.Animal.biography.field.name,
                animals.models.Animal.date_of_birth.field.name,
                animals.models.Animal.date_of_death.field.name,
            )
        )

        comment_queryset = (
            animals.models.AnimalComments.objects.filter(animal_id=pk)
            .select_related("user")
            .only(
                "user__first_name",
                animals.models.AnimalComments.comment.field.name,
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
