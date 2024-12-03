from django.contrib.auth import views as auth_views
from django.urls import path

import users.views


app_name = "users"

urlpatterns = [
    path("<str:username>/", users.views.user_detail, name="user-detail"),
    path("profile/edit/", users.views.profile_edit, name="profile-edit"),
]
