import django.contrib

import animals.models


django.contrib.admin.site.register(animals.models.Animal)
django.contrib.admin.site.register(animals.models.AnimalImages)
django.contrib.admin.site.register(animals.models.AnimalComments)
