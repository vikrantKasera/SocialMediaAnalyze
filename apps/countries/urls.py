from django.urls import path
from . import views

app_name = "countries"

urlpatterns = [
    path("", views.list_countries, name="list"),
    path("add/", views.create_country, name="create"),
    path("<int:pk>/edit/", views.edit_country, name="edit"),
    path("<int:pk>/delete/", views.delete_country, name="delete"),
]
