from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns

import api.views


app_name = "api"

urlpatterns = [
    path("paste/", api.views.PasteList.as_view(), name="paste-list"),
    path("paste/<str:short_link>/", api.views.PasteDetail.as_view(), name="paste-detail"),
]

urlpatterns = format_suffix_patterns(urlpatterns)
