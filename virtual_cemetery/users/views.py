from datetime import timedelta


from django.conf import settings
import django.contrib.auth.forms
import django.contrib.auth.models
import django.contrib.auth.views
import django.core.exceptions
from django.core.mail import send_mail
import django.forms
from django.http import HttpResponse
import django.shortcuts
from django.urls import reverse
from django.utils import timezone
from django.views import View


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


class SignUpView(View):
    def get(self, request):
        form = users.forms.CustomUserCreationForm()
        return django.shortcuts.render(request, "users/signup.html", {"form": form})

    def post(self, request):
        form = users.forms.CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = settings.DEFAULT_USER_IS_ACTIVE
            user.save()
            profile = users.models.Profile.objects.create(user=user)
            profile.save()

            activate_url = request.build_absolute_uri(
                reverse(
                    "users:activate",
                    kwargs={"pk": user.id},
                ),
            )

            send_mail(
                "Activate your account",
                f"link to activate your account: {activate_url}",
                settings.DJANGO_MAIL,
                [user.email],
                fail_silently=False,
            )
            return django.shortcuts.redirect("homepage:home")
        else:
            return django.shortcuts.render(request, "users/signup.html", {"form": form})


def activate(request, pk):
    user = django.contrib.auth.models.User.objects.get(pk=pk)
    if timezone.now() > user.date_joined + timedelta(hours=12):
        return HttpResponse("Ссылка на активацию истекла")

    user.is_active = True
    user.save()
    return HttpResponse(
        "<h1>Аккаунт активирован</h1> Но редиректа не будет",
        "<h1>ХАХАХХАХАХА</h1><br> Ведь это и есть выбор Врат Штейна)) ",
    )


def reactivate(requset, pk):
    user = users.models.User.objects.get(pk=pk)
    if user.profile.block_date + timedelta(days=7) > timezone.now():
        user.is_active = True
        user.save()

    return django.shortcuts.redirect(reverse("homepage:home"))
