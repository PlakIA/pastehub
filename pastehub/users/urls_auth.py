from django.contrib.auth import views as auth_views
from django.urls import path

import users.forms
import users.views


app_name = "auth"

urlpatterns = [
    path(
        "signup/",
        users.views.signup,
        name="signup",
    ),
    path(
        "activate/<str:username>/",
        users.views.activate,
        name="activate",
    ),
    path(
        "login/",
        auth_views.LoginView.as_view(
            template_name="auth/login.html",
            form_class=users.forms.BootstrapAuthenticationForm,
        ),
        name="login",
    ),
    path(
        "logout/",
        auth_views.LogoutView.as_view(
            template_name="auth/logout.html",
        ),
        name="logout",
    ),
]

urlpatterns_password_reset = [
    path(
        "password_change/",
        auth_views.PasswordChangeView.as_view(
            success_url="done",
            template_name="auth/password_change.html",
            form_class=users.forms.BootstrapPasswordChangeForm,
        ),
        name="password_change",
    ),
    path(
        "password_change/done",
        auth_views.PasswordChangeDoneView.as_view(
            template_name="auth/password_change_done.html",
        ),
        name="password_change",
    ),
    path(
        "password_reset/",
        auth_views.PasswordResetView.as_view(
            success_url="done",
            template_name="auth/password_reset.html",
            form_class=users.forms.BootstrapPasswordResetForm,
        ),
        name="password_reset",
    ),
    path(
        "password_reset/done/",
        auth_views.PasswordResetDoneView.as_view(
            template_name="auth/password_reset_done.html",
        ),
        name="password_reset_done",
    ),
    path(
        "reset/<uidb64>/<token>/",
        auth_views.PasswordResetConfirmView.as_view(
            template_name="auth/password_reset_confirm.html",
            form_class=users.forms.BootstrapSetPasswordForm,
        ),
        name="password_reset_confirm",
    ),
    path(
        "reset/done/",
        auth_views.PasswordResetCompleteView.as_view(
            template_name="auth/password_reset_complete.html",
        ),
        name="password_reset_complete",
    ),
]

urlpatterns += urlpatterns_password_reset
