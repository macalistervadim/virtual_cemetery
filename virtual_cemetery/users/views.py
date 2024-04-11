import django.contrib.auth.forms
import django.contrib.auth.models
import django.contrib.auth.views
import django.core.exceptions
import django.forms
import django.shortcuts
import django.utils.translation as translation


class CustomPasswordResetForm(django.contrib.auth.forms.PasswordResetForm):
    """
    Проверка на существование пользователя с указанной почтой в форме
    """

    def clean_email(self):
        email = self.cleaned_data.get("email")
        try:
            django.contrib.auth.models.User.objects.get(email=email)
        except django.core.exceptions.ObjectDoesNotExist:
            raise django.forms.ValidationError(
                translation.gettext_lazy("Пользователь с указанной почтой не найден"),
                code="invalid_email",
            )
        return email


class CustomPasswordResetView(django.contrib.auth.views.PasswordResetView):
    form_class = CustomPasswordResetForm


def profile_user(request):
    user = request.user

    template = "users/profile_user.html"
    context = {
        "user": user,
    }
    return django.shortcuts.render(request, template, context)
