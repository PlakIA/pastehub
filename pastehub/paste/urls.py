from django.urls import path

from paste import views

app_name = "paste"

urlpatterns = [
    path("", views.create, name="create"),
    path("<str:short_link>/", views.detail, name="detail"),
    path("<str:short_link>/delete/", views.delete, name="delete"),
]
