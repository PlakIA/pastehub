from django.urls import path

from export.views import export_docx, export_json, export_source


app_name = "export"

urlpatterns = [
    path("source/<str:id_paste>", export_source, name="source"),
    path("json/<str:id_paste>", export_json, name="json"),
    path("docx/<str:id_paste>", export_docx, name="docx"),
]
