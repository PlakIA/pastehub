from django.urls import path

from qr_code import views

app_name = "qr_code"

urlpatterns = [
    path("preview/<path:url>/", views.qr_code_preview, name="preview"),
    path("download/<str:format_image>/<path:url>/", views.qr_code_download, name="download"),
]