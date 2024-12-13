from django.urls import path

from report import views

app_name = "report"

urlpatterns = [
    path("<str:short_link>/", views.create, name="create"),
    path("<str:short_link>/review/", views.review, name="review"),
]
