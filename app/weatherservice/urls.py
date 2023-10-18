from django.urls import path

from . import views

app_name = "weatherservice"
urlpatterns = [
    path("", views.index, name="index"),
    path("id/<str:id>/", views.get_by_id, name="id"),
    path("city/<str:city>/", views.get_latest_for_city, name="latest"),
    path("new/", views.new, name="new"),
]