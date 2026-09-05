from django.urls import path
from . import views

app_name = "results"

urlpatterns = [
    path("", views.list_results, name="list"),
    path("<int:pk>/download/", views.download_result, name="download"),
]
