import django.contrib
import django.urls

urlpatterns = [
    django.urls.path("admin/", django.contrib.admin.site.urls),
    django.urls.path("", django.urls.include("homepage.urls")),
]

if django.conf.settings.DEBUG:
    import debug_toolbar

    urlpatterns += [
        django.urls.path(
            "__debug__/",
            django.urls.include(debug_toolbar.urls),
        ),
    ]
