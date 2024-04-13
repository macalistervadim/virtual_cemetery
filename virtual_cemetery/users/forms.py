import django.contrib.auth.forms
from django.contrib.auth.models import User
import django.forms
import django.utils.translation as translation

import users.managers
import users.models


class BootstrapFormMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for fieldn in self.visible_fields():
            fieldn.field.widget.attrs["class"] = "form-control"


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


class CustomUserCreationForm(
    BootstrapFormMixin,
    django.contrib.auth.forms.UserCreationForm,
):
    class Meta(django.contrib.auth.forms.UserCreationForm.Meta):
        model = User
        fields = (
            User.email.field.name,
            User.username.field.name,
        )

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = users.managers.UserManager.normalize_email(user.email)
        if commit:
            user.save()

        return user

    def clean(self):
        cleaned_data = super().clean()
        if User.objects.filter(email=cleaned_data.get('email')).exists():
            self.add_error('email', "Эта почта уже зарегестрированна")
        return cleaned_data


class AuthForm(
    BootstrapFormMixin,
    django.contrib.auth.forms.AuthenticationForm,
):
    class Meta:
        model = users.models.User
        fields = (
            User.username.field.name,
            User.password.field.name,
        )
