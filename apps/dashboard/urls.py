from django.urls import path
from . import views

app_name = "dashboard"

urlpatterns = [
    path("", views.index, name="index"),
    path("set-limit/", views.set_limit, name="set_limit"),
]
