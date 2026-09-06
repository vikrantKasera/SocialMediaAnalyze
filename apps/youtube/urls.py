from django.urls import path
from . import views

app_name = "youtube"

urlpatterns = [
    path("outreach/", views.outreach, name="outreach"),
    path("outreach/start/", views.start_outreach, name="start_outreach"),
    path("outreach/stop/", views.stop_outreach, name="stop_outreach"),
    path("outreach/status/<int:run_id>/", views.outreach_status, name="outreach_status"),
]
