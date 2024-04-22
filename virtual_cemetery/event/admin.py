import django.contrib

import event.models

django.contrib.admin.site.register(event.models.Event)
django.contrib.admin.site.register(event.models.WorkUser)
django.contrib.admin.site.register(event.models.VoteEvent)
