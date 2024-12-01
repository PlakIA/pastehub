from django.shortcuts import get_object_or_404, redirect, render

from core.crypto import aes256_decrypt, aes256_encrypt
from core.utils import delete_from_storage, get_from_storage, upload_to_storage
from paste.forms import GetPasswordForm, PasteForm, ProtectForm
from paste.models import Paste


def create(request):
    paste_form = PasteForm(request.POST or None)
    protect_form = ProtectForm(request.POST or None)

    if (
        request.method == "POST"
        and paste_form.is_valid()
        and protect_form.is_valid()
    ):
        instance = paste_form.save(commit=False)
        instance.is_protected = protect_form.cleaned_data.get("is_protected")
        instance.save()

        content = paste_form.cleaned_data.get("content")

        password = protect_form.cleaned_data.get("password")
        if password:
            content = aes256_encrypt(password, content)

        upload_to_storage(f"pastes/{instance.id}", content)

        return redirect("paste:detail", short_link=instance.short_link)

    return render(
        request=request,
        template_name="paste/create.html",
        context={"forms": [paste_form, protect_form]},
    )


def detail(request, short_link):
    paste = get_object_or_404(Paste, short_link=short_link)
    content = get_from_storage(f"pastes/{paste.id}")

    if paste.is_protected:
        form = GetPasswordForm(request.POST or None)
        if request.method == "POST" and form.is_valid():
            password = form.cleaned_data.get("password")
            print(password)

            try:
                content = aes256_decrypt(password, content)
                return render(
                    request=request,
                    template_name="paste/detail.html",
                    context={"paste": paste, "content": content},
                )

            except ValueError:
                return redirect("paste:create")

        return render(
            request=request,
            template_name="paste/get_password.html",
            context={"form": form},
        )

    return render(
        request=request,
        template_name="paste/detail.html",
        context={"paste": paste, "content": content},
    )


def delete(request, short_link):
    paste = get_object_or_404(Paste, short_link=short_link)

    delete_from_storage(f"pastes/{paste.id}")
    paste.delete()

    return redirect("paste:create")


__all__ = []
