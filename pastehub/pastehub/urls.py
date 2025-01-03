from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

handler401 = "pastehub.views.handler401"
handler404 = "pastehub.views.handler404"
handler405 = "pastehub.views.handler405"
handler500 = "pastehub.views.handler500"

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("paste.urls")),
    path("users/", include("users.urls_users")),
    path("auth/", include("users.urls_auth")),
    path("auth/", include("django.contrib.auth.urls")),
    path("export/", include("export.urls")),
    path("qr_code/", include("qr_code.urls")),
    path("report/", include("report.urls")),
    path("i18n/", include("django.conf.urls.i18n")),
    path("api/v1/", include("api.urls")),
    path("api-auth/", include("rest_framework.urls")),
]

if settings.DEBUG:
    import debug_toolbar

    urlpatterns += (
        path(
            "__debug__/",
            include(debug_toolbar.urls),
        ),
    )

    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT,
    )
