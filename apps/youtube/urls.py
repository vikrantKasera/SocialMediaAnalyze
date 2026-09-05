from django.urls import path
from . import views

app_name = "youtube"

urlpatterns = [
    path("outreach/", views.outreach, name="outreach"),
    path("outreach/start/", views.start_outreach, name="start_outreach"),
]
