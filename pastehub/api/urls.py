from django.urls import path

import api.views


app_name = "api"

urlpatterns = [
    path("paste/", api.views.paste_list, name="paste-list"),
    path("paste/<str:short_link>/", api.views.paste_detail, name="paste-detail"),
]
