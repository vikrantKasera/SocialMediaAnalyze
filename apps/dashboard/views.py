from django.contrib import messages
from django.shortcuts import redirect, render

def index(request):
    return render(request, "dashboard/outreach.html", {
        "active_page": "outreach",
        "logs": request.session.get("outreach_logs", []),
    })

def set_limit(request):
    if request.method == "POST":
        try:
            limit = max(1, int(request.POST.get("limit", 1000)))
        except (TypeError, ValueError):
            limit = 1000
        request.session["limit"] = limit
        messages.success(request, f"Limit updated to {limit}.")
    return redirect(request.META.get("HTTP_REFERER", "dashboard:index"))
