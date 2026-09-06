from django.contrib import messages
from django.shortcuts import redirect, render

from .models import OutreachRun

def index(request):
    return render(request, "dashboard/outreach.html", {
        "active_page": "outreach",
        "run": OutreachRun.objects.filter(status=OutreachRun.STATUS_RUNNING).first(),
    })

def set_limit(request):
    if request.method == "POST":
        try:
            limit = max(1, int(request.POST.get("limit", 1000)))
        except (TypeError, ValueError):
            limit = 1000
        from apps.posting_criteria.models import PostingCriteria

        criteria = PostingCriteria.objects.filter(is_active=True).order_by("-updated_at").first()
        if criteria is None:
            criteria = PostingCriteria()
        criteria.max_creators = limit
        criteria.is_active = True
        criteria.save()
        messages.success(request, f"Limit updated to {limit}.")
    return redirect(request.META.get("HTTP_REFERER", "dashboard:index"))
