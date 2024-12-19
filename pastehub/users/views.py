from datetime import timedelta
import io
import json
import zipfile

import django.conf
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.core.paginator import Paginator
from django.http import (
    HttpResponse,
    HttpResponseBadRequest,
)
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.utils import timezone
from django.utils.crypto import get_random_string
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode

from core.storage import get_from_storage
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
            token = get_random_string(length=32)

            user.confirmation_token = token
            user.save()

            uid = urlsafe_base64_encode(force_bytes(user.pk))

            activate_url = request.build_absolute_uri(
                reverse(
                    "auth:activate",
                    kwargs={"uidb64": uid, "token": token},
                ),
            )

            send_mail(
                subject="Активация аккаунта",
                message=activate_url,
                html_message=f'<a href="{activate_url}">{activate_url}</a>',
                from_email=django.conf.settings.DEFAULT_FROM_EMAIL,
                recipient_list=[user.email],
            )

            return render(
                request,
                "auth/activation_sent.html",
                {"title": "Активация аккаунта", "user": user},
            )

    return render(request, "auth/signup.html", {"form": form})


def activate(request, uidb64, token):
    uid = force_str(urlsafe_base64_decode(uidb64))
    user = get_object_or_404(users.models.CustomUser, pk=uid)

    if (
        user.confirmation_token == token
        and user.date_joined + timedelta(hours=12) > timezone.now()
    ):
        user.is_active = True
        user.confirmation_token = None
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
        .order_by(Paste.created.field.name)
    )
    page = request.GET.get("page")
    if not str(page).isdigit():
        return HttpResponseBadRequest("Page is not integer")

    page = int(page)

    paginator = Paginator(user_pastes, 25)
    page_obj = paginator.get_page(page)
    return render(
        request,
        "users/user_detail.html",
        {
            "page_obj": page_obj,
            "list_pages": list(paginator.page_range),
            "user": user,
        },
    )


@login_required
def profile_edit(request):
    user = request.user
    profile_form = users.forms.ProfileForm(
        request.POST or None,
        request.FILES or None,
        instance=user,
    )

    if request.method == "POST" and profile_form.is_valid():
        profile_form.save()
        messages.success(request, "Профиль успешно сохранён")

    return render(
        request,
        "users/profile.html",
        {"form": profile_form, "user": user},
    )


def backup_pastes(request, username, format_file):
    if (
        format_file in ("source", "json", "md")
        and request.user.username == username
    ):
        buffer = io.BytesIO()
        zip_file = zipfile.ZipFile(buffer, "w")
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
        if format_file in "source":
            for paste in user_pastes:
                zip_file.writestr(
                    f"{paste.short_link}.txt",
                    get_from_storage(f"pastes/{paste.id}"),
                )
        elif format_file == "json":
            for paste in user_pastes:
                paste_dict = {
                    "content": get_from_storage(f"pastes/{paste.id}"),
                    "title": paste.title,
                    "author": str(paste.author),
                    "category": str(paste.category),
                    "created": str(paste.created),
                    "short_link": paste.short_link,
                }
                zip_file.writestr(
                    f"{paste.short_link}.json",
                    json.dumps(paste_dict).encode("utf-8"),
                )
        else:
            for paste in user_pastes:
                paste_text = get_from_storage(f"pastes/{paste.id}")
                zip_file.writestr(f"{paste.short_link}.md", paste_text)

        zip_file.close()

        response = HttpResponse(
            buffer.getvalue(),
            content_type="application/zip",
        )
        response["Content-Disposition"] = (
            f"attachment; filename=pastehub_{username}_"
            f"backup_{format_file}.zip"
        )

        return response

    return redirect("paste:create")


__all__ = ()
