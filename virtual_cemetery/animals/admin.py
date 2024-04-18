import django.contrib

import animals.models


@django.contrib.admin.register(animals.models.Animal)
class AimalsAdmin(django.contrib.admin.ModelAdmin):
    readonly_fields = [
        "created_on",
        "updated_on",
    ]


@django.contrib.admin.register(animals.models.AnimalComments)
class AimalCommentsAdmin(django.contrib.admin.ModelAdmin):
    readonly_fields = [
        "created_on",
        "updated_on",
    ]
