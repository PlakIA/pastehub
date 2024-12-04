from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("paste.urls")),
    path("auth/", include("users.urls")),
    path("auth/", include("django.contrib.auth.urls")),
    path("export/", include("export.urls")),
]
