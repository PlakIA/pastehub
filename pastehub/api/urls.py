from django.conf import settings
from django.urls import path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions
from rest_framework.urlpatterns import format_suffix_patterns

import api.views

app_name = "api"


schema_view = get_schema_view(
    openapi.Info(
        title="API сервиса PasteHub",
        default_version="v1",
        description="API реализует функциональность CRUD относительно паст",
        contact=openapi.Contact(email=settings.DEFAULT_FROM_EMAIL),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)


urlpatterns = [
    path("", api.views.ApiRoot.as_view(), name="root"),
    path("paste/", api.views.PasteList.as_view(), name="paste-list"),
    path(
        "paste/<str:short_link>/",
        api.views.PasteDetail.as_view(),
        name="paste-detail",
    ),
    path(
        "paste/<str:short_link>/highlight/",
        api.views.PasteHighlight.as_view(),
        name="paste-detail-highlight",
    ),
    path("users/", api.views.UserList.as_view(), name="user-list"),
    path(
        "users/<int:pk>/",
        api.views.UserDetail.as_view(),
        name="user-detail",
    ),
    path("category/", api.views.CategoryList.as_view(), name="category-list"),
    path(
        "swagger/",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
]

urlpatterns = format_suffix_patterns(urlpatterns)
