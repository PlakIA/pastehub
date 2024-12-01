from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render

from core.utils import delete_from_storage, get_from_storage, upload_to_storage
from paste.forms import PasteForm
from paste.models import Paste


def create(request):
    form = PasteForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        instance = form.save()
        content = form.cleaned_data.get("content")
        upload_to_storage(f"pastes/{instance.id}", content)

        messages.success(
            request,
            f"{request.build_absolute_uri()}{instance.short_link}",
        )

        return redirect("paste:create")

    return render(
        request=request,
        template_name="paste/create.html",
        context={"form": form},
    )


def detail(request, short_link):
    paste = get_object_or_404(Paste, short_link=short_link)
    content = get_from_storage(f"pastes/{paste.id}")

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
