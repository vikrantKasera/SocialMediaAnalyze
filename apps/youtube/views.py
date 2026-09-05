from django.shortcuts import redirect, render
from django.utils import timezone

def outreach(request):
    return render(request, "dashboard/outreach.html", {
        "active_page": "outreach",
        "logs": request.session.get("outreach_logs", []),
    })

def start_outreach(request):
    if request.method != "POST":
        return redirect("youtube:outreach")

    # Replace this demo section with your real service/task.
    now = timezone.localtime().strftime("%H:%M:%S")
    logs = [
        f"[{now}] Starting YouTube outreach process...",
        f"[{now}] Initializing search modules...",
        f"[{now}] Searching for creators...",
    ]

    request.session["outreach_logs"] = logs
    return redirect("youtube:outreach")
