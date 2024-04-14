import django.contrib

import users.models


class ProfileInline(django.contrib.admin.TabularInline):
    model = users.models.Profile
    can_delete = False
    readonly_fields = ("block_date",)


class UserAdmin(django.contrib.auth.admin.UserAdmin):
    inlines = (ProfileInline,)


django.contrib.admin.site.unregister(django.contrib.auth.models.User)
django.contrib.admin.site.register(
    django.contrib.auth.models.User,
    UserAdmin,
)
