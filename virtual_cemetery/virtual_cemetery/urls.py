import django.contrib
import django.urls
import django.views

urlpatterns = [
    django.urls.path("admin/", django.contrib.admin.site.urls),
    django.urls.path("", django.urls.include("homepage.urls")),
    django.urls.path("about/", django.urls.include("about.urls")),
    django.urls.path("animals/", django.urls.include("animals.urls")),
    django.urls.path("users/", django.urls.include("users.urls")),
    django.urls.path("event/", django.urls.include("event.urls")),
    django.urls.path("faq/", django.urls.include("faq.urls")),
    django.urls.path("feedback/", django.urls.include("feedback.urls")),
    django.urls.path(
        "set-language/",
        django.views.i18n.set_language,
        name="set-language",
    ),
]

if django.conf.settings.DEBUG:
    import debug_toolbar
    import django.conf.urls.static

    STATIC_ROOT = django.conf.urls.static.static

    urlpatterns += (
        [
            django.urls.path(
                "__debug__/",
                django.urls.include(debug_toolbar.urls),
            ),
        ]
        + STATIC_ROOT(
            django.conf.settings.STATIC_URL,
            document_root=django.conf.settings.STATICFILES_DIRS,
        )
        + STATIC_ROOT(
            django.conf.settings.MEDIA_URL,
            document_root=django.conf.settings.MEDIA_ROOT,
        )
    )
