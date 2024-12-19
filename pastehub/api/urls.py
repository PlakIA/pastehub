from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns

import api.views

app_name = "api"

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
]

urlpatterns = format_suffix_patterns(urlpatterns)
