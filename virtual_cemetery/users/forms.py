import django.contrib.auth
import django.forms
import django.utils.translation as translation

import core.forms
import users.managers
import users.models


class CustomPasswordChangeForm(
    core.forms.BootstrapFormMixin,
    django.contrib.auth.forms.PasswordChangeForm,
):
    pass


class CustomPasswordResetForm(
    core.forms.BootstrapFormMixin,
    django.contrib.auth.forms.PasswordResetForm,
):
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
    core.forms.BootstrapFormMixin,
    django.contrib.auth.forms.UserCreationForm,
):
    class Meta(django.contrib.auth.forms.UserCreationForm.Meta):
        model = django.contrib.auth.models.User
        fields = (
            django.contrib.auth.models.User.email.field.name,
            django.contrib.auth.models.User.username.field.name,
        )

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = users.managers.UserManager.normalize_email(user.email)
        if commit:
            user.save()

        return user

    def clean(self):
        cleaned_data = super().clean()
        if django.contrib.auth.models.User.objects.filter(email=cleaned_data.get("email")).exists():
            self.add_error("email", "Эта почта уже зарегестрированна")
        return cleaned_data


class AuthForm(
    core.forms.BootstrapFormMixin,
    django.contrib.auth.forms.AuthenticationForm,
):
    class Meta:
        model = users.models.User
        fields = (
            django.contrib.auth.models.User.username.field.name,
            django.contrib.auth.models.User.password.field.name,
        )


class ChangeProfile(
    core.forms.BootstrapFormMixin,
    django.forms.ModelForm,
):
    class Meta:
        model = users.models.Profile
        fields = [
            users.models.Profile.avatar.field.name,
        ]


class UserChangeForm(
    core.forms.BootstrapFormMixin,
    django.contrib.auth.forms.UserChangeForm,
):
    password = None

    class Meta(django.contrib.auth.forms.UserChangeForm.Meta):
        fields = [
            django.contrib.auth.models.User.first_name.field.name,
            django.contrib.auth.models.User.email.field.name,
        ]
        exclude = [
            django.contrib.auth.models.User.password.field.name,
        ]
