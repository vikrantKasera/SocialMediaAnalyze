from django.urls import path
from . import views

app_name = "posting_criteria"

urlpatterns = [
    path("", views.edit_criteria, name="edit"),
]
