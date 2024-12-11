from datetime import timedelta

import django.conf
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404, render
from django.utils import timezone

from paste.models import Paste
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
                "auth/activation_sent.html",
                {"title": "Активация аккаунта"},
            )

    return render(request, "auth/signup.html", {"form": form})


def activate(request, username):
    user = users.models.CustomUser.objects.get(username=username)

    if user.date_joined + timedelta(hours=12) > timezone.now():
        user.is_active = True
        user.save()

        return render(
            request,
            "auth/activation_success.html",
            {"title": "Успешная активация"},
        )

    return render(
        request,
        "auth/activation_expired.html",
        {"title": "Ссылка просрочена"},
    )


def user_detail(request, username):
    user = get_object_or_404(users.models.CustomUser, username=username)

    user_pastes = (
        user.pastes.select_related("category")
        .only(
            Paste.title.field.name,
            Paste.created.field.name,
            Paste.category.field.name,
            Paste.author.field.name,
        )
        .all()
    )

    return render(
        request,
        "users/user_detail.html",
        {"pastes": user_pastes, "user": user},
    )


@login_required
def profile_edit(request):
    profile_form = users.forms.ProfileForm(
        request.POST or None,
        request.FILES or None,
        instance=request.user,
    )
    if request.method == "POST" and profile_form.is_valid():
        profile_form.save()
        messages.success(request, "Все прошло успешно")

    user_info = {
        "image": request.user.image,
        "username": request.user.username,
        "email": request.user.email,
    }

    return render(
        request,
        "users/profile.html",
        {"profile_form": profile_form, "user": user_info},
    )


__all__ = ()
