from django.shortcuts import get_object_or_404, redirect, render

from core.crypto import aes256_decrypt, aes256_encrypt
from core.utils import delete_from_storage, get_from_storage, upload_to_storage
from paste.forms import GetPasswordForm, PasteForm
from paste.models import Paste


def create(request):
    form = PasteForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        instance = form.save(commit=False)

        if request.user.is_authenticated:
            instance.author = request.user

        content = form.cleaned_data.get("content")

        password = form.cleaned_data.get("password")
        if password:
            instance.is_protected = True
            content = aes256_encrypt(password, content)

        instance.save()
        upload_to_storage(f"pastes/{instance.id}", content)

        return redirect("paste:detail", short_link=instance.short_link)

    return render(
        request=request,
        template_name="paste/create.html",
        context={"form": form},
    )


def detail(request, short_link):
    paste = get_object_or_404(Paste, short_link=short_link)
    content = get_from_storage(f"pastes/{paste.id}")

    context = {"paste": paste, "content": content}

    if paste.is_protected:
        form = GetPasswordForm(request.POST or None)
        if request.method == "POST" and form.is_valid():
            password = form.cleaned_data.get("password")

            # Проверка на валидность пароля
            # Если пароль неверный - редирект на страницу создания пасты
            try:
                decrypted_content = aes256_decrypt(password, content)
            except ValueError:
                return redirect("paste:create")
            else:
                context["content"] = decrypted_content
                return render(
                    request=request,
                    template_name="paste/detail.html",
                    context=context,
                )

        return render(
            request=request,
            template_name="paste/get_password.html",
            context={"form": form},
        )

    return render(
        request=request,
        template_name="paste/detail.html",
        context=context,
    )


def delete(request, short_link):
    paste = get_object_or_404(Paste, short_link=short_link)

    delete_from_storage(f"pastes/{paste.id}")
    paste.delete()

    return redirect("paste:create")


__all__ = []
