from django.urls import path

from export.views import export_json, export_markdown, export_source


app_name = "export"

urlpatterns = [
    path(
        "<str:short_link>/<int:version>/source",
        export_source,
        name="source",
    ),
    path("<str:short_link>/<int:version>/json", export_json, name="json"),
    path(
        "<str:short_link>/<int:version>/markdown",
        export_markdown,
        name="markdown",
    ),
]
