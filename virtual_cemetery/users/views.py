import datetime

import django.conf
import django.contrib
import django.contrib.auth.decorators
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
import django.utils.translation as translation
import django.views

import users.forms
import users.models


class CustomPasswordResetView(django.contrib.auth.views.PasswordResetView):
    form_class = users.forms.CustomPasswordResetForm


@django.contrib.auth.decorators.login_required
def profile_user(request):
    user = request.user
    template = "users/profile/profile_user.html"

    context = {
        "user": user,
    }
    return django.shortcuts.render(request, template, context)


@django.contrib.auth.decorators.login_required
def profile_user_change(request):
    template = "users/profile/profile_user_change.html"

    if request.method == "POST":
        profile_form = users.forms.ChangeProfile(
            request.POST or None,
            request.FILES or None,
            instance=request.user.profile,
        )
        user_form = users.forms.UserChangeForm(
            request.POST or None,
            instance=request.user,
        )

        if profile_form.is_valid() and user_form.is_valid():
            profile_form.save()
            user_form.save()
            django.contrib.messages.success(
                request,
                translation.gettext_lazy(
                    "Настройки успешно сохранены",
                ),
            )
            return django.shortcuts.redirect("users:profile")
    else:
        profile_form = users.forms.ChangeProfile(instance=request.user.profile)
        user_form = users.forms.UserChangeForm(instance=request.user)

    return django.shortcuts.render(
        request,
        template,
        {"profile_form": profile_form, "user_form": user_form},
    )


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


def resend_activation_email(request):
    if request.method == "POST":
        username = request.POST["username"]
        try:
            if "@" in username:
                user = users.models.User.objects.by_mail(username)
            else:
                user = users.models.User.objects.get(username=username)
            if user is not None and not user.is_active:
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
                django.contrib.messages.success(request, "Письмо успешно отправлено!")
                request.session["show_resend_button"] = False
        except users.models.User.DoesNotExist:
            django.contrib.messages.error(request, "Аккаунт не найден!")
            return django.shortcuts.redirect("users:login")

    return django.shortcuts.redirect("users:login")
