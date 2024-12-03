from datetime import timedelta

import django.conf
import django.contrib.auth.mixins
from django.core.mail import send_mail
from django.shortcuts import render, get_object_or_404
from django.utils import timezone


import users.forms
import users.models


def signup(request):
    form = users.forms.SignUpForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        user = form.save(commit=False)
        user.is_active = django.conf.settings.DEFAULT_USER_IS_ACTIVE
        user.save()

        if not user.is_active:
            activation_link = (
                f"http://127.0.0.1:8000/auth/activate/{user.username}/"
            )

            send_mail(
                subject="Активация",
                message=activation_link,
                from_email=django.conf.settings.MAIL,
                recipient_list=[user.email],
                fail_silently=True,
            )

            return render(
                request,
                "users/activation_sent.html",
                {"title": "Активация аккаунта"},
            )

    return render(request, "users/signup.html", {"form": form})


def activate(request, username):
    user = users.models.CustomUser.objects.get(username=username)

    if user.date_joined + timedelta(hours=12) > timezone.now():
        user.is_active = True
        user.save()

        print(user)
        print(user.is_active)

        return render(
            request,
            "users/activation_success.html",
            {"title": "Успешная активация"},
        )

    return render(
        request,
        "users/activation_expired.html",
        {"title": "Ссылка просрочена"},
    )


def user_detail(request, pk):
    user = get_object_or_404(users.models.CustomUser, pk=pk)
    profile_form = users.forms.ProfileForm(instance=user)

    return render(request, "users/profile.html", {"profile_form": profile_form})

__all__ = ()
