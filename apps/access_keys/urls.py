from django.urls import path
from . import views

app_name = "access_keys"

urlpatterns = [
    path("", views.list_keys, name="list"),
    path("add/", views.create_key, name="create"),
    path("<int:pk>/edit/", views.edit_key, name="edit"),
    path("<int:pk>/delete/", views.delete_key, name="delete"),
]
