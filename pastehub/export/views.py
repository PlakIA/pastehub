from django.http import FileResponse, HttpResponse, JsonResponse
from docx import Document

from core.utils import get_from_storage
from paste.models import Paste


def export_source(request, id_paste):
    paste_text = get_from_storage(f"pastes/{id_paste}")
    return FileResponse(
                paste_text,
                content_type="application/octet-stream",
                as_attachment=True,
    )


def export_json(request, id_paste):
    paste = Paste.objects.prefetch_related(
        "category").filter(id=id_paste).first()
    paste_text = get_from_storage(f"pastes/{id_paste}")
    json_dict = {
        "title": paste.title,
        "category": str(paste.category),
        "text": paste_text,
    }
    return JsonResponse(json_dict)


def export_docx(request, id_paste):
    paste = Paste.objects.prefetch_related(
        "category").filter(id=id_paste).first()
    paste_text = get_from_storage(f"pastes/{id_paste}")

    document = Document()
    document.add_heading(paste.title, level=3)
    document.add_paragraph(f"Категория: {paste.category}")
    document.add_paragraph(paste_text)
    response = HttpResponse(content_type="application/vnd."
                                         "openxmlformats-officedocument."
                                         "wordprocessingml.document")
    response["Content-Disposition"] = f"attachment; filename={id_paste}.docx"
    document.save(response)

    return response


__all__ = ["export_docx", "export_json", "export_source"]
