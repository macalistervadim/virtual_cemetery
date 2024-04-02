import os

import django.core.asgi

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "virtual_cemetery.settings")

application = django.core.asgi.get_asgi_application()
