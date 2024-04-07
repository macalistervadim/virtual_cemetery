import django.contrib
import django.urls

urlpatterns = [
    django.urls.path("admin/", django.contrib.admin.site.urls),
]

if django.conf.settings.DEBUG:
    import debug_toolbar

    urlpatterns += [
        django.urls.path(
            "__debug__/",
            django.urls.include(debug_toolbar.urls),
        ),
    ]
