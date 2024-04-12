__all__ = ["AuthBackend"]

import django.conf
import django.contrib.auth.backends
from django.core.exceptions import ValidationError
import django.urls
import django.utils

import users.models


class AuthBackend(django.contrib.auth.backends.ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            if "@" in username:
                user = users.models.User.objects.by_mail(username)
            else:
                user = users.models.User.objects.get(username=username)
        except users.models.User.DoesNotExist:
            return None
        else:
            if user.check_password(password):
                user.profile.attempts_count = 0
                user.profile.save()
                return user

            user.profile.attempts_count += 1
            if user.profile.attempts_count >= django.conf.settings.MAX_AUTH_ATTEMPTS:
                user.is_active = False
                user.profile.block_date = django.utils.timezone.now()
                user.save()
                activate_url = request.build_absolute_uri(
                    django.urls.reverse(
                        "users:reactivate",
                        kwargs={"pk": user.id},
                    ),
                )
                django.core.mail.send_mail(
                    "SO many login attempts! ReActivate your account",
                    f"link to reactivate your account: {activate_url}",
                    django.conf.settings.DJANGO_MAIL,
                    [user.email],
                    fail_silently=False,
                )
                raise ValidationError("Превышено количество попыток входа. Aккаунт заблокирован")

            user.profile.save()

        return None
