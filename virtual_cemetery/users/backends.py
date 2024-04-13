import django.conf
import django.contrib.auth.backends
import django.core.exceptions
import django.template
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
                user.profile.save()
                user.save()
                activate_url = request.build_absolute_uri(
                    django.urls.reverse(
                        "users:reactivate",
                        kwargs={"pk": user.id},
                    ),
                )
                django.core.mail.send_mail(
                    django.template.loader.render_to_string(
                        "users/login/sent_mail/reactivate_subject.txt",
                    ),
                    django.template.loader.render_to_string(
                        "users/login/sent_mail/reactivate_body.html",
                        {"activate_url": activate_url},
                    ),
                    django.conf.settings.DEFAULT_FROM_EMAIL,
                    [user.email],
                    fail_silently=False,
                )
                raise django.core.exceptions.ValidationError(
                    "Превышено количество попыток входа. Aккаунт заблокирован."
                    " Для разблокировки проверьте вашу эл. почту",
                )

            user.profile.save()  # хоть эта строчка не нужна на всякий случай пусть будет

        return None
