from django.urls import path
from . import views

app_name = "relevance_keywords"

urlpatterns = [
    path("", views.list_keywords, name="list"),
    path("add/", views.create_keyword, name="create"),
    path("<int:pk>/edit/", views.edit_keyword, name="edit"),
    path("<int:pk>/delete/", views.delete_keyword, name="delete"),
]
