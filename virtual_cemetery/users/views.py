import datetime

import django.conf
import django.contrib.auth.forms
import django.contrib.auth.models
import django.contrib.auth.views
import django.core.exceptions
import django.core.mail
import django.forms
import django.shortcuts
import django.template
import django.template.loader
import django.urls
import django.utils
import django.views


import users.forms
import users.models


class CustomPasswordResetView(django.contrib.auth.views.PasswordResetView):
    form_class = users.forms.CustomPasswordResetForm


def profile_user(request):
    user = request.user

    template = "users/profile_user.html"
    context = {
        "user": user,
    }
    return django.shortcuts.render(request, template, context)


class SignUpView(django.views.View):
    def get(self, request):
        form = users.forms.CustomUserCreationForm()
        return django.shortcuts.render(request, "users/signup/signup.html", {"form": form})

    def post(self, request):
        form = users.forms.CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = django.conf.settings.DEFAULT_USER_IS_ACTIVE
            user.save()
            profile = users.models.Profile.objects.create(user=user)
            profile.save()

            activate_url = request.build_absolute_uri(
                django.urls.reverse(
                    "users:activate",
                    kwargs={"pk": user.id},
                ),
            )
            django.core.mail.send_mail(
                django.template.loader.render_to_string(
                    "users/signup/sent_mail/activate_subject.html",
                ),
                django.template.loader.render_to_string(
                    "users/signup/sent_mail/activate_body.html",
                    {"activate_url": activate_url},
                ),
                django.conf.settings.DEFAULT_FROM_EMAIL,
                [user.email],
                fail_silently=False,
            )
            return django.shortcuts.redirect("homepage:home")
        else:
            return django.shortcuts.render(request, "users/signup/signup.html", {"form": form})


def activate(request, pk):
    """
    Активация аккаунта пользователя
    """
    user = django.contrib.auth.models.User.objects.get(pk=pk)
    if django.utils.timezone.now() > user.date_joined + datetime.timedelta(hours=12):
        return django.shortcuts.render(request, "users/signup/activate_false.html")

    user.is_active = True
    user.save()
    return django.shortcuts.render(request, "users/signup/activate_true.html")


def reactivate(requset, pk):
    """
    Разблокировка аккаунта пользователя (повторная активация)
    """
    user = users.models.User.objects.get(pk=pk)
    if user.profile.block_date + datetime.timedelta(days=7) > django.utils.timezone.now():
        user.is_active = True
        user.save()

    return django.shortcuts.redirect(django.urls.reverse("homepage:home"))
