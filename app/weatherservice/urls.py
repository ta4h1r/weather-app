from django.urls import path

from . import views

app_name = "weatherservice"
urlpatterns = [
    path("", views.index, name="index"),
    path("new/", views.create, name="create"),
]