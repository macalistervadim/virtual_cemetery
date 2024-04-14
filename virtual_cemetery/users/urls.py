import django.contrib.auth.views as auth_views
import django.forms
import django.urls


import users.views

app_name = "users"

urlpatterns = [
    django.urls.path(
        "login/",
        auth_views.LoginView.as_view(
            template_name="users/login/login.html",
            authentication_form=users.forms.AuthForm,
        ),
        name="login",
    ),
    django.urls.path(
        "logout/",
        auth_views.LogoutView.as_view(
            template_name="users/login/logout.html",
        ),
        name="logout",
    ),
    django.urls.path(
        "password-reset/",
        users.views.CustomPasswordResetView.as_view(
            template_name="users/reset_password/password_reset_form.html",
            email_template_name="users/reset_password/sent_mail/password_reset_email.html",
            subject_template_name="users/reset_password/sent_mail/password_reset_subject.txt",
            success_url=django.urls.reverse_lazy(
                "users:password-reset-done",
            ),
        ),
        name="password-reset",
    ),
    django.urls.path(
        "password-reset/done/",
        auth_views.PasswordResetDoneView.as_view(
            template_name="users/reset_password/password_reset_done.html",
        ),
        name="password-reset-done",
    ),
    django.urls.path(
        "password-reset/confirm/<uidb64>/<token>/",
        auth_views.PasswordResetConfirmView.as_view(
            template_name="users/reset_password/password_reset_confirm.html",
            success_url=django.urls.reverse_lazy(
                "users:password-reset-complete",
            ),
        ),
        name="password-reset-confirm",
    ),
    django.urls.path(
        "password-reset/complete/",
        auth_views.PasswordResetCompleteView.as_view(
            template_name="users/reset_password/password_reset_complete.html",
        ),
        name="password-reset-complete",
    ),
    django.urls.path(
        "password-change/",
        auth_views.PasswordChangeView.as_view(
            template_name="users/change_password/password_change.html",
            success_url=django.urls.reverse_lazy(
                "users:password-change-done",
            ),
        ),
        name="password-change",
    ),
    django.urls.path(
        "password-change/done/",
        auth_views.PasswordChangeDoneView.as_view(
            template_name="users/change_password/password_change_done.html",
        ),
        name="password-change-done",
    ),
    django.urls.path("profile/", users.views.profile_user, name="profile"),
    django.urls.path("profile/settings/", users.views.profile_user_change, name="profile_settings"),
    django.urls.path("signup/", users.views.SignUpView.as_view(), name="signup"),
    django.urls.path("activate/<pk>/", users.views.activate, name="activate"),
    django.urls.path("reactivate/<pk>/", users.views.reactivate, name="reactivate"),
]
