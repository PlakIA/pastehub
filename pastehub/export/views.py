from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404

from core.storage import get_from_storage
from paste.models import Paste


def export_source(request, short_link, version):
    paste = get_object_or_404(Paste, short_link=short_link)
    paste_text = get_from_storage(f"pastes/versions/{paste.id}_{version}")

    response = HttpResponse(paste_text, content_type="text/plain")
    response["Content-Disposition"] = (
        f"attachment; filename={short_link}_{version}.txt"
    )
    response["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response["Pragma"] = "no-cache"
    response["Expires"] = "0"

    return response


def export_json(request, short_link, version):
    paste = get_object_or_404(Paste, short_link=short_link)

    data = {
        "content": get_from_storage(f"pastes/versions/{paste.id}_{version}"),
        "title": paste.title,
        "author": str(paste.author),
        "category": str(paste.category),
        "created": paste.created,
        "short_link": paste.short_link,
    }
    response = JsonResponse(
        data,
        json_dumps_params={
            "indent": 4,
            "ensure_ascii": False,
        },
    )
    response.charset = "utf-8"
    response["Content-Disposition"] = (
        f"attachment; filename={short_link}_{version}.json"
    )
    response["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response["Pragma"] = "no-cache"
    response["Expires"] = "0"

    return response


def export_markdown(request, short_link, version):
    paste = get_object_or_404(Paste, short_link=short_link)
    paste_text = get_from_storage(f"pastes/versions/{paste.id}_{version}")
    markdown_content = (
        f"# Заметка с Pastehub: {paste.title}\n"
        f"### Категория: {paste.category}\n"
        f"### Автор: {paste.author}\n"
        f"### Создана: {paste.created}\n"
        f"#### Содержимое:\n{paste_text}"
    )

    response = HttpResponse(markdown_content, content_type="text/markdown")
    response["Content-Disposition"] = (
        f"attachment; filename={short_link}_{version}.md"
    )
    response["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response["Pragma"] = "no-cache"
    response["Expires"] = "0"

    return response


__all__ = ["export_markdown", "export_json", "export_source"]
